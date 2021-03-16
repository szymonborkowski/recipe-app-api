# used to ONLY add the list model function:
from rest_framework import viewsets, mixins

# token authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()  # this gets all of the tags
    # therefore we override it to filter to only authenticated tags below
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated use only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
