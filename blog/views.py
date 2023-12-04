from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import *
from home.models import  About
from django.urls import reverse
from .forms import CommentForm, BlogSearchForm
from django.db.models import Q, Count
from django.views import View

class HomeView(ListView):
    model = Blog 
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-published']
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Blog.objects.all().order_by('-published')
        context['categories'] = Category.objects.all()
        # context['latest_post'] = Blog.objects.latest('published')
        context['top_editors_pick'] = Blog.objects.filter(post_type__title="Editor's Pick").first()
        context['blogauthor'] = About.objects.all() 

        return context

class BlogDetailView(FormMixin, DetailView):
    model = Blog 
    template_name = 'post.html'
    form_class = CommentForm
  
    def get_object(self, queryset=None):
        category_slug = self.kwargs['category_slug']
        post_slug = self.kwargs['post_slug']
        blog = get_object_or_404(Blog, category__slug=category_slug, slug=post_slug)
        return blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = BlogTag.objects.values('tag').annotate(tag_count=Count('tag'))
        context['categories'] = Category.objects.all()
        context['posts'] = Blog.objects.all().order_by('-published')
        context['latest_post'] = Blog.objects.latest('published')
        context['comment_form'] = CommentForm()
        context['blogauthor'] = About.objects.all() 
        context['comments'] = BlogComment.objects.filter(title=self.object)
        return context
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            commenter_name = form.cleaned_data.get('commenter_name')
            BlogComment.objects.create(
                title=self.object,
                comment=comment,
                commenter_name=commenter_name
            )
            return redirect(self.object)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        category_slug = self.object.category.slug
        post_slug=self.object.slug

        return HttpResponseRedirect(reverse('blog:error', kwargs={'category_slug': category_slug, 'post_slug': post_slug}))


class SearchView(View):
    model = Blog 
    template_name = 'search.html'
    paginate_by = 2
    
    def get(self, request, *args, **kwargs):
        form = BlogSearchForm(request.GET)
        results = []
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Blog.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(blogsection__outline_content__icontains=query)
            ).distinct()

            results = list(results) 
            
        categories = Category.objects.all()
        other_categories = Category.objects.all()
        latest_post = Blog.objects.latest('published')
        posts = Blog.objects.all().order_by('-published')
        tags = BlogTag.objects.values('tag').annotate(tag_count=Count('tag'))

        context = {
            'query' : query,
            'form': form,
            'results' : results,
            'results': results,
            'other_categories' : other_categories,
            'latest_post': latest_post,
            'categories' : categories,
            'posts' : posts,
            'tags': tags,
        }
        return render(request, self.template_name, context)
    
