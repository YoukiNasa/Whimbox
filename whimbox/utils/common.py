import numpy as np

def is_rgba_image(image: np.ndarray):
    """
    验证 np.ndarray 是否为 H, W, 4 形状的 RGBA 图像。

    Args:
        image (np.ndarray): 待验证的图像数组。

    Returns:
        bool: 如果是 H, W, 4 形状的数组则返回 True，否则返回 False。
    """
    return image.ndim == 3 and image.shape[2] == 4

def convert_bbox_to_absolute(rel_coords, img_width, img_height):
    """
    将相对坐标转换为绝对坐标。

    Args:
        rel_coords (list): 包含 [x_ratio, y_ratio, width_ratio, height_ratio] 的列表。
                           比例值应在 0.0 到 1.0 之间。
                           如果 width_ratio(height_ratio) 为 -1.0，则边界框的表示绝对宽度（绝对高度）将被设置为与绝对高度（绝对宽度）相等。
                           width_ratio 和 height_ratio 不能同时为 -1.0。
        img_width (int): 图像的宽度。
        img_height (int): 图像的高度。

    Returns:
        tuple: (x1, y1, x2, y2)，表示边界框左上角和右下角的绝对坐标。
    """
    rel_x1, rel_y1, rel_width, rel_height = rel_coords

    if rel_width == -1.0 and rel_height == -1.0:
        raise ValueError(
            f"Invalid bbox coordinates {rel_coords}: "
            "rel_width and rel_height cannot both be -1.0 simultaneously."
        )

    if rel_width == -1.0:
        abs_height = int(rel_height * img_height)
        abs_width = abs_height
    elif rel_height == -1.0:
        abs_width = int(rel_width * img_width)
        abs_height = abs_width
    else:
        abs_width = int(rel_width * img_width)
        abs_height = int(rel_height * img_height)

    x1 = int(rel_x1 * img_width)
    y1 = int(rel_y1 * img_height)
    x2 = x1 + abs_width
    y2 = y1 + abs_height

    return x1, y1, x2, y2