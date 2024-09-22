from django.db import models

class Client(models.Model):
    name = models.TextField("ФИО")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    
    def __str__(self) -> str:
        return self.name
    

class Orders(models.Model):
    address = models.TextField("Адрес")
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True) 

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
