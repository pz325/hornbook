from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def study(request):
    category = request.GET.get('category', 'read_hanzi')
    return render(request, 'study.html', {'category': category})
