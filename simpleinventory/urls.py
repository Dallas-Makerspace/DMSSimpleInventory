from django.conf.urls import patterns, include, url

from inventory import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simpleinventory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^bins/$', views.BinListView.as_view()),
    url(r'^bins/page(?P<page>[0-9]+)/$', views.BinListView.as_view()),
    url(r'^bins/(?P<pk>[0-9]+)/$', views.BinDetailView.as_view()),
    url(r'^bins/(?P<pk>[0-9]+)/add$', views.add_inventory, name='add_inventory'),
    url(r'^parts/(?P<pk>[0-9]+)/$', views.PartDetailView.as_view()),
    url(r'^add_part/', views.PartCreate.as_view(), name='add_part'),
    url(r'^search/$', views.search, name='search'),
    url(r'^export/$', views.export, name='export'),
    url(r'^import/$', views.import_view, name='import')
    
)
