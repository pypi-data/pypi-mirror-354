import cv2


def convert_an_image_to_numpy_array(img_path):
    """Đọc từ đường dẫn ảnh và convert thành mảng numpy

    Args:
        img_path (_type_): đường dẫn đến ảnh
    """
    img = cv2.imread(img_path)
    img = cv2.cvtColor(
        img, cv2.COLOR_BGR2RGB
    )  # Vì cv2 đọc ảnh theo BGR (ngược với RGB)
    return img
