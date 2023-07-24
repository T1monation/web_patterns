from django.db import models
from mainapp.models import Phone
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='покупатель',
                             on_delete=models.PROTECT)


class OrderItem(models.Model):
    phone = models.ForeignKey(Phone,
                              on_delete=models.PROTECT,
                              verbose_name='смартфон')
    count = models.PositiveSmallIntegerField(verbose_name='количество')
    order = models.ForeignKey(Order,
                              on_delete=models.PROTECT,
                              verbose_name='заказ')
