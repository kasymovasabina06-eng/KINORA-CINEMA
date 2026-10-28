from django.urls import path
from . import views
app_name='booking'
urlpatterns=[path('signup/',views.signup,name='signup'),path('profile/',views.profile,name='profile'),path('show/<int:showtime_id>/',views.seats,name='seats'),path('show/<int:showtime_id>/reserve/',views.reserve,name='reserve'),path('order/<uuid:booking_id>/pay/',views.pay,name='pay'),path('order/<uuid:booking_id>/demo-pay/',views.demo_pay,name='demo_pay'),path('order/<uuid:booking_id>/cancel/',views.cancel,name='cancel'),path('order/<uuid:booking_id>/ticket/',views.ticket,name='ticket'),path('check/<uuid:booking_id>/',views.verify,name='verify'),path('favorite/<int:movie_id>/',views.favorite,name='favorite')]
