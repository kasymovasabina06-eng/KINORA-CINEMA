from django.db import models
class Genre(models.Model):
    name=models.CharField('Жанр',max_length=80,unique=True)
    slug=models.SlugField(unique=True)
    def __str__(self): return self.name
    class Meta: verbose_name='Жанр'; verbose_name_plural='Жанры'; ordering=['name']
class Movie(models.Model):
    genre=models.ForeignKey(Genre,on_delete=models.PROTECT,related_name='movies',verbose_name='Жанр')
    title=models.CharField('Название',max_length=180)
    original_title=models.CharField('Оригинальное название',max_length=180,blank=True)
    description=models.TextField('Описание')
    year=models.PositiveIntegerField('Год')
    duration=models.PositiveIntegerField('Минут',default=110)
    rating=models.DecimalField('Оценка',max_digits=3,decimal_places=1,default=0)
    age=models.CharField('Возраст',max_length=5,default='12+')
    actors=models.CharField('Актёры / озвучка',max_length=500,blank=True)
    director=models.CharField('Режиссёр',max_length=160,blank=True)
    poster=models.URLField('URL постера',max_length=600,blank=True)
    trailer=models.URLField('Ссылка на трейлер',blank=True)
    is_upcoming=models.BooleanField('Скоро в кино',default=False)
    release_date=models.DateField('Премьера',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
    class Meta: ordering=['-rating','title']; verbose_name='Фильм'; verbose_name_plural='Фильмы'
