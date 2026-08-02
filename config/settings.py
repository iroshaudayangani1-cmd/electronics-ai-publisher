
import os

# ==========================
# GEMINI
# ==========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash"

GEMINI_MAX_RETRIES = 5
GEMINI_RETRY_DELAY = 15

# ==========================
# BLOGGER
# ==========================

BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")

# ==========================
# CLOUDINARY
# ==========================

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# ==========================
# FACEBOOK
# ==========================

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

# ==========================
# FILES
# ==========================

NEWS_JSON = "output/news/news.json"
REWRITTEN_JSON = "output/news/rewritten.json"
