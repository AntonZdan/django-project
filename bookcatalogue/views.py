from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Book, Author, Genre, Rating
from .forms import RegisterForm, RatingForm
from django.contrib import messages


def index(request):
    """
    This view renders 'index.html' template, when the user accesses the homepage '/'
    :param request:
    :return: Returning index.html template
    """
    return render(request, 'index.html')

def about(request):
    """
    This view renders 'about.html' template, when the user accesses the about page 'about/'
    :param request:
    :return: Returning about.html template
    """
    return render(request, 'about.html')

def contacts(request):
    """
    This view renders 'contacts.html' template, when the user accesses the contacts page 'contacts/'
    :param request:
    :return: Returning contacts.html template
    """
    return render(request, 'contacts.html')

def register(request):
    """
    If form in template have methods "POST", then uploading RegisterForm().
     If form is valid, all data saving in database and inform user about success registration,
     and renders user in "login.html" template for login.
    If user fill wrong information in form, he will get error notification,
    and user  will be redirected back to the 'register.html' template.
    This view renders 'register.html' template, when the user accesses the contacts page 'register/'
    :param request:
    :return: If success - redirect to the "login.html", if error - redirect back to the "register.html" template.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered!')
            return redirect('login')
        else:
            messages.error(request, 'Something goes wrong! Please try again.')
            return render(request, 'register.html', {'form': form,
                                                                        'request':request})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

class CatalogueListView(ListView):
    """
    Attributes:
        model = Book - Using to get all books.
        template_name = Using 'catalogue.html' template tu render all books.
        context_object_name = Using to access the list of books in the template
        paginate_by = Using to make pagination in 'catalogue.html'. If there are more than 6 books, pagination is applied.
    """

    model = Book
    template_name = 'catalogue.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        """
        Books can be filtering by author, genre, year(from - to) and ordering by "title" or "year".
        Annotated with queryset rating for each book(to display it in 'catalogue.html' template).
        :return: Returning filtered and ordered by "title" or "year" books.
        """
        queryset = Book.objects.all()

        author = self.request.GET.get('author')
        genre = self.request.GET.get('genre')
        from_year = self.request.GET.get('from_year')
        to_year = self.request.GET.get('to_year')
        ordering = self.request.GET.get('ordering')

        if author:
            queryset = queryset.filter(author__id=author)
        if genre:
            queryset = queryset.filter(genres__id=genre)
        if from_year:
            queryset = queryset.filter(year__gte=from_year)
        if to_year:
            queryset = queryset.filter(year__lte=to_year)
        if ordering == 'title':
            queryset = queryset.order_by('title')
        elif ordering == 'year':
            queryset = queryset.order_by('year')

        queryset = queryset.annotate(avg_rating=Avg('ratings__stars'))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds additional context data. (list of authors and genres).
        :param kwargs:
        :return: Returning updated context with "authors" and "genres" objects.
        """
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        return context

class BookDetailView(DetailView):
    """
    Attributes:
        model = Book - Using to get all books.
        template_name = Using 'book-detail.html' template tu render detailed book information.
        context_object_name = Using to access the book information in the template.
    """
    model = Book
    template_name = 'book-detail.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        """
        Retriving the book object and annotates it with average rating.
        Getting book from database using Primary Key (pk).
        :param queryset:
        :return: Returning book object with annotated average rating.
        """
        return Book.objects.annotate(avg_rating=Avg('ratings__stars')).get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """
        Adds additional context data. (list of average rating and rating count).
            :param kwargs:
            :return: Returning updated context with "average rating" and "rating count" objects.
        Checking is user logged in with "self.request.user.is_authenticated". If yes - updating context data (adding RatingForm)
        to allow user rate the book.
        """
        context = super().get_context_data(**kwargs)
        book = self.object
        context['average_rating'] = round(book.avg_rating, 2) if book.avg_rating is not None else "No rating"
        context['rating_count'] = book.ratings.count()

        if self.request.user.is_authenticated:
            context['form'] = RatingForm()
        return context

    def post(self, request, **kwargs):
        """
        Check: if user not logged in, redirecting to "login.html"
        Retriving book object using Primary Key (pk)
        Creating RatingForm form with request method "POST"
        If form is valid, getting users rating from form "stars".
        Creating new rating for book object or updating it if book has already rating.
        The user is informed with success message if rating was saved and also informed if something went wrong.
        :param request:
        :param kwargs:
        :return: Redirecting to the "book_detail.html" template with updated book rating.
        """
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = RatingForm(request.POST)
        if form.is_valid():
            stars = form.cleaned_data['stars']
            Rating.objects.update_or_create(user=request.user, book=self.object, defaults={'stars': stars})
            messages.success(request, 'Your rating was successfully saved!')
        else:
            messages.error(request, 'Something went wrong! Please try again.')
        return redirect('book_detail', pk=self.object.pk)


