"""Учебные данные: модуль 1, без базы данных. Постеры — локальные SVG."""
MOVIES = [
    {'id': 1, 'title': 'Предел горизонта', 'genre': 'Фантастика', 'slug': 'fantastika', 'year': 2026, 'duration': 142, 'rating': 8.9, 'price': 450, 'age': '12+', 'is_new': True, 'accent': 'cyan', 'poster': 'images/poster-1.svg', 'description': 'Группа исследователей получает сигнал из области космоса, где исчезают законы времени. Экспедиция меняет их представление о Вселенной.'},
    {'id': 2, 'title': 'Тихий переулок', 'genre': 'Ужасы', 'slug': 'uzhasy', 'year': 2025, 'duration': 104, 'rating': 7.8, 'price': 350, 'age': '18+', 'is_new': False, 'accent': 'red', 'poster': 'images/poster-2.svg', 'description': 'Возвращение в родной город становится началом загадочной истории. Каждую ночь в одном переулке исчезает свет.'},
    {'id': 3, 'title': 'Письма из Парижа', 'genre': 'Мелодрама', 'slug': 'melodrama', 'year': 2026, 'duration': 116, 'rating': 8.4, 'price': 400, 'age': '12+', 'is_new': True, 'accent': 'pink', 'poster': 'images/poster-3.svg', 'description': 'Случайно перепутанные письма соединяют судьбы двух людей, живущих в разных странах.'},
    {'id': 4, 'title': 'Последний рейс', 'genre': 'Боевик', 'slug': 'boevik', 'year': 2025, 'duration': 128, 'rating': 8.1, 'price': 380, 'age': '16+', 'is_new': False, 'accent': 'orange', 'poster': 'images/poster-4.svg', 'description': 'Обычная поездка превращается в гонку со временем, когда водитель узнаёт, что его пассажир скрывает опасную тайну.'},
    {'id': 5, 'title': 'Большая перемена', 'genre': 'Комедия', 'slug': 'komediya', 'year': 2026, 'duration': 97, 'rating': 8.2, 'price': 350, 'age': '6+', 'is_new': True, 'accent': 'yellow', 'poster': 'images/poster-5.svg', 'description': 'Друзья решают открыть необычное кафе и за неделю попадают в десятки нелепых ситуаций.'},
    {'id': 6, 'title': 'Подводный мир', 'genre': 'Приключения', 'slug': 'priklyucheniya', 'year': 2024, 'duration': 111, 'rating': 8.6, 'price': 360, 'age': '6+', 'is_new': False, 'accent': 'blue', 'poster': 'images/poster-6.svg', 'description': 'Юные океанологи обнаруживают старинную карту и отправляются на поиски забытого города.'},
    {'id': 7, 'title': 'Код тишины', 'genre': 'Триллер', 'slug': 'triller', 'year': 2026, 'duration': 122, 'rating': 8.7, 'price': 430, 'age': '16+', 'is_new': True, 'accent': 'purple', 'poster': 'images/poster-7.svg', 'description': 'Эксперт по кибербезопасности замечает закономерность в городских сбоях и выходит на масштабный заговор.'},
    {'id': 8, 'title': 'Ритм улиц', 'genre': 'Драма', 'slug': 'drama', 'year': 2025, 'duration': 109, 'rating': 8.3, 'price': 370, 'age': '12+', 'is_new': False, 'accent': 'magenta', 'poster': 'images/poster-8.svg', 'description': 'Талантливая танцовщица борется за возможность выступить на большой сцене вопреки ожиданиям окружающих.'},
    {'id': 9, 'title': 'Звёздная команда', 'genre': 'Мультфильм', 'slug': 'multfilm', 'year': 2026, 'duration': 91, 'rating': 9.0, 'price': 320, 'age': '0+', 'is_new': True, 'accent': 'teal', 'poster': 'images/poster-9.svg', 'description': 'Маленькие космические путешественники спасают целую планету благодаря дружбе и находчивости.'},
    {'id': 10, 'title': 'Легенда гор', 'genre': 'Приключения', 'slug': 'priklyucheniya', 'year': 2025, 'duration': 134, 'rating': 8.8, 'price': 420, 'age': '12+', 'is_new': False, 'accent': 'green', 'poster': 'images/poster-10.svg', 'description': 'Во время путешествия по горам Кыргызстана герои находят подсказки к древнему преданию.'},
    {'id': 11, 'title': 'Неожиданный гость', 'genre': 'Комедия', 'slug': 'komediya', 'year': 2024, 'duration': 102, 'rating': 7.9, 'price': 300, 'age': '12+', 'is_new': False, 'accent': 'coral', 'poster': 'images/poster-11.svg', 'description': 'Планы семьи на спокойные выходные рушатся после визита эксцентричного родственника.'},
    {'id': 12, 'title': 'За гранью', 'genre': 'Фантастика', 'slug': 'fantastika', 'year': 2026, 'duration': 125, 'rating': 8.5, 'price': 410, 'age': '12+', 'is_new': True, 'accent': 'indigo', 'poster': 'images/poster-12.svg', 'description': 'Учёная создаёт устройство, позволяющее заглядывать в альтернативные варианты будущего.'},
]

def search_movies(movies, query):
    query = query.strip().casefold()
    return [movie for movie in movies if query in movie['title'].casefold() or query in movie['description'].casefold()]

def filter_by_genre(movies, slug):
    return [movie for movie in movies if movie['slug'] == slug]

def genre_counts(movies):
    counts = {}
    for movie in movies:
        key = (movie['slug'], movie['genre'])
        counts[key] = counts.get(key, 0) + 1
    return [{'slug': slug, 'name': name, 'count': count} for (slug, name), count in sorted(counts.items(), key=lambda x: x[0][1])]
