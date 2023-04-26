from django.urls import path

from mwk.modules.profiles.views.profile_api_view import ProfileListView
from mwk.modules.profiles.views.profile_detail_api_view import ProfileDetailView
from mwk.modules.profiles.views.profile_details_api_view import ProfileDetailsView

urlpatterns = [
    path("", ProfileListView.as_view(), name='profiles'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('me/', ProfileDetailsView.as_view(), name='profile_details'),
]
