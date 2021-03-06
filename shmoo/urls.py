from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'articles.views.display_article', name="articles_display_article"),
    url(r'^blog/', include('articles.urls')),
    (r'^about/$', 'shmoo.views.about'),
    (r'^contact/$', 'shmoo.views.contact'),
    (r'^gallery/$', 'shmoo.views.gallery'),
    (r'^projects/$', 'shmoo.views.projects'),
    (r'^n/$', 'shmoo.views.can'),
    url(r'^admin/', include(admin.site.urls)),
)
