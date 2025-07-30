from Mylib import sk_fit_incremental_model, myfuncs, myclasses
import numpy as np
import time
import gc
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LogisticRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
import os
from pathlib import Path


class ModelTrainer:
    PARAM_DICT_FILENAME = "param_dict.pkl"
    LIST_PARAM_FILENAME = "list_param.pkl"
    SCORING_FILENAME = "scoring.pkl"

    SCORINGS_PREFER_MININUM = ["log_loss", "mse", "mae"]
    SCORINGS_PREFER_MAXIMUM = ["accuracy", "roc_auc"]

    def __init__(
        self,
        model_training_path,
        num_models,
        param_dict,
        train_features,
        train_target,
        val_features,
        val_target,
        scoring,
    ):
        self.model_training_path = model_training_path
        self.num_models = num_models
        self.param_dict = param_dict
        self.train_features = train_features
        self.train_target = train_target
        self.val_features = val_features
        self.val_target = val_target
        self.scoring = scoring

        self.save_data_before_training()

    def save_data_before_training(self):
        self.param_dict_path = self.model_training_path / self.PARAM_DICT_FILENAME
        scoring_path = self.model_training_path / self.SCORING_FILENAME

        myfuncs.save_python_object_without_overwrite(
            self.param_dict_path, self.param_dict
        )
        myfuncs.save_python_object_without_overwrite(scoring_path, self.scoring)

    def train(
        self,
    ):
        # Khởi tạo biến cho logging
        log_message = ""

        # Tạo thư mục lưu kết quả mô hình tốt nhất
        model_training_run_path = Path(
            f"{self.model_training_path}/{self.get_folder_name()}"
        )
        myfuncs.create_directories([model_training_run_path])

        # Get list_param và lưu lại
        list_param = self.get_list_param()
        myfuncs.save_python_object(
            Path(f"{model_training_run_path}/{self.LIST_PARAM_FILENAME}"), list_param
        )

        # Get các tham số cần thiết khác
        best_val_scoring = -np.inf
        sign_for_val_scoring_find_best_model = (
            self.get_sign_for_val_scoring_to_find_best_model()
        )

        best_model_result_path = Path(f"{model_training_run_path}/best_result.pkl")

        # Logging
        log_message += f"Kết quả model tốt nhất lưu tại {model_training_run_path}\n"
        log_message += f"Kết quả train từng model:\n"

        for i, param in enumerate(list_param):
            try:
                # Tạo after transformer
                after_transformer = myfuncs.convert_list_estimator_into_pipeline(
                    param["list_after_transformer"]
                )

                # Transform đặc trưng của tập train và val
                train_features = after_transformer.fit_transform(self.train_features)
                val_features = after_transformer.transform(self.val_features)

                # Tạo model
                model = self.create_model(param)

                # Train model
                print(f"Train model {i} / {self.num_models}")
                model.fit(train_features, self.train_target)

                train_scoring = myfuncs.evaluate_model_on_one_scoring(
                    model,
                    train_features,
                    self.train_target,
                    self.scoring,
                )
                val_scoring = myfuncs.evaluate_model_on_one_scoring(
                    model,
                    val_features,
                    self.val_target,
                    self.scoring,
                )

                # In kết quả
                training_result_text = f"{param}\n -> Val {self.scoring}: {val_scoring}, Train {self.scoring}: {train_scoring}\n"
                print(training_result_text)

                # Logging
                log_message += training_result_text

                # Cập nhật best model và lưu lại
                val_scoring_find_best_model = (
                    val_scoring * sign_for_val_scoring_find_best_model
                )

                if best_val_scoring < val_scoring_find_best_model:
                    best_val_scoring = val_scoring_find_best_model

                    # Lưu kết quả
                    myfuncs.save_python_object(
                        best_model_result_path,
                        (param, val_scoring, train_scoring),
                    )

            except:
                continue

        # In ra kết quả của model tốt nhất
        best_model_result = myfuncs.load_python_object(best_model_result_path)
        best_model_result_text = f"Model tốt nhất\n{best_model_result[0]}\n -> Val {self.scoring}: {best_model_result[1]}, Train {self.scoring}: {best_model_result[2]}\n"
        print(best_model_result_text)

        # Logging
        log_message += best_model_result_text

        return log_message

    def create_model(self, param):
        ClassName = globals()[param["model_name"]]

        param.pop("list_after_transformer")
        param.pop("model_name")

        return ClassName(**param)

    def get_list_param(self):
        # Get full_list_param
        param_dict = myfuncs.load_python_object(self.param_dict_path)
        full_list_param = myfuncs.get_full_list_dict(param_dict)

        # Get folder của run
        run_folders = self.get_run_folders()

        if len(run_folders) > 0:
            # Get list param còn lại
            for run_folder in run_folders:
                list_param = myfuncs.load_python_object(
                    Path(
                        f"{self.model_training_path}/{run_folder}/{self.LIST_PARAM_FILENAME}"
                    )
                )
                full_list_param = myfuncs.subtract_2list_set(
                    full_list_param, list_param
                )

        # Random list
        return myfuncs.randomize_list(full_list_param, self.num_models)

    def get_folder_name(self):
        # Get các folder lưu model tốt nhất
        run_folders = self.get_run_folders()

        if len(run_folders) == 0:  # Lần đầu tiên chạy thì là run0
            return "run0"

        number_in_run_folders = run_folders.str.extract(r"(\d+)").astype("int")[
            0
        ]  # Các con số trong run0, run1, ... (0, 1, )
        folder_name = f"run{number_in_run_folders.max() +1}"  # Tên folder sẽ là số lớn nhất để prevent trùng
        return folder_name

    def get_sign_for_val_scoring_to_find_best_model(self):
        if self.scoring in self.SCORINGS_PREFER_MININUM:
            return -1

        if self.scoring in self.SCORINGS_PREFER_MAXIMUM:
            return 1

        raise ValueError(f"Chưa định nghĩa cho {self.scoring}")

    def get_run_folders(self):
        run_folders = pd.Series(os.listdir(self.model_training_path))
        run_folders = run_folders[run_folders.str.startswith("run")]
        return run_folders


