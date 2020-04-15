from djangorestframework_camel_case.settings import api_settings

from djangorestframework_camel_case.util import camel_to_underscore
from rest_framework.filters import OrderingFilter
from django.db.models.sql.constants import ORDER_PATTERN


class CamelCaseOrderingFilter(OrderingFilter):
    """
    This filter basically transforms any camelCase field to a snake_case field and overrides the DRF OrderingFilter
    """

    def remove_invalid_fields(self, queryset, fields, view, request):
        underscorized_fields = [camel_to_underscore(field, **api_settings.JSON_UNDERSCOREIZE) for field in fields]
        valid_fields = [item[0] for item in self.get_valid_fields(queryset, view, {'request': request})]
        return [term for term in underscorized_fields if term.lstrip('-') in valid_fields and ORDER_PATTERN.match(term)]
