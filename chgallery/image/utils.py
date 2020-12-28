from PIL import Image, UnidentifiedImageError


def is_allowed_image_file(fn):
    """
    Checks if file is actual image and it's mime type is allowed.
    It uses Pillow to check image type.

    :param fn: A filename (string), pathlib.Path object or a file object
    :rtype bool:
    """
    try:
        return Image.open(fn).format in ('JPEG', 'PNG', 'GIF')
    except UnidentifiedImageError:
        return False


def smart_resize(image, max_size=2000):
    """
    Resize image to `max_size` using it's bigger size (either width or height).
    This will set wide image width to `max_size` and adjust height accordingly.

    :param image: Pillow.Image object
    :param max_size: maximum value of width or height in pixels.
    :rtype Pillow.Image:
    """
    if image.width >= image.height:
        new_width = max_size
        new_height = int(new_width / image.width * image.height)
    else:
        new_height = max_size
        new_width = int(new_height / image.height * image.width)

    return image.resize((new_width, new_height))
