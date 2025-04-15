# blog/utils.py

from eventregistry import *
from django.conf import settings
from .models import BlogPost
from django.utils.dateparse import parse_datetime

def fetch_articles_and_create_posts():
    er = EventRegistry(apiKey=settings.EVENT_REGISTRY_API_KEY, allowUseOfArchive=False)

    # Get South Africa URI
    sa_uri = er.getLocationUri("South Africa")

    # Trending articles in SA — last 30 days, ordered by social media shares
    q = QueryArticlesIter(
        sourceLocationUri=sa_uri,
        dataType=["news"],
        isDuplicateFilter="skipDuplicates"
    )

    for art in q.execQuery(er, sortBy="socialScore", maxItems=10):
        title = art.get('title', 'No Title')
        content = art.get('body', 'No content available.')
        source_url = art.get('url', '#')
        published_at = parse_datetime(art.get('dateTime'))
        image_url = art.get('image', '')  # fetch image URL
       

        # Prevent duplicates
        if not BlogPost.objects.filter(title=title).exists():
            BlogPost.objects.create(
                title=title,
                content=content,
                source_url=source_url,
                published_at=published_at,
                 image_url=image_url
            )
