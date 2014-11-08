from django.conf import settings
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from articles.models import Article, Tag

SITE = Site.objects.get_current()

FEED_TIMEOUT = getattr(settings, 'ARTICLE_FEED_TIMEOUT', 0)

class LatestEntries(Feed):
    link = "http://ahal.ca/blog"

    def title(self):
        return "%s Articles" % SITE.name

    def items(self):
        key = 'latest_articles'
        articles = cache.get(key)

        if articles is None:
            articles = list(Article.objects.live().order_by('-publish_date')[:15])
            cache.set(key, articles, FEED_TIMEOUT)

        return articles

    def item_author_name(self, item):
        return item.author.username

    def item_tags(self, item):
        return [c.name for c in item.tags.all()] + [keyword.strip() for keyword in item.keywords.split(',')]

    def item_pubdate(self, item):
        return item.publish_date

    def item_description(self, item):
        return render_to_string('feeds/latest_description.html', { 'obj': item })

class TagFeed(Feed):
    def get_object(self, bits, **kwargs):
        tag = kwargs.get('tag', None)
        if not tag:
            raise FeedDoesNotExist

        return Tag.objects.get(name__iexact=tag)

    def title(self, obj):
        return "%s: Newest Articles Tagged '%s'" % (SITE.name, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Articles Tagged '%s'" % obj.name

    def items(self, obj):
        return self.item_set(obj)[:10]

    def item_set(self, obj):
        key = 'articles_for_%s' % obj.name
        articles = cache.get(key)

        if articles is None:
            articles = list(obj.article_set.live().order_by('-publish_date'))
            cache.set(key, articles, FEED_TIMEOUT)

        return articles

    def item_author_name(self, item):
        return item.author.username

    def item_author_link(self, item):
        return reverse('articles_by_author', args=[item.author.username])

    def item_pubdate(self, item):
        return item.publish_date

    def item_description(self, item):
        return render_to_string('feeds/tags_description.html', { 'obj': item })

