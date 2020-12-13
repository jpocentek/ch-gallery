from PIL import Image, UnidentifiedImageError


def is_allowed_image_file(file_path):
    try:
        img = Image.open(file_path)
        return img.format in ('JPEG', 'PNG', 'GIF')
    except UnidentifiedImageError:
        return False
