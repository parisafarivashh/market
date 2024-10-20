import django_filters

from .models.cart import Cart


class CartFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')

    class Meta:
        model = Cart
        fields = ['start_date', 'end_date', 'status']

