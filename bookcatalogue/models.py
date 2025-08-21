from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    birt_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(to=Genre)

    def __str__(self):
        return f'"{self.title}". ({self.year})'

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('book', 'user')
