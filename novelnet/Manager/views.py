from django.shortcuts import render,redirect
import time;
from pymongo import MongoClient
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from Manager.models import Users,Writers
from django.db.models import F
from Manager.message_models import Messages
from django.db import transaction
from os import path
import os;
def index(request):
    userlogin=None
    message=None
    try:
        userlogin=request.session['userlogin']
        # 查信息表倒叙输出(作品表数据不够)
        message=Users.objects.raw("select * from messages ORDER BY updtime DESC")
        for i in message:
            print(message.updtime)
    except Exception as arr:
        pass
    # del request.session['userlogin']
    return render(request, 'index.html',{'userlogin':userlogin,'message':message});
def register(request):
    if request.method == 'POST':
        # 转成字典形式
        dict = request.POST.dict();
        if dict['email']=="":
            return HttpResponse("<script>alert('用户名不得为空！');location.href='/index' </script>")
        if dict['pwd']=="":
            return HttpResponse("<script>alert('密码不得为空！');location.href='/index' </script>")
        if dict['nicheng']=="":
            return HttpResponse("<script>alert('昵称不得为空！');location.href='/index' </script>")
        # print(dict);
        try:
            del dict['csrfmiddlewaretoken']
            user = Users.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        **dict)
            dict['id'] = user.id  # **dict必须放到最后
            dict['msgnum']=user.msgnum
            request.session['login'] = dict
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
        dict=request.POST.dict()
        if dict['email']=="":
            return HttpResponse("<script>alert('用户名不得为空！');location.href='/index' </script>")
        if dict['pwd']=="":
            return HttpResponse("<script>alert('密码不得为空！');location.href='/index' </script>")
        dicts = Users.objects.filter(email=dict['email'], pwd=dict['pwd']).first();
        dict['role']= dicts.role
        dict['nicheng']=dicts.nicheng
        dict['id']=dicts.id
        dict['msgnum']=dicts.msgnum
        if dicts == None:
            return HttpResponse("用户名密码错误");
        request.session['userlogin'] = dict
        if dicts.role==0:
            return HttpResponseRedirect('/index/managerhome/');
        elif dicts.role>0:
            return HttpResponseRedirect('/index/userhome_head/');
    else:
        try:
            dict = request.session['login'];
            print(dict)
            if dict != None:
                request.session['userlogin'] = dict
                del request.session['login'];
                # return HttpResponse("success");
                return HttpResponseRedirect('/index/userhome_head/');
            else:
                return HttpResponse("please rejister");
        except Exception as err:
            return HttpResponse("<script>alert('请登录');location.href='/index' </script>")
def loginhtml(request):
    return render(request, 'home/login.html')
def registerhtml(request):
    return render(request, 'home/register.html')
def userhome_head(request):
    try:
        session = request.session['userlogin']
        if session['role']>0:
            return render(request, 'personhome/userhome_head.html', {'session': session})
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def managerhome(request):
    try:
        session = request.session['userlogin']
        if session['role']==0:
            return render(request, 'admin/managerhome.html', {'session': session})
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def userhome(request):
    try:
        userlogin = request.session['userlogin']
        if request.method != 'POST':
            return render(request, 'personhome/usershome.html',{'session':userlogin})
        dict = request.POST.dict()
        del dict['csrfmiddlewaretoken']
        idimage = request.FILES.get('idimage')
        if idimage == None:
            return HttpResponse("<script>alert('必须上传身份证照片');location.href='/index/userhome'</script>")
        idperson = request.FILES.get('idperson')
        if idperson == None:
            return HttpResponse("<script>alert('必须上传手持身份证照片');location.href='/index/userhome'</script>")
        try:
            # 改图片名字另存为
            idimagePath = "%s1%s" % (time.time(), idimage.name)
            f = open(os.path.join("manager\\static\\imgs", idimagePath), 'wb')
            for chunk in idimage.chunks(chunk_size=1024):
                f.write(chunk)
            dict['idimage'] = idimagePath
            dict['id']=userlogin['id']
            idpersonPath = "%s2%s" % (time.time(), idperson.name)
            f = open(os.path.join("manager\\static\\imgs", idpersonPath), 'wb')
            for chunk in idperson.chunks(chunk_size=1024):
                f.write(chunk)
            dict['idperson'] = idpersonPath
            Writers.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), **dict)
            dict['role'] = 2
            # 将 users表的role 修改
            Users.objects.filter(id=userlogin['id']).update(role=2)
            # 修改session
            dict['nicheng'] = userlogin['nicheng']
            print(dict)
            request.session['userlogin'] = dict
        except Exception as e:
            print(e)
        finally:
            f.close()
            return HttpResponseRedirect('/index/userhome_head/');
        if userlogin['role']>0:
            return render(request, 'personhome/usershome.html',{'session':userlogin})
        else:
            return HttpResponse("<script>alert('权限不足');location.href='/index'</script>")
    except Exception as err:
        if err =='userlogin':
            return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")

        return HttpResponse("<script>alert('页面错误');</script>")
