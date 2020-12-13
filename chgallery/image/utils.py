from PIL import Image, UnidentifiedImageError


def is_allowed_image_file(file_path):
    try:
        img = Image.open(file_path)
        return img.format in ('JPEG', 'PNG', 'GIF')
    except UnidentifiedImageError:
        return False


def smart_resize(image, max_size=2000):

    if image.width >= image.height:
        new_width = max_size
        new_height = int(new_width / image.width * image.height)
    else:
        new_height = max_size
        new_width = int(new_height / image.height * image.width)

    return image.resize((new_width, new_height))


def smart_thumbnail(image, max_width=250):
    height = int(max_width / image.width * image.height)
    return image.resize((max_width, height))
