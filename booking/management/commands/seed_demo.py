from datetime import timedelta,date,datetime,time
from urllib.parse import quote_plus
from django.core.management.base import BaseCommand
from django.utils import timezone
from movies.models import Movie,Genre
from booking.models import Cinema,Hall,Showtime

MOVIES=[
('Дюна: Часть вторая','Dune: Part Two','sci-fi',2024,166,'8.5','Тимоти Шаламе, Зендея, Ребекка Фергюсон','Дени Вильнёв','Пол Атрейдес объединяется с фременами, чтобы изменить судьбу Арракиса.','https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg',False,None),
('Интерстеллар','Interstellar','sci-fi',2014,169,'8.7','Мэттью Макконахи, Энн Хэтэуэй, Джессика Честейн','Кристофер Нолан','Группа исследователей отправляется за пределы Солнечной системы в поисках нового дома для человечества.','https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',False,None),
('Головоломка 2','Inside Out 2','animation',2024,96,'7.6','Эми Полер, Майя Хоук, Филлис Смит (озвучка)','Келси Манн','Райли взрослеет, и в её голове появляются новые эмоции.','https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg',False,None),
('Барби','Barbie','comedy',2023,114,'7.0','Марго Робби, Райан Гослинг, Америка Феррера','Грета Гервиг','Барби отправляется в реальный мир, чтобы понять, что значит быть собой.','https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg',False,None),
('Дэдпул и Росомаха','Deadpool & Wolverine','action',2024,127,'7.5','Райан Рейнольдс, Хью Джекман, Эмма Коррин','Шон Леви','Дэдпул объединяется с Росомахой для опасного путешествия по мультивселенной.','https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg',False,None),
('Холодное сердце 2','Frozen II','animation',2019,103,'7.2','Кристен Белл, Идина Мензел, Джош Гэд (озвучка)','Крис Бак, Дженнифер Ли','Эльза и Анна отправляются на поиски разгадки прошлого Эренделла.','https://image.tmdb.org/t/p/w500/mINJaa34MtknCYl5AjtNJzWj8cD.jpg',False,None),
('Начало','Inception','sci-fi',2010,148,'8.8','Леонардо Ди Каприо, Джозеф Гордон-Левитт, Эллиот Пейдж','Кристофер Нолан','Профессиональный вор проникает в чужие сны, чтобы внедрить идею.','https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg',False,None),
('Оппенгеймер','Oppenheimer','drama',2023,180,'8.3','Киллиан Мёрфи, Эмили Блант, Роберт Дауни-младший','Кристофер Нолан','Биографическая драма о создателе атомной бомбы.','https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg',False,None),
('Холодное сердце 3','Frozen III','animation',2027,100,'0.0','Кристен Белл, Идина Мензел, Джош Гэд (английская озвучка)','Дженнифер Ли, Трент Корри','Анна, Эльза и Олаф возвращаются в новую сказочную историю. Продолжительность пока неизвестна: 100 минут — заглушка для демонстрации.','',True,date(2027,11,24)),
('Суперсемейка 3','Incredibles 3','animation',2028,100,'0.0','Актёрский состав уточняется','Питер Сон','Продолжение истории семьи супергероев. Продолжительность и дата здесь предварительные, уточняйте у студии.','',True,None),
('Тайна Коко 2','Coco 2','animation',2029,100,'0.0','Актёрский состав уточняется','Режиссёр уточняется','Анонсированное продолжение мультфильма Pixar. Продолжительность предварительная.','',True,None),
('Аватар: Путь воды','Avatar: The Way of Water','sci-fi',2022,192,'7.6','Сэм Уортингтон, Зои Салдана, Сигурни Уивер','Джеймс Кэмерон','Джейк Салли и его семья исследуют океаны Пандоры и защищают свой дом.','https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg',False,None),
('Человек-паук: Через вселенные','Spider-Man: Into the Spider-Verse','animation',2018,117,'8.4','Шамеик Мур, Джейк Джонсон, Хейли Стайнфелд','Боб Персичетти, Питер Рэмзи, Родни Ротман','Майлз Моралес открывает мультивселенную и учится быть Человеком-пауком.','https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg',False,None),
('Гарри Поттер и философский камень','Harry Potter and the Philosopher’s Stone','fantasy',2001,152,'7.6','Дэниел Рэдклифф, Эмма Уотсон, Руперт Гринт','Крис Коламбус','Одиннадцатилетний Гарри узнаёт, что он волшебник, и попадает в Хогвартс.','https://image.tmdb.org/t/p/w500/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg',False,None),
('Тёмный рыцарь','The Dark Knight','action',2008,152,'9.0','Кристиан Бейл, Хит Леджер, Аарон Экхарт','Кристофер Нолан','Бэтмен вступает в противостояние с Джокером, ставящим Готэм на грань хаоса.','https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',False,None),
('Джокер','Joker','drama',2019,122,'8.4','Хоакин Феникс, Роберт Де Ниро, Зази Битц','Тодд Филлипс','История Артура Флека, который постепенно превращается в Джокера.','https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg',False,None),
('ВАЛЛ-И','WALL·E','animation',2008,98,'8.4','Бен Бёртт, Элисса Найт, Джефф Гарлин (озвучка)','Эндрю Стэнтон','Маленький робот обнаруживает новое предназначение среди заброшенных вещей на Земле.','https://image.tmdb.org/t/p/w500/hbhFnRzzg6ZDmm8YAmxBnQpQIPh.jpg',False,None),
('Кунг-фу Панда 4','Kung Fu Panda 4','animation',2024,94,'6.3','Джек Блэк, Аквафина, Виола Дэвис (озвучка)','Майк Митчелл','По должен выбрать преемника и встретиться с новым опасным противником.','https://image.tmdb.org/t/p/w500/kDp1vUBnMpe8ak4rjgl3cLELqjU.jpg',False,None),
('Веном: Последний танец','Venom: The Last Dance','action',2024,109,'6.0','Том Харди, Чиветел Эджиофор, Джуно Темпл','Келли Марсел','Эдди и Веном скрываются от преследователей в финальной главе истории.','https://image.tmdb.org/t/p/w500/aosm8NMQ3UyoBVpSxyimorCQykC.jpg',False,None),
('Гладиатор II','Gladiator II','drama',2024,148,'6.5','Пол Мескал, Педро Паскаль, Дензел Вашингтон','Ридли Скотт','Луций оказывается на арене Колизея и ищет путь к свободе.','https://image.tmdb.org/t/p/w500/2cxhvwyEwRlysAmRH4iodkvo0z5.jpg',False,None),
('Как приручить дракона','How to Train Your Dragon','animation',2010,98,'8.1','Джей Барушель, Джерард Батлер, Америка Феррера (озвучка)','Крис Сандерс, Дин ДеБлуа','Юный викинг знакомится с драконом, который меняет его представление о мире.','https://image.tmdb.org/t/p/w500/ygGmAO60t8GyqUo9xYeYxSZAR3b.jpg',False,None),
('Стражи Галактики. Часть 3','Guardians of the Galaxy Vol. 3','sci-fi',2023,150,'7.9','Крис Пратт, Зои Салдана, Дэйв Батиста','Джеймс Ганн','Команда друзей отправляется на новую миссию, чтобы спасти одного из своих.','https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg',False,None),
('Бедные-несчастные','Poor Things','drama',2023,141,'7.4','Эмма Стоун, Марк Руффало, Уиллем Дефо','Йоргос Лантимос','Фантастическая история женщины, которая заново открывает мир.','https://image.tmdb.org/t/p/w500/kQs6keheMwCxJxrzV83VUwFtHkB.jpg',False,None),
('Кот в сапогах 2: Последнее желание','Puss in Boots: The Last Wish','animation',2022,102,'7.8','Антонио Бандерас, Сальма Хайек, Харви Гильен (озвучка)','Джоэл Кроуфорд','Кот в сапогах отправляется в приключение, чтобы вернуть утраченные жизни.','https://image.tmdb.org/t/p/w500/kuf6dutpsT0vSVehic3EZIqkOBt.jpg',False,None),
('Чёрная пантера: Ваканда навеки','Black Panther: Wakanda Forever','action',2022,161,'6.7','Летиша Райт, Анджела Бассетт, Теноч Уэрта','Райан Куглер','Ваканда защищает своё будущее после тяжёлой утраты.','https://image.tmdb.org/t/p/w500/sv1xJUazXeYqALzczSZ3O6nkH75.jpg',False,None),

]
GENRES=[('fantasy','Фэнтези'),('sci-fi','Фантастика'),('animation','Мультфильмы'),('comedy','Комедия'),('action','Боевик'),('drama','Драма')]
class Command(BaseCommand):
    help='Учебные фильмы, кинотеатры и условные сеансы. НЕ реальные расписания.'
    def handle(self,*args,**kwargs):
        for slug,name in GENRES: Genre.objects.update_or_create(slug=slug,defaults={'name':name})
        for title,original,slug,year,duration,rating,actors,director,description,poster,upcoming,release in MOVIES:
            Movie.objects.update_or_create(original_title=original,defaults={'title':title,'genre':Genre.objects.get(slug=slug),'year':year,'duration':duration,'rating':rating,'actors':actors,'director':director,'description':description,'poster':poster,'trailer':'https://www.youtube.com/results?search_query='+quote_plus(original+' official trailer'), 'is_upcoming':upcoming,'release_date':release})
        names=['Дордой Плаза','Томми Молл','Азия Молл']
        for name in names:
            cinema,_=Cinema.objects.get_or_create(name=name)
            for hall_name in ['Зал 1','Зал 2','VIP зал']:
                Hall.objects.get_or_create(cinema=cinema,name=hall_name,defaults={'rows':5,'columns':8})
        # Демонстрационные сеансы: каждый фильм доступен сегодня и в следующие 13 дней.
        # На каждом дне 9 залов × 5 времён = 45 сеансов, распределённых по каталогу.
        today=timezone.localdate()
        current=list(Movie.objects.filter(is_upcoming=False).order_by('id'))
        halls=list(Hall.objects.select_related('cinema').order_by('id'))
        times=[(10,30),(13,0),(15,30),(18,0),(20,30),(23,0)]
        count=0
        if current:
            for offset in range(14):
                day=today+timedelta(days=offset)
                for h_idx,hall in enumerate(halls):
                    for t_idx,(hour,minute) in enumerate(times):
                        at=timezone.make_aware(datetime.combine(day,time(hour,minute)),timezone.get_current_timezone())
                        if at<=timezone.now():
                            continue
                        movie=current[(h_idx*len(times)+t_idx+offset)%len(current)]
                        # Не перезаписываем уже существующие сеансы с бронями.
                        _,created=Showtime.objects.get_or_create(
                            hall=hall,starts_at=at,
                            defaults={'movie':movie,'price':550 if 'VIP' in hall.name else 350}
                        )
                        count+=int(created)
        self.stdout.write(self.style.SUCCESS(f'Афиша обновлена: {count} новых сеансов. Расписание и цены демонстрационные.'))