def managerhome_writerapply(request):
    try:
        session = request.session['userlogin']

        if session['role'] == 0:
            sql="select w.id,w.biming,w.realname,w.updtime from users u,writers w where u.role=2 and u.id=w.id;"
            rs=Users.objects.raw(sql);
            return render(request, 'admin/managerhome_writerapply.html', {'session': session,'rs':rs})
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def write_off(request):
    del request.session['userlogin']
    return HttpResponseRedirect('/index/')
def writer_detail_message(request):
    try:
        session = request.session['userlogin']
        if session['role'] == 0:
            id=request.GET['id']
            rs=Writers.objects.filter(id=id).first();
            return render(request, 'admin/writer_detail_message.html', {'session': session,'rs':rs})
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def apply_default(request):
    try:

        session = request.session['userlogin']
        if session['role'] == 0:
            dict={}
            id=request.GET['id']
            contents=request.GET['contents']
            try:
                transaction.set_autocommit(False)
                Users.objects.filter(id=id).update(role=1,msgnum=F('msgnum')+1)
                writer=Writers.objects.filter(id=id).first()
                d = path.dirname(__file__)
                imgpath = os.path.join(d, 'static/imgs/', writer.idimage)
                imgpath1 = os.path.join(d, 'static/imgs/', writer.idperson)
                os.remove(imgpath)
                os.remove(imgpath1)
                Writers.objects.filter(id=id).delete()
                dict['sendId']=session['id']
                dict['sendName']="系统通知"
                dict['recId']=id
                dict['contents']=contents
                Messages.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                            **dict)
                transaction.commit()
            except Exception as err:
                print(err)
                transaction.rollback()
            finally:
                transaction.set_autocommit(True)
            return redirect("/index/managerhome_writerapply/")
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def apply_success(request):
    try:
        session = request.session['userlogin']
        if session['role'] == 0:
            id = request.GET['id']
            dict = {}
            try:

                transaction.set_autocommit(False)
                Users.objects.filter(id=id).update(role=3,msgnum=F('msgnum')+1)
                dict['sendId'] = session['id']
                dict['sendName'] = "系统通知"
                dict['recId'] = id
                dict['contents'] = "恭喜你成为作家"
                Messages.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        **dict)
                transaction.commit()
            except Exception as err:
                print(err)
                transaction.rollback()
            finally:
                transaction.set_autocommit(True)
            return redirect("/index/managerhome_writerapply/")
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def show_news(request):
    try:
        session = request.session['userlogin']
        message=Messages.objects.filter(recId=session['id'])
        # print(message.sendId)
        return render(request, 'news/show_news.html', {'session':session, 'message':message})
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
def work_type(request):
    try:
        session = request.session['userlogin']
        if session['role'] == 0:
            client = MongoClient('localhost', 27017)
            db = client.novel
            dicts={}
            collection = db.boy_list
            rs=collection.find()
            for item in rs:
                if item['pid']==None:
                    dicts[item['_id']]=[item]
                else :
                    dicts[item['pid']].append(item)
            return render(request, 'admin/works_type.html',{'rs':dicts})
        else:
            return HttpResponse("<script>alert('无访问权限');location.href='/index'</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('登录超时');location.href='/index'</script>")
