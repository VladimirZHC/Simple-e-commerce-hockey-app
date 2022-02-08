import sys
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

from io import BytesIO

User = get_user_model()




class MinResolutionError(Exception):
    pass


class MaxResolutionError(Exception):
    pass





class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name


class Product(models.Model):


    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (4000, 4000)
    MAX_Img_Size = 3145728

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    Age = models.CharField(max_length=255, verbose_name='Возраст', null=True, blank=True)

    Flex = models.IntegerField(verbose_name='Жесткость клюшки', null=True, blank=True)
    Material = models.CharField(max_length=255, verbose_name='Материал', null=True, blank=True)
    Curvature = models.CharField(max_length=255, verbose_name='Загиб клюшки', null=True, blank=True)
    Weight = models.FloatField(verbose_name='Масса', null=True, blank=True)

    Fullness = models.CharField(max_length=255, verbose_name='Полнота коньков', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        pic = new_img.resize((200, 200), Image.ANTIALIAS)
        filestream = BytesIO()
        pic.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})




class CartProduct(models.Model):
    user = models.ForeignKey('Custumer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveBigIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Custumer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveBigIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



class Custumer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    status_new = 'new'
    status_in_progress = 'in_progress'
    status_ready = 'is_ready'
    status_completed = 'completed'

    buying_type_self = 'self'
    buying_type_delivery = 'delivery'

    STATUS_CHOICES = (
        (status_new, 'Новый заказ'),
        (status_in_progress, 'Заказ в обработке'),
        (status_ready, 'Заказ готов'),
        (status_completed, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (buying_type_self, 'Самовывоз'),
        (buying_type_delivery, 'Доставка')
    )

    customer = models.ForeignKey(Custumer, verbose_name='Покупатель', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=status_new)
    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=buying_type_self)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
