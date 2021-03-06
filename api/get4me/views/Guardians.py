from rest_framework import viewsets, permissions
from get4me.models import GuardiansModel
from get4me.serializers import GuardiansSerializer

class GuardiansView(viewsets.ModelViewSet):

    queryset = GuardiansModel.objects.all()
    serializer_class = GuardiansSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return GuardiansModel.objects.all()
        return GuardiansModel.objects.filter(user__username=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.action == 'create':
            self.permission_classes = [permissions.AllowAny]

        return super(GuardiansView, self).get_permissions()
