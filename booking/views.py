import base64
from io import BytesIO
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError,transaction
from django.http import Http404,HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import SignupForm
from .models import Showtime,Booking,BookingSeat,Profile

def signup(request):
    if request.user.is_authenticated: return redirect('booking:profile')
    form=SignupForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); Profile.objects.get_or_create(user=user); login(request,user)
        return redirect('booking:profile')
    return render(request,'accounts/signup.html',{'form':form})

@login_required
def profile(request):
    bookings=Booking.objects.filter(user=request.user).select_related('showtime__movie','showtime__hall__cinema').prefetch_related('seats').order_by('-created_at')
    return render(request,'accounts/profile.html',{'bookings':bookings})

@login_required
def seats(request,showtime_id):
    showtime=get_object_or_404(Showtime.objects.select_related('movie','hall__cinema'),pk=showtime_id,starts_at__gt=timezone.now(),movie__is_upcoming=False)
    taken={(s.row,s.number) for s in showtime.booked_seats.all()}
    matrix=[{'row':r,'items':[{'number':n,'taken':(r,n) in taken,'key':f'{r}-{n}'} for n in range(1,showtime.hall.columns+1)]} for r in range(1,showtime.hall.rows+1)]
    return render(request,'booking/seats.html',{'showtime':showtime,'matrix':matrix})

@login_required
@require_POST
def reserve(request,showtime_id):
    showtime=get_object_or_404(Showtime.objects.select_related('movie','hall'),pk=showtime_id,starts_at__gt=timezone.now(),movie__is_upcoming=False)
    raw=request.POST.getlist('seats')
    if not 1<=len(raw)<=6 or len(set(raw))!=len(raw):
        messages.error(request,'Выберите от 1 до 6 разных мест.'); return redirect('booking:seats',showtime_id)
    parsed=[]
    try:
        for s in raw:
            a,b=s.split('-'); row,col=int(a),int(b)
            if not (1<=row<=showtime.hall.rows and 1<=col<=showtime.hall.columns): raise ValueError()
            parsed.append((row,col))
    except (ValueError,AttributeError):
        messages.error(request,'Недопустимый номер места.'); return redirect('booking:seats',showtime_id)
    try:
        with transaction.atomic():
            booking=Booking.objects.create(user=request.user,showtime=showtime,total=len(parsed)*showtime.price)
            for r,n in parsed: BookingSeat.objects.create(booking=booking,showtime=showtime,row=r,number=n)
    except IntegrityError:
        messages.error(request,'Некоторые места уже заняты — выберите другие.'); return redirect('booking:seats',showtime_id)
    return redirect('booking:pay',booking.id)

@login_required
def pay(request,booking_id):
    booking=get_object_or_404(Booking.objects.select_related('showtime__movie','showtime__hall__cinema').prefetch_related('seats'),id=booking_id,user=request.user)
    if booking.status=='paid': return redirect('booking:ticket',booking.id)
    return render(request,'booking/pay.html',{'booking':booking})

@login_required
@require_POST
def demo_pay(request,booking_id):
    with transaction.atomic():
        booking=get_object_or_404(Booking.objects.select_for_update(),id=booking_id,user=request.user)
        if request.POST.get('method') not in ('mbank','elcart','card'):
            messages.error(request,'Выберите способ оплаты.')
            return redirect('booking:pay',booking.id)
        if booking.status=='pending': booking.status='paid'; booking.save(update_fields=['status'])
    messages.success(request,'Демо-оплата завершена. Реальные деньги не списывались.')
    return redirect('booking:ticket',booking.id)

@login_required
@require_POST
def cancel(request,booking_id):
    with transaction.atomic():
        booking=get_object_or_404(Booking.objects.select_for_update(),id=booking_id,user=request.user,status='pending')
        booking.status='cancelled'; booking.save(update_fields=['status']); booking.seats.all().delete()
    messages.info(request,'Бронь отменена.'); return redirect('booking:profile')

@login_required
def ticket(request,booking_id):
    booking=get_object_or_404(Booking.objects.select_related('showtime__movie','showtime__hall__cinema').prefetch_related('seats'),id=booking_id,user=request.user,status='paid')
    qr=None
    try:
        import qrcode
        from django.urls import reverse
        url=request.build_absolute_uri(reverse('booking:verify',args=[booking.id]))
        qr_image=qrcode.make(url); out=BytesIO(); qr_image.save(out,format='PNG'); qr=base64.b64encode(out.getvalue()).decode('ascii')
    except ImportError: pass
    return render(request,'booking/ticket.html',{'booking':booking,'qr':qr})

@login_required
def verify(request,booking_id):
    if not request.user.is_staff:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied('Проверка QR доступна только сотрудникам.')
    booking=get_object_or_404(Booking.objects.select_related('showtime__movie','showtime__hall__cinema'),id=booking_id)
    return render(request,'booking/verify.html',{'booking':booking})

@login_required
@require_POST
def favorite(request,movie_id):
    from movies.models import Movie
    movie=get_object_or_404(Movie,id=movie_id); profile,_=Profile.objects.get_or_create(user=request.user)
    if profile.favorites.filter(pk=movie.pk).exists(): profile.favorites.remove(movie)
    else: profile.favorites.add(movie)
    return redirect('movies:detail',movie_id)
