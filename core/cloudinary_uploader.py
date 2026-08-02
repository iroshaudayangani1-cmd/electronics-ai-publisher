
import os

import cloudinary
import cloudinary.uploader

from config.settings import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)


# ==========================================================
# CLOUDINARY CONFIG
# ==========================================================

cloudinary.config(

    cloud_name=CLOUDINARY_CLOUD_NAME,

    api_key=CLOUDINARY_API_KEY,

    api_secret=CLOUDINARY_API_SECRET,

    secure=True,

)


# ==========================================================
# UPLOAD IMAGE
# ==========================================================

def upload_image(image_path):

    if not os.path.exists(image_path):

        raise FileNotFoundError(image_path)

    try:

        result = cloudinary.uploader.upload(

            image_path,

            folder="edata-sl",

            resource_type="image",

            overwrite=True,

        )

        return result["secure_url"]

    except Exception as e:

        print("Cloudinary Upload Error")

        print(e)

        raise
