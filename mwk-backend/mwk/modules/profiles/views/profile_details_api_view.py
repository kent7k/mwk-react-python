from rest_framework.generics import RetrieveAPIView, ListAPIView
from mwk.modules.profiles.serializers.profile import ProfileSerializer


class ProfileDetailsView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        obj = self.request.user.profile
        self.check_object_permissions(self.request, obj)
        return obj
