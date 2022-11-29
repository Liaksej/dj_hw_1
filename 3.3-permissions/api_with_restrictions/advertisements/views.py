from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerForFavorite, IsOwner
from advertisements.serializers import AdvertisementSerializer, AdvertisementFilter, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        """Получение выборки за исключением чужих драфтов."""

        if not self.request.user.id:
            return Advertisement.objects.all().exclude(status='DRAFT')
        return Advertisement.objects.all().exclude(
            status='DRAFT', creator_id__lt=self.request.user.id).exclude(
            status='DRAFT', creator_id__gt=self.request.user.id)

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return [IsAuthenticated(), IsAdminUser()]
            else:
                return [IsAuthenticated(), IsOwner()]
        return []


class FavoriteViewSet(ModelViewSet):
    """ViewSet для избранного."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_permissions(self):
        """Получение прав для действий."""

        return [IsAuthenticated(), IsOwnerForFavorite()]

    def get_queryset(self):
        """Получение выборки для конкретного юзера."""

        return Favorite.objects.all().filter(user=self.request.user)
