from django.urls import path

from mwk.modules.authentication.views.check_token_view import TokenCheckAPIView
from mwk.modules.authentication.views.user_activate_view import UserActivateAPIView
from mwk.modules.authentication.views.user_login_view import UserLoginAPIView
from mwk.modules.authentication.views.user_logout_all_view import UserLogoutAllAPIView
from mwk.modules.authentication.views.user_logout_view import UserLogoutAPIView
from mwk.modules.authentication.views.user_register_view import UserRegisterAPIView


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='reg'),
    path('confirm/<str:uid>/<str:token>/', UserActivateAPIView.as_view(), name='activate'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('logoutall/', UserLogoutAllAPIView.as_view(), name='logout_all'),
    path('check-token/', TokenCheckAPIView.as_view(), name='check_token'),
]
