import json
import requests

from config.settings import (
    BLOG_ID,
    BLOGGER_CLIENT_ID,
    BLOGGER_CLIENT_SECRET,
    BLOGGER_REFRESH_TOKEN,
)


# ==========================================================
# GET ACCESS TOKEN
# ==========================================================

def get_access_token():

    print("=" * 60)
    print("BLOGGER DEBUG")
    print("=" * 60)

    print("BLOG_ID:", BLOG_ID)
    print("CLIENT_ID:", BLOGGER_CLIENT_ID[:20] + "...")
    print("CLIENT_SECRET exists:", bool(BLOGGER_CLIENT_SECRET))
    print("REFRESH_TOKEN exists:", bool(BLOGGER_REFRESH_TOKEN))

    if BLOGGER_REFRESH_TOKEN:
        print("Refresh token length:", len(BLOGGER_REFRESH_TOKEN))

    print("=" * 60)

    token_url = "https://oauth2.googleapis.com/token"

    payload = {

        "client_id": BLOGGER_CLIENT_ID,

        "client_secret": BLOGGER_CLIENT_SECRET,

        "refresh_token": BLOGGER_REFRESH_TOKEN,

        "grant_type": "refresh_token",

    }

    response = requests.post(
        token_url,
        data=payload,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["access_token"]
  # ==========================================================
# PUBLISH POST
# ==========================================================

def publish_post(title, content, tags):

    access_token = get_access_token()

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"

    headers = {

        "Authorization": f"Bearer {access_token}",

        "Content-Type": "application/json",

    }

    payload = {

        "kind": "blogger#post",

        "title": title,

        "content": content,

        "labels": tags,

    }

    response = requests.post(

        url,

        headers=headers,

        json=payload,

        timeout=120,

    )

    print("=" * 60)
    print("BLOGGER DEBUG")
    print("=" * 60)
    print("Status Code:", response.status_code)

    if response.status_code != 200:

        print(response.text)

    response.raise_for_status()

    data = response.json()

    print("✓ Blogger accepted the post.")

    return {

        "id": data["id"],

        "url": data["url"],

    }
  # ==========================================================
# GET RECENT TITLES
# ==========================================================

def get_recent_titles(limit=20):

    access_token = get_access_token()

    url = (
        f"https://www.googleapis.com/blogger/v3/blogs/"
        f"{BLOG_ID}/posts?maxResults={limit}"
    )

    headers = {

        "Authorization": f"Bearer {access_token}"

    }

    response = requests.get(

        url,

        headers=headers,

        timeout=60,

    )

    response.raise_for_status()

    data = response.json()

    titles = set()

    for post in data.get("items", []):

        title = post.get("title", "").strip().lower()

        if title:

            titles.add(title)

    return titles


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("Testing Blogger connection...")

    titles = get_recent_titles()

    print(f"Found {len(titles)} recent posts.")
