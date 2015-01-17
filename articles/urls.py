from django.conf.urls import patterns, url
from articles.feeds import TagFeed, LatestEntries
from articles import views

urlpatterns = patterns('',
    (r'^(?P<year>\d{4})/(?P<month>.{3})/(?P<day>\d{1,2})/(?P<slug>.*)/$', views.redirect_to_article),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_in_month_page'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.display_blog_page, name='articles_in_month'),
)

urlpatterns += patterns('',
    url(r'^$', views.display_article, name='articles_display_article'),
    url(r'^page/(?P<page>\d+)/$', views.display_blog_page, name='articles_archive_page'),

    url(r'^tag/(?P<tag>.*)/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_display_tag_page'),
    url(r'^tag/(?P<tag>.*)/$', views.display_blog_page, name='articles_display_tag'),

    url(r'^author/(?P<username>.*)/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_by_author_page'),
    url(r'^author/(?P<username>.*)/$', views.display_blog_page, name='articles_by_author'),

    url(r'^(?P<year>\d{4})/(?P<slug>.*)/$', views.display_article, name='articles_display_article'),
    url(r'^draft/(?P<year>\d{4})/(?P<slug>.*)/$', views.display_article, {'draft': True}),

    # AJAX
    url(r'^ajax/tag/autocomplete/$', views.ajax_tag_autocomplete, name='articles_tag_autocomplete'),

    # RSS
    url(r'^feeds/latest.rss$', LatestEntries(), name='articles_feed'),
    url(r'^feeds/tags/(?P<tag>.*)/$', TagFeed(), name='tag_feed'),
)
