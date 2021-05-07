from sys import api_version
from django.utils.text import re_words
from newsapp.models import News
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response


def manage_news(request):
    news_objs = News.objects.all()

    context = {'news_objs' : news_objs , 'is_active' :'news'}
    return render(request , 'manage_news.html' , context)


def create_news(request):
    context = {'form' : NewsForm  , 'is_active' : 'news'}

    if request.method == 'POST':
        form = NewsForm(request.POST)
        title = request.POST.get('title')
        try:

            if form.is_valid():
                content = form.cleaned_data['content']
                print(type(content))
                print(title)
                News.objects.create(
                    title=title,
                    content = content
                )
        except Exception as e:
            print(e)
            # news_obj = News(
            #     title = title,
            #     content = context
            # )
            # news_obj.save()
        
        return redirect('/news/create-news/')


    return render(request , 'create_news.html' , context)


def update_news(request , id):
    context = {'is_active' : 'news'}

    try:
        if request.method == 'POST':
            form = NewsForm(request.POST)
            title = request.POST.get('title')
            try:
                if form.is_valid():
                    content = form.cleaned_data['content']

                    news_obj = News.objects.get(id = id)
                    
                    news_obj.title = title
                    news_obj.content = content
                    news_obj.save()
                    return redirect(f'/news/update-news/{id}/')
            except Exception as e:
                print(e)

        news_obj = News.objects.get(id = id)
        initial_dict = {'content' : news_obj.content}
        form = NewsForm(initial=initial_dict)
        context['form'] = form
        context['news_obj'] = news_obj

    except Exception as e:
        print(e)



    return render(request , 'update_news.html' , context)




def view_news(request , slug):
    context = {'is_active' : 'news'}
    try:
        news_obj = News.objects.filter(slug = slug).first()
        print(news_obj)
        context  = {'news_obj' : news_obj}
    except Exception as e:
        print('AAA')
        print(e)
        print('AAA')

    print(context)
    return render(request , 'views_news.html' , context)









class ToggleNewsTrending(APIView):
    def get(self , request):
        id = request.GET.get('id')
        print('caught')
        try:
            if id:
                news_obj = News.objects.get(id = id)
                news_obj.is_trending = not news_obj.is_trending
                news_obj.save()
        except Exception as e:
            print(e)

        return Response({'status' : 200})

ToggleNewsTrending = ToggleNewsTrending.as_view()

class ToggleNewsPublished(APIView):
    def get(self , request):
        id = request.GET.get('id')
        try:
            if id :
                news_obj = News.objects.get(id = id)
                news_obj.is_published = not news_obj.is_published
                news_obj.save()
        except Exception as e:
            print(e)
        
        return Response({'status' : 200})
        

        
ToggleNewsPublished = ToggleNewsPublished.as_view()





class DeleteNews(APIView):
    def get(self , request):
        id = request.GET.get('id')
        print(id)
        try:
            if id :
                news_obj = News.objects.get(id = id)
                print(news_obj)
                news_obj.is_deleted = True
                news_obj.save()
        except Exception as e:
            print(e)
        
        return Response({'status' : 200})

DeleteNews = DeleteNews.as_view()