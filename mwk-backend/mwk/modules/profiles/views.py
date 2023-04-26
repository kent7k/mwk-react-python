from rest_framework.generics import RetrieveAPIView, ListAPIView
from mwk.modules.profiles.serializers.profile import ProfileSerializer
from mwk.modules.profiles.services import get_profiles


class ProfileDetailAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = get_profiles()


class ProfileAPIView(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = get_profiles()


class ProfileDetailsAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        obj = self.request.user.profile
        self.check_object_permissions(self.request, obj)
        return obj
