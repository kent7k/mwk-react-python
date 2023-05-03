from rest_framework.generics import ListAPIView
from mwk.modules.profiles.serializers.profile import ProfileSerializer
from mwk.modules.profiles.services.get_profiles import get_profiles


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return get_profiles()
