from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Product
from app.pagination import CustomPagination
from app.serializers.product import ProductDetailSerializer


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(initial_consonant__icontains=search)
            )

        return queryset
