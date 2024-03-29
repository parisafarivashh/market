from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        db_table = 'SubCategory'
        verbose_name_plural = 'sub categories'


class Product(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    description = models.JSONField(blank=True, null=True)
    rank = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='seller')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', verbose_name='sub categories')

    class Meta:
        db_table = 'Product'
        verbose_name_plural = 'products'


class Color(models.Model):
    code = models.CharField(max_length=20, blank=False, null=False, verbose_name='code of color')
    name = models.CharField(max_length=20, blank=False, null=False, verbose_name='name')

    class Meta:
        db_table = 'Color'
        verbose_name_plural = 'color'


class Detail(models.Model):

    class Size(models.IntegerChoices):
        MEDIUM = 1, _('M')
        LARGE = 2, _('L')
        XLARG = 3, _('XL')
        XXLARG = 4, _('XXL')
        XXXLARG = 5, _('XXXL')

    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='color')
    size = models.IntegerField(choices=Size.choices, default=Size.MEDIUM)
    price = models.FloatField(blank=False, null=False)
    count = models.IntegerField(blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product', related_name='details')

    class Meta:
        db_table = 'Detail'
        verbose_name_plural = 'details of product'

