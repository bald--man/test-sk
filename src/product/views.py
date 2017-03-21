from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView

from django.utils import timezone
from datetime import timedelta

from .forms import ProductForm, CommentForm
from .models import Product, Comment

# Create your views here.


class ProductLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(Product, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


def product_list(request):
    queryset_list = Product.objects.all()  # .order_by("-created_at")

    sort = request.GET.get('sort')
    if sort == 'likes':
        queryset_list = Product.objects.all().order_by('-likes')

    paginator = Paginator(queryset_list, 10)  # Show n product per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "page_request_var": page_request_var,
        "sort": sort,
    }
    return render(request, "product_list.html", context)


def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Successfully Created")

    context = {
        "form": form,
    }
    return render(request, "product_form.html", context)


def product_detail(request, slug=None):
    instance = get_object_or_404(Product, slug=slug)
    initial_data = {
                 "content_type": instance.get_content_type,
                 "object_id": instance.id
        }
    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
                                    content_type=content_type,
                                    object_id=obj_id,
                                    content=content_data,
                                )

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    comments = instance.comments.filter(timestamp__gt=timezone.now()-timedelta(days=1))
    context = {
        "name": instance.name,
        "instance": instance,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "product_detail.html", context)


def product_update(request, slug=None):
    instance = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "name": instance.name,
        "instance": instance,
        "form": form,
    }
    return render(request, "product_form.html", context)

