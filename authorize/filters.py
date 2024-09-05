from datetime import datetime, timedelta, UTC

import django_filters as filters

from .models import User


class FilterUser(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    phone_number = filters.NumberFilter(field_name='phone_number', lookup_expr='exact')
    is_staff = filters.BooleanFilter(field_name='is_staff')
    hours = filters.NumberFilter(field_name='date_joined', method='get_past_n_hours')


    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        filter = super(FilterUser, cls).filter_for_field(f, name, lookup_expr)
        filter.extra['help_text'] = f.help_text
        return filter

    def get_past_n_hours(self, queryset, field_name, value):
        time_threshold = \
            datetime.now(tz=UTC) - timedelta(hours=int(value))
        return queryset.filter(date_joined__gte=time_threshold)


    class Meta:
        model = User
        fields = ['title', 'first_name', 'last_name', 'phone_number', 'is_staff']

