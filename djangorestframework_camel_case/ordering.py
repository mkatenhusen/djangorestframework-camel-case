from djangorestframework_camel_case.settings import api_settings

from djangorestframework_camel_case.util import camel_to_underscore
from rest_framework.filters import OrderingFilter
from django.db.models.sql.constants import ORDER_PATTERN
from django.db.models import F


class CamelCaseOrderingFilter(OrderingFilter):
    """
    This filter basically transforms any camelCase field to a snake_case field and overrides the DRF OrderingFilter
    """

    def remove_invalid_fields(self, queryset, fields, view, request):
        underscorized_fields = [camel_to_underscore(field, **api_settings.JSON_UNDERSCOREIZE) for field in fields]
        valid_fields = [item[0] for item in self.get_valid_fields(queryset, view, {'request': request})]
        return [term for term in underscorized_fields if term.lstrip('-') in valid_fields and ORDER_PATTERN.match(term)]


class AdvancedCamelCaseOrderingFilter(CamelCaseOrderingFilter):

    def apply_ordering_fields(self, ordering: tuple):
        return (F(ordering_field_item[1:]).desc(nulls_last=api_settings.ADVANCED_ORDERING.get("descending_nulls_last"))
                if ordering_field_item.startswith("-")
                else F(ordering_field_item).asc(nulls_last=api_settings.ADVANCED_ORDERING.get("ascending_nulls_last"))
                for ordering_field_item in ordering
                )

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            return queryset.order_by(*self.apply_ordering_fields(ordering))

        return queryset
