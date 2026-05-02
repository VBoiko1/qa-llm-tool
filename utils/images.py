import base64


def encode_image(file):
    file.seek(0)
    return base64.b64encode(file.read()).decode("utf-8")


def get_image_mime_type(file):
    return file.type or "image/png"