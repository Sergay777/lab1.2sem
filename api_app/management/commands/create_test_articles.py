from django.core.management.base import BaseCommand
from api_app.models import Category, Women


class Command(BaseCommand):
    help = 'Создаёт тестовые статьи'

    def handle(self, *args, **options):
        # Создаём категории
        categories = []
        for name in ['Спорт', 'Наука', 'Кино', 'Музыка', 'Путешествия']:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)
        
        # Создаём статьи
        articles = [
            ('Футбол', 'Новости футбола', categories[0]),
            ('Хоккей', 'Новости хоккея', categories[0]),
            ('Физика', 'Законы физики', categories[1]),
            ('Химия', 'Химические элементы', categories[1]),
            ('Новый фильм', 'Премьера месяца', categories[2]),
            ('Сериал', 'Новый сезон', categories[2]),
            ('Концерт', 'Выступление группы', categories[3]),
            ('Альбом', 'Новый альбом', categories[3]),
            ('Отпуск', 'Куда поехать', categories[4]),
            ('Отель', 'Лучшие отели', categories[4]),
        ]
        
        for title, content, cat in articles:
            Women.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'cat': cat,
                    'is_published': True
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(articles)} статей'))
