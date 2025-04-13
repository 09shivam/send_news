import feedparser
from datetime import datetime
from dateutil import parser

# Add more RSS feeds here
RSS_FEEDS = {
    "SemiWiki": "https://semiwiki.com/category/semiconductor-news/feed/",
    "EETimes": "https://www.eetimes.com/feed/",
    "EDN Network": "https://www.edn.com/feed/",
    "AnandTech": "https://www.anandtech.com/rss/",
    "TechCrunch (Chips)": "https://techcrunch.com/tag/semiconductors/feed/",
}

def fetch_news(keywords=None):
    """
    Fetches news articles from multiple RSS feeds.
    Optionally filters articles by the provided keywords and sorts by date.
    """
    articles = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            summary = entry.get("summary", "")
            if isinstance(summary, dict):
                # Sometimes summary can be a dict — convert to string
                summary = summary.get("value", "")

            article = {
                "title": entry.title,
                "summary": summary,
                "text": summary,  # fallback field for summarizer
                "link": entry.link,
                "source": source,
                "published": entry.get("published", ""),
            }

            # If a published date is available, use dateutil.parser to parse it
            if article['published']:
                try:
                    article['published_date'] = parser.parse(article['published'])
                    if article['published_date'].tzinfo is not None:
                        article['published_date'] = article['published_date'].replace(tzinfo=None)
                except ValueError:
                    article['published_date'] = datetime.min
            else:
                article['published_date'] = datetime.min

            # Filter articles based on the provided keywords (any match in title or summary)
            if keywords:
                searchable_text = f"{article['title']} {article['summary']}".lower()
                if any(keyword.lower() in searchable_text for keyword in keywords):
                    articles.append(article)
            else:
                articles.append(article)

    articles.sort(key=lambda x: x['published_date'], reverse=True)
    return articles
