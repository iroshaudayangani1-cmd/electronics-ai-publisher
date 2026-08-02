import json
import os
import time

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_MAX_RETRIES,
    GEMINI_RETRY_DELAY,
    REWRITTEN_JSON,
)

from core.cloudinary_uploader import upload_image


# ==========================================================
# IMAGE GENERATOR
# ==========================================================

def generate_images():

    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY not found.")

    if not os.path.exists(REWRITTEN_JSON):
        raise Exception(REWRITTEN_JSON)

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    with open(
        REWRITTEN_JSON,
        "r",
        encoding="utf-8"
    ) as f:

        articles = json.load(f)

    if not articles:

        print("No rewritten articles found.")
        return

    for index, article in enumerate(articles, start=1):

        print(f"\nGenerating image for article {index}")

        image_prompt = article.get("image_prompt", "")

        if not image_prompt:

            image_prompt = f"""
Ultra realistic editorial electronics photograph.

Subject:

{article["title"]}

Requirements:

Professional electronics laboratory

Printed circuit boards

Electronic components

Modern workbench

Natural lighting

High detail

Photojournalism

Cinematic composition

16:9 aspect ratio

No text

No logo

No watermark

No illustration

Real photograph
"""
        success = False

        for attempt in range(1, GEMINI_MAX_RETRIES + 1):

            try:

                print(f"Attempt {attempt}/{GEMINI_MAX_RETRIES}")

                response = client.models.generate_images(

                    model="imagen-4.0-generate-preview",

                    prompt=image_prompt,

                )

                image = response.generated_images[0].image

                filename = f"electronics_{index}.png"

                image.save(filename)

                print("✓ AI image generated")

                print("Uploading to Cloudinary...")

                image_url = upload_image(filename)

                article["image_url"] = image_url

                print("✓ Uploaded successfully")

                print(image_url)

                if os.path.exists(filename):

                    os.remove(filename)

                success = True

                break

            except Exception as e:

                print(e)

                wait = GEMINI_RETRY_DELAY * attempt

                print(f"Retrying in {wait} seconds...")

                time.sleep(wait)

        if not success:

            print("Image generation failed.")

            article["image_url"] = ""
              # ==========================================================
    # SAVE UPDATED ARTICLES
    # ==========================================================

    with open(
        REWRITTEN_JSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            articles,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\nFinished generating AI images.")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    generate_images()


