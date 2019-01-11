from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Powtoon
from api.permissions import IsPowtoonOwnerOrAdmin
from api.serializers import PowtoonSerializer, PowtoonSharedSerializer


class PowtoonViewSet(viewsets.ModelViewSet):
    queryset = Powtoon.objects.all()
    serializer_class = PowtoonSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticated, IsPowtoonOwnerOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.has_perm('api.can_see'):
            qs = qs.filter(
                Q(shared_with__in=[self.request.user, ]) | Q(user=self.request.user)
            )

        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class PowtoonSharedViewSet(viewsets.ModelViewSet):
    queryset = Powtoon.objects.all()
    serializer_class = PowtoonSharedSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [
        IsAuthenticated,
        IsPowtoonOwnerOrAdmin
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.has_perm('api.can_share'):
            qs = qs.filter(
                Q(shared_with__in=[self.request.user, ]) | Q(user=self.request.user)
            )

        return qs
