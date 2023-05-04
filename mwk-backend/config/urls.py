from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Admin password reset URL patterns
password_reset_patterns = [
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]

# Documentation URL patterns
documentation_patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='docs_schema'),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='docs_schema'),
        name='docs_swagger-ui',
    ),
]

# Main URL patterns
urlpatterns = [
    # Admin password reset
    path('admin/', include(password_reset_patterns)),
    # Admin
    path('admin/', admin.site.urls),
    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    # Apps
    path("", include('mwk.modules.authentication.urls')),
    path('feed/', include('mwk.modules.main.urls')),
    path('peoples/', include('mwk.modules.profiles.urls')),
    # Documentation
    path('docs/', include(documentation_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