class ModelTrainerOnBatches:
    def __init__(
        self,
        training_batches_folder_path,
        model_training_path,
        num_models,
        base_model,
        param_dict,
        val_feature,
        val_target,
        scoring,
        model_saving_val_scoring_limit,
    ):

        self.training_batches_folder_path = training_batches_folder_path
        self.model_training_path = model_training_path
        self.num_models = num_models
        self.base_model = base_model
        self.param_dict = param_dict
        self.val_feature = val_feature
        self.val_target = val_target
        self.scoring = scoring
        self.model_saving_val_scoring_limit = model_saving_val_scoring_limit

    def train_models(
        self,
    ):
        log_message = ""
        list_param = myfuncs.randomize_dict(self.param_dict, self.num_models)
        best_val_scoring = -np.inf
        sign_for_val_scoring_find_best_model = (
            sk_model_training_funcs.get_sign_for_val_scoring_find_best_model(
                self.scoring
            )
        )
        model_saving_val_scoring_limit = (
            model_saving_val_scoring_limit * sign_for_val_scoring_find_best_model
        )

        # Get số lượng batch cần train
        num_batch = myfuncs.load_python_object(
            f"{self.training_batches_folder_path}/num_batch.pkl"
        )

        for i, param in enumerate(list_param):
            # Tạo model
            model = self.create_model(param)

            # Train model
            print(f"Train model {i} / {self.num_models}")
            start_time = time.time()
            train_scoring = self.train_on_batches(model, num_batch)
            training_time = time.time() - start_time

            val_scoring = myfuncs.evaluate_model_on_one_scoring(
                model,
                self.val_feature,
                self.val_target,
                self.scoring,
            )

            # In kết quả
            training_result_text = f"{param}\n -> Val {self.scoring}: {val_scoring}, Train {self.scoring}: {train_scoring}, Time: {training_time} (s)\n"
            print(training_result_text)

            # Logging
            log_message += training_result_text

            # Cập nhật best model và lưu lại
            val_scoring_find_best_model = (
                val_scoring * sign_for_val_scoring_find_best_model
            )

            if best_val_scoring < val_scoring_find_best_model:
                best_val_scoring = val_scoring_find_best_model

                # Lưu model
                if best_val_scoring > model_saving_val_scoring_limit:
                    myfuncs.save_python_object(
                        f"{self.model_training_path}/model.pkl", model
                    )

                # Lưu kết quả
                myfuncs.save_python_object(
                    f"{self.model_training_path}/result.pkl",
                    (param, val_scoring, train_scoring, training_time),
                )

            # Giải phóng bộ nhớ
            del model
            gc.collect()

        # In ra kết quả của model tốt nhất
        best_model_result = myfuncs.load_python_object(
            f"{self.model_training_path}/result.pkl"
        )
        best_model_result_text = f"Model tốt nhất\n{best_model_result[0]}\n -> Val {self.scoring}: {best_model_result[1]}, Train {self.scoring}: {best_model_result[2]}, Time: {best_model_result[3]} (s)\n"

        print(best_model_result_text)

        # Logging
        log_message += best_model_result_text

        return log_message

    def create_model(self, param):
        ClassName = globals()[self.base_model]
        return ClassName(**param)

    def train_on_batches(self, model, num_batch):
        list_train_scoring = (
            []
        )  # Cần biến này vì có thể sau này lấy min, max, ... tùy ý

        # Fit batch đầu tiên
        first_feature_batch = myfuncs.load_python_object(
            f"{self.training_batches_folder_path}/train_features_0.pkl"
        )
        first_target_batch = myfuncs.load_python_object(
            f"{self.training_batches_folder_path}/train_target_0.pkl"
        )

        # Lần đầu nên fit bình thường
        print("Train batch thứ 0")
        model.fit(first_feature_batch, first_target_batch)

        first_train_scoring = myfuncs.evaluate_model_on_one_scoring(
            model,
            first_feature_batch,
            first_target_batch,
            self.scoring,
        )

        list_train_scoring.append(first_train_scoring)

        # Fit batch thứ 1 trở đi
        for i in range(1, num_batch - 1 + 1):
            feature_batch = myfuncs.load_python_object(
                f"{self.training_batches_folder_path}/train_features_{i}.pkl"
            )
            target_batch = myfuncs.load_python_object(
                f"{self.training_batches_folder_path}/train_target_{i}.pkl"
            )

            # Lần thứ 1 trở đi thì fit theo kiểu incremental
            print(f"Train batch thứ {i}")
            sk_fit_incremental_model.fit_model_incremental_learning(
                model, feature_batch, target_batch
            )

            train_scoring = myfuncs.evaluate_model_on_one_scoring(
                model,
                feature_batch,
                target_batch,
                self.scoring,
            )

            list_train_scoring.append(train_scoring)

        return list_train_scoring[-1]  # Lấy kết quả trên batch cuối cùng


