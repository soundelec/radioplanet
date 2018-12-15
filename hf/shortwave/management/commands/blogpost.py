# blogpost.py - get the latest five posts from the blog and stick them in Django's database

from django.core.management.base import BaseCommand, CommandError
from shortwave.models import BlogPost
import feedparser

b = feedparser.parse('https://blog.radiopla.net/feed/')
posts = BlogPost.objects.all()

class Command(BaseCommand):
    help = 'Retrieves blog posts and adds them to BlogPost model'

    def handle(self, *args, **options):
        for post in b.entries:
            title = post.title
            link = post.link
            if posts.filter(link=link).exists():
                pass
            else:
                BlogPost.objects.create(title=title, link=link)
                print("added blog post", title)
