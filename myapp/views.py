from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .data import books

def index(request):
    return render(request, "myapp/index.html")

def book_list(request):
    return render(request, "myapp/book_list.html", {"books": books.values()})

def book_detail(request, id: int):
    book = books.get(id)

    if book is None:
        raise Http404()

    return render(request, "myapp/book_detail.html", {"book": book})
    
def old_catalog(request):
    return HttpResponseRedirect(reverse("dot:book_list"))

def not_found(request, exception):
    return render(request, "myapp/404.html", status=404)
