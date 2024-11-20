from PIL import Image
import numpy as np

# Fungsi Rotasi
def apply_rotation(image, degree):
    radians = np.deg2rad(degree)
    cos_val, sin_val = np.cos(radians), np.sin(radians)
    width, height = image.size
    new_width = int(abs(width * cos_val) + abs(height * sin_val))
    new_height = int(abs(width * sin_val) + abs(height * cos_val))
    rotated_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
    orig_center_x, orig_center_y = width / 2, height / 2
    new_center_x, new_center_y = new_width / 2, new_height / 2
    rotation_matrix = np.array([[cos_val, -sin_val], [sin_val, cos_val]])

    for x in range(new_width):
        for y in range(new_height):
            rel_x, rel_y = x - new_center_x, y - new_center_y
            orig_coords = np.linalg.inv(rotation_matrix) @ np.array([rel_x, rel_y])
            orig_x, orig_y = orig_coords + np.array([orig_center_x, orig_center_y])
            if 0 <= orig_x < width - 1 and 0 <= orig_y < height - 1:
                x0, y0 = int(orig_x), int(orig_y)
                dx, dy = orig_x - x0, orig_y - y0
                top_left = np.array(image.getpixel((x0, y0)))
                top_right = np.array(image.getpixel((x0 + 1, y0)))
                bottom_left = np.array(image.getpixel((x0, y0 + 1)))
                bottom_right = np.array(image.getpixel((x0 + 1, y0 + 1)))
                interpolated_pixel = (1 - dx) * (1 - dy) * top_left + dx * (1 - dy) * top_right + (1 - dx) * dy * bottom_left + dx * dy * bottom_right
                interpolated_pixel = tuple(interpolated_pixel.astype(int))
                rotated_image.putpixel((x, y), interpolated_pixel)
    return rotated_image

# Fungsi Refleksi
def apply_reflection(image, axis):
    if axis.lower() == 'x':
        reflection_matrix = [1, 0, 0, 0, -1, image.height]
    elif axis.lower() == 'y':
        reflection_matrix = [-1, 0, image.width, 0, 1, 0]
    else:
        print("Sumbu tidak valid. Pilih 'x' atau 'y'.")
        return image
    return image.transform(image.size, Image.AFFINE, reflection_matrix, resample=Image.BICUBIC)

# Fungsi Dilatasi
def apply_dilation(image, scale):
    dilation_matrix = [scale, 0, 0, 0, scale, 0]
    return image.transform(image.size, Image.AFFINE, dilation_matrix, resample=Image.BICUBIC)

# Fungsi Proyeksi
def apply_projection(image, shear, axis):
    if axis.lower() == 'x':
        projection_matrix = [1, shear, 0, 0, 1, 0]
    elif axis.lower() == 'y':
        projection_matrix = [1, 0, 0, shear, 1, 0]
    else:
        print("Sumbu tidak valid. Pilih 'x' atau 'y'.")
        return image
    return image.transform(image.size, Image.AFFINE, projection_matrix, resample=Image.BICUBIC)
