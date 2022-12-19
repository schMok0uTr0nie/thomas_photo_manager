
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from thomas import settings
from .views import *

urlpatterns = [
    path('', FeedView.as_view(), name="feed"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),

    path('<str:nick>', show_profile, name="profile"),
    path('<str:nick>/edit_profile', EditProfileView.as_view(), name="edit_profile"),

    path('<str:nick>/portfolio', show_portfolio, name="portfolio"),
    path('snap/<int:pk>', show_snap, name="show_snap"),

    path('snap/upload', UploadSnapView.as_view(), name="upload_snap"),
    path('snap/<int:pk>/delete', delete_snap, name="delete_snap"),
    path('snap/<int:pk>/edit', edit_snap, name="edit_snap"),

    path('<str:nick>/subs', show_subs, name="subs"),
    path('cat/all', show_cats, name="cats"),
    path('cat/<slug:cat_slug>', show_cats, name="show_cat"),

    path('subscribe/<str:nick>', subscribe_pro, name="subscribe_pro"),
    path('unsubscribe/<str:nick>', unsubscribe_pro, name="unsubscribe_pro"),

    path('subscribe/<slug:cat_slug>', subscribe_cat, name="subscribe_cat"),
    path('unsubscribe/<slug:cat_slug>', unsubscribe_cat, name="unsubscribe_cat"),

    path('search/', SearchView.as_view(), name='search')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
