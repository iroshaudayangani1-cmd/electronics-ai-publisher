import json
import os
import requests
import urllib.parse

from config.settings import (
    REWRITTEN_JSON,
    IMAGE_FOLDER,
)

from core.cloudinary_uploader import upload_image


def generate_images():

    if not os.path.exists(REWRITTEN_JSON):
        print("No rewritten articles found.")
        return

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    for i, article in enumerate(articles, start=1):

        prompt = article.get("image_prompt", "")

        if not prompt:
            print(f"Article {i}: No image prompt.")
            continue

        print(f"\nGenerating AI image for article {i}...")

        encoded = urllib.parse.quote(prompt)

        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            "?width=1280&height=720&model=flux"
        )

        filename = os.path.join(
            IMAGE_FOLDER,
            f"article_{i}.jpg"
        )

        try:

            response = requests.get(
                image_url,
                timeout=120,
            )

            if response.status_code != 200:
                print("Image generation failed.")
                continue

            with open(filename, "wb") as img:
                img.write(response.content)

            print("✓ AI image generated")

            print("Uploading to Cloudinary...")

            cloudinary_url = upload_image(filename)

            article["image"] = filename
            article["image_url"] = cloudinary_url

            print("✓ Uploaded successfully")
            print(cloudinary_url)

        except Exception as e:

            print("Image error:")
            print(e)

    with open(REWRITTEN_JSON, "w", encoding="utf-8") as f:
        json.dump(
            articles,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\nFinished generating AI images.")


if __name__ == "__main__":
    generate_images()
