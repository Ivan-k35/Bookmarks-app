from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    context = {'section': 'images', 'form': form}
    return render(request, 'images/image/create.html', context)


def image_detail(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, slug=slug)
    context = {'section': 'images', 'image': image}
    return render(request, 'images/image/detail.html', context)


@login_required
@require_POST
def image_like(request):
    image_pk = request.POST.get('pk')
    action = request.POST.get('action')
    if image_pk and action:
        try:
            image = Image.objects.get(pk=image_pk)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
