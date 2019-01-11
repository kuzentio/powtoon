from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Powtoon


class PowtoonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Powtoon
        fields = ('id', 'name', 'content')
        read_only_fields = ('id', )

    def create(self, validated_data):
        if self.context:
            validated_data.update({'user': self.context['user']})

        return super().create(validated_data)


class PowtoonSharedSerializer(PowtoonSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Powtoon
        fields = ('id', 'shared_with', )
        read_only_fields = ('id', )

    def update(self, instance, validated_data):
        for user in validated_data['shared_with']:
            instance.shared_with.add(user)

        return instance
