from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        first_name = self.user.first_name or ''
        last_name = self.user.last_name or ''
        username = self.user.username or ''

        display_name = f"{first_name} {last_name} ({username})".strip()

        return display_name


class Orders(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Оформлен'),
        ('assembling', 'Собирается'),
        ('in_transit', 'В пути'),
        ('arrived', 'Прибыл в пункт доставки'),
        ('picked_up', 'Забран'),
    ]
    address = models.TextField("Адрес")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    sum = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='ordered')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Category(models.Model):
    name = models.TextField("Название")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    name = models.TextField("Название")
    cost = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Статус")
    amount = models.IntegerField("Количество")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="products")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def calculate_total(self):
        return sum(
            item.product.cost * item.quantity for item in self.productshoppingcart_set.all()
        )

class ProductShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, null=True, related_name="items")
    quantity = models.PositiveIntegerField("Количество", default=1)


class OrderProduct(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

class Review(models.Model):
    text = models.TextField("Текст")
    rating = models.IntegerField(
        "Оценка", 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

