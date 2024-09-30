from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Client(models.Model):
    name = models.TextField("ФИО")
    password = models.TextField("Пароль")
    email = models.TextField("Почта")
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    
    def __str__(self) -> str:
        return self.name
    

class Orders(models.Model):
    address = models.TextField("Адрес")
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True) 
    sum = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    status = models.TextField("Статус")
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Product(models.Model):
    name = models.TextField("Название")
    cost = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Статус")
    amount = models.IntegerField("Количество")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True) 
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Category(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class ShoppingCart(models.Model):
    sum = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class ProductShoppingCart(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)
    shoppingCart = models.ForeignKey("ShoppingCart", on_delete=models.CASCADE, null=True)

class OrderProduct(models.Model):
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)

class Review(models.Model):
    text = models.TextField("Текст")
    rating = models.IntegerField(
        "Оценка", 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
