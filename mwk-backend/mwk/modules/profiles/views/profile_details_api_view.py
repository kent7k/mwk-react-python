from rest_framework.generics import RetrieveAPIView
from mwk.modules.profiles.serializers.profile import ProfileSerializer


class ProfileDetailsView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.profile)
        return self.request.user.profile

