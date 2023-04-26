from rest_framework.generics import RetrieveAPIView, ListAPIView
from mwk.modules.profiles.serializers.profile import ProfileSerializer
from mwk.modules.profiles.services import get_profiles


class ProfileDetailView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = get_profiles()
