from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from booking.models import Showtime,Cinema
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,render
from .models import Movie,Genre

def movie_list(request):
    movies=Movie.objects.select_related('genre').all()
    q=request.GET.get('q','').strip()
    genre=request.GET.get('genre','').strip()
    sort=request.GET.get('sort','rating')
    if q: movies=movies.filter(Q(title__icontains=q)|Q(original_title__icontains=q)|Q(actors__icontains=q))
    if genre: movies=movies.filter(genre__slug=genre)
    if sort=='year': movies=movies.order_by('-year','title')
    elif sort=='title': movies=movies.order_by('title')
    elif sort=='new': movies=movies.order_by('-created_at')
    else: movies=movies.order_by('-rating')
    return render(request,'movies/movie_list.html',{'movies':movies,'genres':Genre.objects.all(),'q':q,'chosen_genre':genre,'sort':sort})

def movie_detail(request,movie_id):
    movie=get_object_or_404(Movie.objects.select_related('genre'),pk=movie_id)
    today=timezone.localdate()
    dates=[{'date':today+timedelta(days=i),'label':('Сегодня' if i==0 else 'Завтра' if i==1 else (today+timedelta(days=i)).strftime('%d.%m'))} for i in range(14)]
    raw_date=request.GET.get('date','')
    valid_dates={item['date'].isoformat():item['date'] for item in dates}
    chosen_date=valid_dates.get(raw_date,today)
    chosen_cinema=request.GET.get('cinema','').strip()
    cinemas=Cinema.objects.all().order_by('name')
    showtimes=Showtime.objects.select_related('hall__cinema').filter(
        movie=movie,starts_at__gte=timezone.now(),starts_at__date=chosen_date
    ).order_by('starts_at','hall__cinema__name')
    if chosen_cinema:
        showtimes=showtimes.filter(hall__cinema_id=chosen_cinema)
    return render(request,'movies/movie_detail.html',{
        'movie':movie,'showtimes':showtimes,'dates':dates,
        'chosen_date':chosen_date,'chosen_cinema':chosen_cinema,'cinemas':cinemas,
    })

def genre_detail(request,slug):
    genre=get_object_or_404(Genre,slug=slug)
    return render(request,'movies/genre.html',{'genre':genre,'movies':genre.movies.all()})

def api_movies(request):
    return JsonResponse({'movies':[{'id':m.id,'title':m.title,'genre':m.genre.name,'year':m.year,'upcoming':m.is_upcoming} for m in Movie.objects.select_related('genre')]})


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from .forms import MovieForm

def upcoming(request):
    movies = Movie.objects.filter(is_upcoming=True).select_related('genre').order_by('release_date')
    return render(request, 'movies/upcoming.html', {'movies':movies})

def can_manage(user):
    return user.is_authenticated and (user.is_staff or user.has_perm('movies.change_movie'))

@login_required
def movie_create(request):
    if not (request.user.is_staff or request.user.has_perm('movies.add_movie')):
        raise PermissionDenied
    form = MovieForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        movie = form.save()
        messages.success(request, 'Фильм добавлен.')
        return redirect('movies:detail', movie.id)
    return render(request, 'movies/movie_form.html', {'form':form, 'heading':'Добавить фильм'})

@login_required
def movie_update(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if not can_manage(request.user):
        raise PermissionDenied
    form = MovieForm(request.POST or None,instance=movie)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Изменения сохранены.')
        return redirect('movies:detail',movie.id)
    return render(request,'movies/movie_form.html',{'form':form,'heading':'Редактировать фильм'})

@login_required
@require_http_methods(['GET','POST'])
def movie_delete(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if not (request.user.is_superuser or request.user.has_perm('movies.delete_movie')):
        raise PermissionDenied
    if request.method == 'POST':
        movie.delete()
        messages.success(request,'Фильм удалён.')
        return redirect('movies:list')
    return render(request,'movies/movie_delete.html',{'movie':movie})
