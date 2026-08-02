
import json
import os
import time

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_MAX_RETRIES,
    GEMINI_RETRY_DELAY,
    NEWS_JSON,
    REWRITTEN_JSON,
)


# ==========================================================
# CLEAN GEMINI RESPONSE
# ==========================================================

def clean_json(text):

    if not text:
        return ""

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ==========================================================
# LOAD BEST ARTICLE
# ==========================================================

def rewrite_articles():

    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY not found.")

    if not os.path.exists(NEWS_JSON):
        raise Exception(f"{NEWS_JSON} not found.")

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    with open(
        NEWS_JSON,
        "r",
        encoding="utf-8"
    ) as f:

        news = json.load(f)

    articles = news.get("articles", [])

    if not articles:

        print("No articles found.")
        return

    # Only rewrite the highest scoring article

    article = articles[0]

    print("=" * 60)
    print("BEST ARTICLE")
    print("=" * 60)
    print(article["title"])
    print("=" * 60)

    prompt = f"""
You are a professional electronics editor.

You write for

EDATA SL

https://edatasl.blogspot.com

Your audience:

• Electronics Engineers
• Arduino Developers
• ESP32 Developers
• Raspberry Pi Users
• Embedded Engineers
• Robotics Developers
• IoT Engineers
• Students
• DIY Electronics Makers

Your task is to rewrite the article professionally.

DO NOT copy sentences.

Write naturally.

700–1200 words.

Use HTML.

Return ONLY valid JSON.

No markdown.

No explanations.

Return exactly this JSON:

{{
"title":"",
"slug":"",
"category":"",
"meta_description":"",
"tags":[],
"image_prompt":"",
"article":""
}}

Allowed categories:

DIY
Arduino
ESP32
Raspberry Pi
Embedded
Electronics
IoT
Robotics
Technology News
Repair

Original Title

{article["title"]}

Original Summary

{article["summary"]}

Original Source

{article["source"]}

Original URL

{article["url"]}
"""
      # ==========================================================
    # GEMINI REQUEST
    # ==========================================================

    rewritten = []

    success = False

    for attempt in range(1, GEMINI_MAX_RETRIES + 1):

        try:

            print(f"\nAttempt {attempt}/{GEMINI_MAX_RETRIES}")

            print("=" * 60)
            print("MODEL:", GEMINI_MODEL)
            print("=" * 60)

            response = client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt,

            )

            text = clean_json(response.text)

            data = json.loads(text)

            data["original_title"] = article["title"]

            data["original_source"] = article["source"]

            data["original_url"] = article["url"]

            if article.get("image"):

                data["original_image"] = article["image"]

            rewritten.append(data)

            print("✓ Rewrite completed.")

            success = True

            break

        except Exception as e:

            print(f"Attempt {attempt} failed:")
            print(e)

            error = str(e).lower()

            if (
                "503" in error
                or "unavailable" in error
                or "429" in error
            ):

                wait = GEMINI_RETRY_DELAY * attempt

                print(
                    f"Waiting {wait} seconds..."
                )

                time.sleep(wait)

                continue

            break

    if not success:

        print("Failed to rewrite article.")

        return
          # ==========================================================
    # SAVE REWRITTEN ARTICLE
    # ==========================================================

    os.makedirs("output/news", exist_ok=True)

    with open(

        REWRITTEN_JSON,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            rewritten,

            f,

            indent=4,

            ensure_ascii=False,

        )

    print("\n" + "=" * 60)
    print("REWRITE COMPLETED")
    print("=" * 60)
    print("Articles rewritten :", len(rewritten))
    print("Saved to:", REWRITTEN_JSON)
    print("=" * 60)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    rewrite_articles()