class ModelTrainingResultGatherer:
    MODEL_TRAINING_FOLDER_PATH = "artifacts/model_training"
    SCORINGS_PREFER_MININUM = ["log_loss", "mse", "mae"]
    SCORINGS_PREFER_MAXIMUM = ["accuracy", "roc_auc"]

    def __init__(self, scoring):
        self.scoring = scoring
        pass

    def next(self):
        model_training_paths = [
            f"{self.MODEL_TRAINING_FOLDER_PATH}/{item}"
            for item in os.listdir(self.MODEL_TRAINING_FOLDER_PATH)
        ]

        result = []
        for folder_path in model_training_paths:
            result += self.get_result_from_1folder(folder_path)

        # Sort theo val_scoring (ở vị trí thứ 1)
        result = sorted(
            result,
            key=lambda item: item[1],
            reverse=self.get_reverse_param_in_sorted(),
        )
        return result

    def get_result_from_1folder(self, folder_path):
        run_folder_names = pd.Series(os.listdir(folder_path))
        run_folder_names = run_folder_names[
            run_folder_names.str.startswith("run")
        ].tolist()
        run_folder_paths = [f"{folder_path}/{item}" for item in run_folder_names]

        list_result = []
        for folder_path in run_folder_paths:
            result = myfuncs.load_python_object(f"{folder_path}/result.pkl")
            list_result.append(result)

        return list_result

    def get_reverse_param_in_sorted(self):
        if self.scoring in self.SCORINGS_PREFER_MAXIMUM:
            return True

        if self.scoring in self.SCORINGS_PREFER_MININUM:
            return False

        raise ValueError(f"Chưa định nghĩa cho {self.scoring}")


class LoggingDisplayer:
    DATE_FORMAT = "%d-%m-%Y-%H-%M-%S"
    READ_FOLDER_NAME = "artifacts/logs"
    WRITE_FOLDER_NAME = "artifacts/gather_logs"

    # Tạo thư mục
    os.makedirs(WRITE_FOLDER_NAME, exist_ok=True)

    def __init__(self, mode, file_name=None, start_time=None, end_time=None):
        self.mode = mode
        self.file_name = file_name
        self.start_time = start_time
        self.end_time = end_time

        if self.file_name is None:
            self.file_name = f"{datetime.now().strftime(self.DATE_FORMAT)}.log"

    def print_and_save(self):
        file_path = f"{self.WRITE_FOLDER_NAME}/{self.file_name}"

        if self.mode == "all":
            result = self.gather_all_logging_result()
        else:
            result = self.gather_logging_result_from_start_to_end_time()

        print(result)
        print(f"Lưu result tại {file_path}")
        myfuncs.write_content_to_file(result, file_path)

    def gather_all_logging_result(self):
        logs_filenames = self.get_logs_filenames()

        return self.read_from_logs_filenames(logs_filenames)

    def gather_logging_result_from_start_to_end_time(self):
        logs_filenames = pd.Series(self.get_logs_filenames())
        logs_filenames = logs_filenames[
            (logs_filenames > self.start_time) & (logs_filenames < self.end_time)
        ].tolist()

        return self.read_from_logs_filenames(logs_filenames)

    def read_from_logs_filenames(self, logs_filenames):
        result = ""
        for logs_filename in logs_filenames:
            logs_filepath = f"{self.READ_FOLDER_NAME}/{logs_filename}.log"
            content = myfuncs.read_content_from_file(logs_filepath)
            result += f"{content}\n\n"

        return result

    def get_logs_filenames(self):
        logs_filenames = os.listdir(self.READ_FOLDER_NAME)
        date_format_in_filename = f"{self.DATE_FORMAT}.log"
        logs_filenames = [
            datetime.strptime(item, date_format_in_filename) for item in logs_filenames
        ]
        logs_filenames = sorted(logs_filenames)  # Sắp xếp theo thời gian tăng dần
        return logs_filenames


