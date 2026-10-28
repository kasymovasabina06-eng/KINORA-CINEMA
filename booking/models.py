import uuid
from django.conf import settings
from django.db import models
class Cinema(models.Model):
    name=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=220,blank=True)
    def __str__(self): return self.name
    class Meta: verbose_name='Кинотеатр'; verbose_name_plural='Кинотеатры'
class Hall(models.Model):
    cinema=models.ForeignKey(Cinema,on_delete=models.CASCADE,related_name='halls')
    name=models.CharField(max_length=80)
    rows=models.PositiveSmallIntegerField(default=5)
    columns=models.PositiveSmallIntegerField(default=8)
    def __str__(self): return f'{self.cinema} • {self.name}'
    class Meta: constraints=[models.UniqueConstraint(fields=['cinema','name'],name='unique_hall_per_cinema')]
class Showtime(models.Model):
    movie=models.ForeignKey('movies.Movie',on_delete=models.CASCADE,related_name='showtimes')
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE,related_name='showtimes')
    starts_at=models.DateTimeField()
    price=models.PositiveIntegerField(default=350)
    def __str__(self): return f'{self.movie} • {self.hall} • {self.starts_at:%d.%m %H:%M}'
    class Meta: ordering=['starts_at']; constraints=[models.UniqueConstraint(fields=['hall','starts_at'],name='unique_showtime_per_hall')]
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cinema_profile')
    phone=models.CharField(max_length=30,blank=True)
    favorites=models.ManyToManyField('movies.Movie',blank=True,related_name='fans')
    def __str__(self): return self.user.username
class Booking(models.Model):
    STATES=[('pending','Ожидает оплаты'),('paid','Оплачено (демо)'),('cancelled','Отменено')]
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cinema_bookings')
    showtime=models.ForeignKey(Showtime,on_delete=models.PROTECT,related_name='bookings')
    status=models.CharField(max_length=15,choices=STATES,default='pending')
    total=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return str(self.id)[:8]
class BookingSeat(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='seats')
    showtime=models.ForeignKey(Showtime,on_delete=models.CASCADE,related_name='booked_seats')
    row=models.PositiveSmallIntegerField()
    number=models.PositiveSmallIntegerField()
    class Meta: constraints=[models.UniqueConstraint(fields=['showtime','row','number'],name='unique_seat_per_showtime')]
