from django.shortcuts import render
from django.contrib.auth import authenticate;
import time;
import MySQLdb;
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponseRedirect
from Manager.models import Users
def index(request):
    return render(request, 'index.html');
def register(request):
    print(request.method)
    if request.method =='POST':
        # 转成字典形式
        dict = request.POST.dict();
        # print(dict);
        try:
            del dict['csrfmiddlewaretoken']
            Users.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),**dict)  # **dict必须放到最后
            request.session['login']=dict
            return HttpResponseRedirect('/index/login/');
        except Exception as err:
            if 'emailuniq' in err.args[1]:
                return HttpResponse("<script>alert('用户名重复！');location.href='/index' </script>")
            if 'nichenguniq' in err.args[1]:
                return HttpResponse("<script>alert('昵称重复！');location.href='/index' </script>")
            print("ERROR")
    else:
         return HttpResponse("请正确提交")
def login(request):
    if request.method == 'POST':
        email = request.POST['email'];
        pwd = request.POST['pwd']
        user=Users.objects.filter(email=email,pwd=pwd).first();
        role=user.role
        if user==None:
            return HttpResponse("用户名密码错误");
        request.session['userlogin'] = {'email':email,'pwd':pwd,'role':role};
        # return HttpResponse("success");
        return HttpResponseRedirect('/index/userhome/');
    else:
        dict=request.session['login'];
        print(dict)
        if dict!=None:
            request.session['userlogin'] =dict
            del request.session['login'];
            return HttpResponse("success");
        else:
            return HttpResponse("please rejister");
def loginhtml(request):
    return render(request, 'login.html')
def registerhtml(request):
    return render(request, 'register.html')
def userhome(request):
    return render(request,'usershome.html')