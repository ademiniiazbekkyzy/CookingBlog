from django.contrib import messages
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView

from main.forms import RecipeForm, ImageForm
from main.models import *


def index(request):
    return render(request, 'index.html')

# class MainPageView(ListView):
#     model = Recipe
#     template_name = 'index.html'
#     context_object_name = 'recipes'
#
#     def get_template_names(self):
#         template_name = super(MainPageView, self).get_template_names()
#         search = self.request.GET.get('q')
#         if search:
#            template_name = 'search.html'
#         return template_name
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         search = self.request.GET.get('q')
#         if search:
#             context['recipes'] = Recipe.objects.filter(Q(title__icontains=search)|
#                                                        Q(description__icontains=search))
#         else:
#             context['recipes'] = Recipe.objects.all()
#         return context


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    recipes = Recipe.objects.filter(category_id=slug)
    return render(request, 'category-detail.html', locals())


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    image = recipe.get_image
    images = recipe.images.exclude(id=image.id)
    return render(request, 'recipe-detail.html', locals())


def add_recipe(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, recipe=recipe)
            return redirect(recipe.get_absolute_url())
        else:
            recipe_form = RecipeForm()
            formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-recipe.html', locals())


def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    recipe_form = RecipeForm(request.POST or None, instance=recipe)
    formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(recipe=recipe))
    if recipe_form.is_valid() and formset.is_valid():
        recipe = recipe_form.save()

        for form in formset.cleaned_data:
            image = form.save(commit=False)
            image.recipe = recipe
            image.save()
        return redirect(recipe.get_absolute_url())
    return render(request, 'update-recipe.html', locals())


def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return redirect('home')
    return render(request, 'delete-recipe.html')
