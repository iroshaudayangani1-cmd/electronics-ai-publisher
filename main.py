
from core.news_collector import collect_news
from core.article_rewriter import rewrite_articles
from core.image_generator import generate_images
from core.publisher import publish_articles


def main():

    print("===== ELECTRONICS AI PUBLISHER =====")

    print("\nStep 1 : Collecting Articles")
    collect_news()

    print("\nStep 2 : Rewriting")
    rewrite_articles()

    print("\nStep 3 : Creating Images")
    generate_images()

    print("\nStep 4 : Publishing")
    publish_articles()

    print("\nDone.")


if __name__ == "__main__":
    main()
