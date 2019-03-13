from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def lists_share(request, list1_id):
    list_ = List.objects.get(id=list1_id)
    if request.method == 'POST':
        email = request.POST.get('sharee')
        user = User.objects.filter(email=email)
        if email:
            if not user:
                User.objects.create(email=email)
            list_.shared_with.add(email)

    return redirect(list_)

