from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

User=get_user_model()

def index(request):
    # 모든 유저의 username, img_profile, nickname을 리스트(ul>li)로 보여주는 뷰 생성
    users = User.objects.all()
    context = {
        'users': users
    }

    # return HttpResponse('hello')
    return render(request, 'index.html', context)