class BestParamSearcher:
    PARAM_DICT_FILENAME = "param_dict.pkl"
    BEST_RESULT_FILENAME = "best_result.pkl"

    SCORINGS_PREFER_MININUM = ["log_loss", "mse", "mae"]
    SCORINGS_PREFER_MAXIMUM = ["accuracy", "roc_auc"]

    def __init__(self, model_training_path, scoring):
        self.model_training_path = model_training_path
        self.scoring = scoring

    def next(self):
        run_folders = self.get_run_folders()
        list_result = []

        for run_folder in run_folders:
            best_result_path = (
                self.model_training_path / run_folder / self.BEST_RESULT_FILENAME
            )
            list_result.append(myfuncs.load_python_object(best_result_path))

        best_param = self.get_best_param(list_result)
        return best_param

    def get_run_folders(self):
        run_folders = pd.Series(os.listdir(self.model_training_path))
        run_folders = run_folders[run_folders.str.startswith("run")]
        return run_folders

    def get_best_param(self, list_result):
        list_result = sorted(
            list_result,
            key=lambda item: item[1],
            reverse=self.get_reverse_param_in_sorted(),
        )  # Sort theo val scoring
        return list_result[0][0]

    def get_reverse_param_in_sorted(self):
        if self.scoring in self.SCORINGS_PREFER_MAXIMUM:
            return True

        if self.scoring in self.SCORINGS_PREFER_MININUM:
            return False

        raise ValueError(f"Chưa định nghĩa cho {self.scoring}")


class ModelEvaluator:
    def __init__(
        self,
        train_features,
        train_target,
        val_features,
        val_target,
        class_names,
        best_param,
        model_evaluation_on_train_val_path,
    ):
        self.train_features = train_features
        self.train_target = train_target
        self.val_features = val_features
        self.val_target = val_target
        self.class_names = class_names
        self.param = best_param
        self.model_evaluation_on_train_val_path = model_evaluation_on_train_val_path

    def next(self):
        log_message = ""

        # Tạo after transformer
        after_transformer = myfuncs.convert_list_estimator_into_pipeline(
            self.param["list_after_transformer"]
        )

        # Transform đặc trưng của tập train và val
        train_features = after_transformer.fit_transform(self.train_features)
        val_features = after_transformer.transform(self.val_features)

        # Tạo model
        model = self.create_model(self.param)

        # Train model
        model.fit(train_features, self.train_target)

        # Đánh giá
        model_result_text = "===============Kết quả đánh giá model==================\n"

        # Đánh giá model trên tập val
        result_text, val_confusion_matrix = myclasses.ClassifierEvaluator(
            model=model,
            class_names=self.class_names,
            train_feature_data=val_features,
            train_target_data=self.val_target,
        ).evaluate()
        model_result_text += result_text  # Thêm đoạn đánh giá vào

        # Lưu lại confusion matrix cho tập val
        val_confusion_matrix_path = Path(
            f"{self.model_evaluation_on_train_val_path}/confusion_matrix.png"
        )
        val_confusion_matrix.savefig(
            val_confusion_matrix_path, dpi=None, bbox_inches="tight", format=None
        )

        # Lưu vào file results.txt
        with open(
            f"{self.model_evaluation_on_train_val_path}/result.txt", mode="w"
        ) as file:
            file.write(model_result_text)

        # Logging
        log_message += model_result_text

        return log_message

    def create_model(self, param):
        ClassName = globals()[param["model_name"]]
        param.pop("list_after_transformer")
        param.pop("model_name")
        return ClassName(**param)
