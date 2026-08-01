from apps.common.permissions import ReadOnlyOrSuperAdmin
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Category, Service
from ..selectors import list_categories, list_services
from ..serializers import ServiceAliasSerializer, CategorySerializer, ServiceSerializer

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)
@extend_schema_view(list=extend_schema(tags=["Catalog"]), retrieve=extend_schema(tags=["Catalog"]))
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrSuperAdmin]
    queryset = Category.objects.all()

    def get_queryset(self):
        return list_categories()

@extend_schema_view(
    list=extend_schema(
        tags=["Catalog"],
        parameters=[
            OpenApiParameter(
                name="category_id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                description="Filter services by category ID",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search service by name",
            ),
        ],
    ),
    retrieve=extend_schema(tags=["Catalog"]),
)
class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]
    queryset = Service.objects.all()

    def get_queryset(self):
        return list_services(
            category_id=self.request.query_params.get("category_id"),
            search=self.request.query_params.get("search", ""),
        )