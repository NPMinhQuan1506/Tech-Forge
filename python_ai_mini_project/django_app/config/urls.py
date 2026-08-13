"""Top-level URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from learning.forms import LoginForm
from learning.views import register_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            authentication_form=LoginForm,
            template_name="registration/login.html",
        ),
        name="login",
    ),
    path("accounts/register/", register_view, name="register"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("learning.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
