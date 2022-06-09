from PIL import Image


def handle_image_incompatibilities(
    image: Image,
    image_format: str,
    image_size: int,
    image_width: int,
    image_height: int,
    image_mode: str,
) -> Image:
    if (
        image_format == "JPEG"
        or image_format == "PNG"
        or image_format == "GIF"
        or image_format == "BMP"
    ):
        if image_size > 1000000:
            image = image.resize((image_width, image_height))
            image = image.convert("RGB")
            image = image.resize((image_width, image_height))
            image = image.convert(image_mode)
        else:
            image = image.convert(image_mode)
    else:
        image = image.convert(image_mode)
    return image
