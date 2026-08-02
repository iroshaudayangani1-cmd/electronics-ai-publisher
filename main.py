from core.collector import collect_news

from core.article_writer import rewrite_articles

from core.image_generator import generate_images

from core.publisher import publish_articles


def main():

    print("=" * 60)
    print("EDATA SL AUTOMATION")
    print("=" * 60)

    print("\nStep 1 : Collecting Electronics News")

    collect_news()

    print("\nStep 2 : Rewriting Article")

    rewrite_articles()

    print("\nStep 3 : Generating AI Image")

    generate_images()

    print("\nStep 4 : Publishing")

    publish_articles()

    print("\nAll Tasks Completed Successfully")


if __name__ == "__main__":

    main()
