from django.shortcuts import render,redirect
from .models import Phone
from django.http import HttpResponse
from .form import Login_form
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def phone_index(request):
    #判断是否有查询数据
    q=request.GET.get('q','')
    if q!='':
        infos = Phone.objects.filter(comment__contains=q)
    else:
        infos = Phone.objects.all() #.order_by('-sentiment')
    #评论数量
    count_comment=infos.count()
    #正向评论数
    count_comment_positive=infos.filter(sentiment__gte=0.5).count()
    if count_comment:
        percent_comment_positive=round(count_comment_positive/count_comment*100,2)
    else:
        percent_comment_positive=0
    #负向评论数
    count_comment_negative=count_comment-count_comment_positive
    percent_comment_negative=100-percent_comment_positive
    # 获取当前页码
    page_id=request.GET.get('page',1)
    # 数据分页
    paginator = Paginator(infos, 30)
    # 获得当前页码数据
    page_data = paginator.page(page_id)

    return render(request, 'phone_shorts.html', locals())

def login2(request):
    if request.method == 'GET':
        loginform = Login_form()
        return render(request, 'form2.html', {'form': loginform})

    if request.method == 'POST':
        loginform = Login_form(request.POST)
        if loginform.is_valid():
            # 读取表单的返回值
            cd = loginform.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return redirect('./index')
            else:
                return HttpResponse('密码错误，请重新登陆')
