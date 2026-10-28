from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','original_title','genre','description','year','duration','rating','age','actors','director','poster','trailer','is_upcoming','release_date']
        widgets = {'description':forms.Textarea(attrs={'rows':5}), 'release_date':forms.DateInput(attrs={'type':'date'})}

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 5:
            raise forms.ValidationError('Название должно содержать не менее 5 символов.')
        if Movie.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Фильм с таким названием уже существует.')
        return title

    def clean_description(self):
        value = self.cleaned_data['description'].strip()
        if len(value) < 15:
            raise forms.ValidationError('Описание должно содержать не менее 15 символов.')
        return value

    def clean(self):
        data = super().clean()
        if data.get('title','').casefold() == data.get('description','').casefold():
            self.add_error('description','Описание не должно совпадать с названием.')
        return data
