import django_filters

from .models import Product, Category
from .models.cart import Cart
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, \
    SearchQuery, SearchRank


class BaseSearchFilter(django_filters.FilterSet):

    def search_title(self, queryset, name, value):
        score = 0.015

        vector = SearchVector(name)
        search_query = SearchQuery(value)

        _queryset = queryset.annotate(score=SearchRank(vector, search_query)) \
            .filter(score__gte=score) \
            .order_by('-score')

        if not _queryset.exists():
            _queryset = queryset \
                .annotate(similarity=TrigramSimilarity(name, value)) \
                .filter(similarity__gte=score)

        return _queryset


class CartFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')

    class Meta:
        model = Cart
        fields = ['start_date', 'end_date', 'status']


class ProductFilter(BaseSearchFilter):
    title = django_filters.CharFilter(field_name='title', method='search_title')

    class Meta:
        model = Product
        fields = ['title']


class CategoryFilter(BaseSearchFilter):
    title = django_filters.CharFilter(field_name='title', method='search_title')

    class Meta:
        model = Category
        fields = ['title']

