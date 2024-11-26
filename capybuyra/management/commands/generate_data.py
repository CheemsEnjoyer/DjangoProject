from django.core.management.base import BaseCommand

from faker import Faker
import random
from capybuyra.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = [
            "Электроника", "Одежда", "Книги", "Игрушки",
            "Мебель", "Кухонные принадлежности", "Техника",
            "Автозапчасти", "Косметика", "Продукты питания"
        ]
        for _ in range(10):
            Category.objects.create(
                name=random.choice(categories)
            )
