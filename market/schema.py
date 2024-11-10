import graphene
from graphene import Schema
from graphene_django import DjangoObjectType

from core.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    get_product = graphene.List(ProductType)

    def resolve_get_product(self, info):
        return Product.objects.all()


schema = Schema(query=Query)
