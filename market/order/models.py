from django.db import models, transaction
from django.db.models import Q

from user.models import User
from product.models import Detail


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    @property
    def final_cost(self):
        cost = 0
        for item in self.items.all():
            cost += item.cost
        return cost


class ItemOrderManager(models.Manager):
    def create(self,  **kwargs):
        detail = kwargs.get('detail', None)
        order = kwargs.get('order', None)
        count = kwargs.get('count', None)

        price = detail.price
        with transaction.atomic():
            item_object = super().filter(detail_id=detail.id)
            print(item_object)
            if len(item_object) == 0:
                item = super().create(price=price, detail=detail, order=order, count=count)
                final_count = count
            else:
                item = item_object.first()
                final_count = 1
                item.count += final_count
                # item.save(update_filed=['count'])

            detail.count = detail.count - final_count
            if detail.count < 0:
                raise ValueError('order number not available')
            detail.save(update_filed=['count'])

            return item


class ItemOrder(models.Model):
    price = models.FloatField()
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    count = models.IntegerField()

    # objects = ItemOrderManager()

    class Meta:
        db_table = 'ItemOrder'


    @property
    def cost(self):
        return self.price * self.count

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        super(ItemOrder, self).delete(*args, **kwargs)
        self.detail.count += self.count
        self.detail.save()

