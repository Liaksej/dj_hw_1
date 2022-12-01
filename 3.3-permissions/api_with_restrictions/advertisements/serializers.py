from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at')
        read_only_fields = ["creator"]

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Метод для обновления"""

        validated_data["creator"] = self.context["request"].user
        return super().update(instance, validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        counting = Advertisement.objects.all().select_related('creator').filter(creator=self.context["request"].user,
                                                                                status='OPEN').count()
        if counting > 10 and (self.context['request'].stream.method == 'POST' or ('status' in data
                                                                                  and data['status'] == "OPEN")):
            raise ValidationError('Количество открытых объявлений превысило максимальное значение')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('favorite', 'advertisement', 'user')

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["user"] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании."""

        check_fav_existing = Favorite.objects.all().filter(user=self.context["request"].user,
                                                           advertisement=data['advertisement'].id)
        owner = data['advertisement'].creator
        if check_fav_existing:
            raise ValidationError('Уже добавлено в избранное ранее')
        if owner == self.context["request"].user:
            raise ValidationError('Вы не можете добавить в избранное свое объявление')
        return data


class AdvertisementFilter(filters.FilterSet):
    """Определения полей фильтрации."""

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ('creator', 'created_at', 'status')
