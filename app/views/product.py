from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Product
from app.pagination import CustomPagination
from app.serializers.product import ProductDetailSerializer


@extend_schema_view(
    list=extend_schema(
        summary="'상품' 리스트 열람.",
        parameters=[
            OpenApiParameter("search", description="상품 검색어", type=OpenApiTypes.STR)
        ],
    ),
    retrieve=extend_schema(summary="특정 '상품' 열람."),
    create=extend_schema(summary="특정 '상품' 생성"),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(summary="특정 '상품' 부분 수정"),
    destroy=extend_schema(summary="특정 '상품' 삭제."),
)
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
