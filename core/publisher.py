import json
import os
from datetime import datetime

from config.settings import REWRITTEN_JSON

from core.blogger import (
    publish_post,
    get_recent_titles,
)

from core.facebook import (
    publish_to_facebook,
)


def publish_articles():

    if not os.path.exists(REWRITTEN_JSON):
        print("No rewritten articles.")
        return

    with open(
        REWRITTEN_JSON,
        "r",
        encoding="utf-8"
    ) as f:

        articles = json.load(f)

    if not articles:
        print("No rewritten articles.")
        return

    existing_titles = get_recent_titles()

    for article in articles:

        title = article["title"]

        if title.lower() in existing_titles:

            print(f"Skipping duplicate: {title}")
            continue

        tags = article.get("tags", [])

        if article.get("category"):

            if article["category"] not in tags:

                tags.append(article["category"])

        today = datetime.utcnow().strftime("%B %d, %Y")

        image_html = ""

        if article.get("image_url"):

            image_html = f"""
<div style="text-align:center;margin:25px 0;">
<img src="{article['image_url']}"
alt="{title}"
style="width:100%;max-width:900px;height:auto;border-radius:10px;">
</div>
"""

        content = f"""
<div style="max-width:900px;margin:auto;font-family:Arial,sans-serif;font-size:18px;line-height:1.8;">

<h1>{title}</h1>

<p><strong>Published:</strong> {today}</p>

<hr>

{image_html}

{article["article"]}

<hr>

<h3>About EDATA SL</h3>

<p>

EDATA SL shares practical electronics,
embedded systems,
Arduino,
ESP32,
Raspberry Pi,
IoT,
repair guides,
DIY projects
and technical news for engineers,
students and makers.

</p>

<hr>

<p style="font-size:14px;color:#666;">

Original news rewritten with AI for educational purposes.

</p>

</div>
"""

        print("\nPublishing to Blogger...")

        result = publish_post(

            title=title,

            content=content,

            tags=tags,

        )

        print(result["url"])

        print("\nPublishing to Facebook...")

        publish_to_facebook(

            title=title,

            blog_url=result["url"],

        )

    print("\nPublishing completed.")


if __name__ == "__main__":

    publish_articles()
