from django.shortcuts import render
from django.http import HttpResponse
from Manager.worksmodels import Works
from Manager.chapter_models import Chapters
from django.http import HttpResponse, HttpResponseRedirect
import time;
def writer(func):
    def _writer(request):
        try:
            session = request.session['userlogin']
            if session['role'] == 3:
                return func(request,session)
            else:
                return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
        except Exception as err:
            print(err)
            return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
        return func(request)
    return _writer
@writer
def writers_work(request,session):
        rs = Works.objects.filter(uid=session['id'])
        # rs.workname
        return render(request, 'writer/writers_works.html',{'session': session,'rs':rs})
@writer
def create_works(request,session):
        return render(request, 'writer/create_works.html',{'session': session})
@writer
def Cnew_work(request,session):
    if request.method == 'POST':
        # 转成字典形式
        dict = request.POST.dict();
        if dict['workname']=="":
            return HttpResponse("<script>alert('用户名不得为空！');location.href='/index' </script>")
        if dict['label']=="":
            return HttpResponse("<script>alert('密码不得为空！');location.href='/index' </script>")
        if dict['introduce']=="":
            return HttpResponse("<script>alert('昵称不得为空！');location.href='/index' </script>")
        try:
            del dict['csrfmiddlewaretoken']
            dict['uid'] = session['id']  # **dict必须放到最后
            user=Works.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        **dict)
            # print(user)
            # print(dict);
            return HttpResponseRedirect('/index/writers_works/');
        except Exception as err:
            print(err)
            return HttpResponse("<script>alert('数据库连接有误！');location.href='/index' </script>")

    else:
        return HttpResponse("请正确提交")
@writer
def work_manager(request,session):
    wid=request.GET['wid']
    # print(wid)
    session['wid']=wid
    request.session['userlogin']=session
    # 查询有作品id的章节
    rs=Chapters.objects.filter(worksid=session['wid'])
    return render(request, 'writer/work_manager.html', {'session': session,'rs':rs})
@writer
def chapter_name(request,session):
    return render(request, 'writer/chapter_name.html', {'session': session})
@writer
def submit_chapter_name(request,session):
    if request.method == 'POST':
        # 转成字典形式
        dict = request.POST.dict();
        try:
            del dict['csrfmiddlewaretoken']
            dict['worksid']=session['wid']
            dict['uid'] = session['id']  # **dict必须放到最后
            Chapters.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        **dict)
            rs=Chapters.objects.filter(worksid=session['wid'])
            return render(request, 'writer/work_manager.html', {'session': session,'rs':rs})
        except Exception as err:
            print(err)
            return HttpResponse("<script>alert('数据库连接有误！');location.href='/index' </script>")

    else:
        return HttpResponse("请正确提交")
@writer
def charpter_content(request,session):
    id=request.GET['cid']
    rs = Chapters.objects.filter(id=id).first()
    print(rs.id)
    return render(request, 'writer/charpter_content.html', {'session': session,'rs':rs})
@writer
def submit_charpter(request,session):
    if request.method == 'POST':
        # 转成字典形式
        dict = request.POST.dict();
        try:
            del dict['csrfmiddlewaretoken']
            dict['worksid']=session['wid']
            dict['uid'] = session['id']  # **dict必须放到最后
            if dict['chaptername']=="":
                Chapters.objects.filter(id=dict['id']).update(content=dict['content'], pubflag=dict['pubflag'])
            else:
                Chapters.objects.filter(id=dict['id']).update(content=dict['content'],pubflag=dict['pubflag'],chaptername=dict['chaptername'])
            rs = Works.objects.filter(uid=session['id'])
            return render(request, 'writer/writers_works.html', {'session': session,'rs':rs})
        except Exception as err:
            print(err)
            return HttpResponse("<script>alert('数据库连接有误！');location.href='/index' </script>")

    else:
        return HttpResponse("请正确提交")