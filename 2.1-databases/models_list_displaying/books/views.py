import datetime
from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books_objects = Book.objects.all()
    context = {
        'books': books_objects,
    }
    return render(request, template, context)


def books_date_pagin(request, pub_date):
    template = 'books/books_list.html'
    books_objects = Book.objects.filter(pub_date=pub_date)
    date = Book.objects.values_list('pub_date').filter(pub_date=pub_date)
    dates_list = Book.objects.all().values_list('pub_date').distinct().order_by('pub_date')
    # index =
    pagges = [next for next in dates_list]
    previous_page = pagges[pagges.index(date[0]) - 1]
    if previous_page == pagges[-1]:
        previous_page = False
    else:
        previous_page = pagges[pagges.index(date[0]) - 1][0].strftime('%Y-%m-%d')
    try:
        next_page = pagges[pagges.index(date[0]) + 1][0].strftime('%Y-%m-%d')
    except IndexError:
        next_page = False
    context = {
        'books': books_objects,
        'next': next_page,
        'previous': previous_page,
    }
    return render(request, template, context)
