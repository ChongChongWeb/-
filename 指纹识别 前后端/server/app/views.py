import time
import uuid

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View

from app import models
from comm import base, scan

'''
系统处理
'''
class SysView(View):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return SysView.getSessionInfo(request)
        elif module == 'exit':
            return SysView.exit(request)
        else:
            return base.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'info':
            return SysView.updSessionInfo(request)
        elif module == 'register':
            return SysView.register(request)
        elif module == 'login':
           return SysView.login(request)
        else:
            return base.error()

    '''
    用户注册处理
    '''
    def register(request):

        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            return base.warn('账号已存在，请重新输入')
        else:
            user = models.Users.objects.create(
                userName=request.POST.get('userName'),
                passWord=request.POST.get('passWord'),
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                type=2,
                createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )

            return base.success()

    '''
    用户登陆处理
    '''
    def login(request):

        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')

        user = models.Users.objects.filter(userName=userName)

        if (user.exists()):

            user = user.first()

            if user.passWord == passWord:

                token = uuid.uuid4()

                resl = {
                    'token': str(token)
                }

                cache.set(token, user.id, 60 * 60 * 60 * 3)

                return base.successData(resl)
            else:
                return base.warn('用户密码输入错误')

        else:
            return base.warn('用户名输入错误')

    '''
    用户登出处理
    '''
    def exit(request):

        token = request.GET.get('token')

        cache.delete(token)

        return base.success()

    '''
    获取登陆用户信息
    '''
    def getSessionInfo(request):

        user = models.Users.objects.filter(id=cache.get(request.GET.get('token'))).first()

        resl = {
            'id': user.id,
            'userName': user.userName,
            'passWord': user.passWord,
            'name': user.name,
            'gender': user.gender,
            'phone': user.phone,
            'createTime': user.createTime,
            'type': user.type
        }

        return base.successData(resl)

    '''
    修改登陆用户信息
    '''
    def updSessionInfo(request):

        user = models.Users.objects.filter(id=request.POST.get('id'))

        if (request.POST.get('userName') != user.first().userName) & \
                (models.Users.objects.filter(userName=request.POST.get('userName')).exists()):
            return base.warn('用户账号已存在')

        user.update(
            userName=request.POST.get('userName')
        )

        return base.success()



'''
系统用户处理
'''
class UserView(View):

    def get(self, request, module, *args, **kwargs):

        if module == 'page':
            return UserView.getPageInfo(request)
        else:
            return base.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return UserView.addInfo(request)
        elif module == 'del':
            return UserView.delInfo(request)
        else:
            return base.error()

    '''
    分页查看用户信息
    '''
    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')

        qruery = Q();
        qruery = qruery & (Q(type = 1) | Q(type = 2))
        if base.isExit(userName):
            qruery = qruery & Q(userName__contains=userName)
        if base.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Users.objects.filter(qruery).order_by("-createTime")

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'name': item.name,
                'gender': item.gender,
                'phone': item.phone,
                'type': item.type,
                'createTime': item.createTime
            }
            resl.append(temp)

        pageData = base.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return base.successData(pageData)

    '''
    添加用户信息
    '''
    def addInfo(request):

        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            return base.warn('账号已存在，请重新输入')

        user = models.Users.objects.create(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            phone=request.POST.get('phone'),
            type=1,
            createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

        return base.success()

    '''
    删除用户信息
    '''
    def delInfo(request):

        models.Users.objects.filter(id=request.POST.get('id')).delete()

        return base.success()


'''
系统应用处理
'''
class AppView(View):

    def get(self, request, module, *args, **kwargs):

        if module == 'page':
            return AppView.getPageInfo(request)
        elif module == 'list':
            return AppView.getList(request)
        else:
            return base.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return AppView.addInfo(request)
        elif module == 'upd':
            return AppView.updInfo(request)
        elif module == 'del':
            return AppView.delInfo(request)
        else:
            return base.error()

    '''
    查看全部应用信息
    '''
    def getList(request):

        apps = models.Apps.objects.all().values()

        return base.successData(list(apps))

    '''
    分页查看应用信息
    '''
    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();
        if base.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Apps.objects.filter(qruery).order_by("-createTime")

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'type': item.type,
                'details': item.details,
                'createTime': item.createTime
            }
            resl.append(temp)

        pageData = base.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return base.successData(pageData)

    '''
    添加应用信息
    '''
    def addInfo(request):

        if models.Apps.objects.filter(name=request.POST.get('name')).exists():
            return base.warn('应用已存在，请重新输入')

        models.Apps.objects.create(
            name=request.POST.get('name'),
            type=request.POST.get('type'),
            details=request.POST.get('details'),
            createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

        return base.success()

    '''
    修改应用信息
    '''
    def updInfo(request):

        app = models.Apps.objects.filter(id=request.POST.get('id'))

        if (request.POST.get('name') != app.first().name) & \
                (models.Apps.objects.filter(name=request.POST.get('name')).exists()):
            return base.warn('应用已存在，请重新输入')

        models.Apps.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name'),
            type=request.POST.get('type'),
            details=request.POST.get('details')
        )

        return base.success()

    '''
    删除应用信息
    '''
    def delInfo(request):

        if models.Fingers.objects.filter(app__id=request.POST.get('id')).exists():
            return base.warn('存在关联内容无法删除')

        models.Apps.objects.filter(id=request.POST.get('id')).delete()

        return base.success()


'''
系统指纹处理
'''
class FingerView(View):

    def get(self, request, module, *args, **kwargs):

        if module == 'page':
            return FingerView.getPageInfo(request)
        else:
            return base.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return FingerView.addInfo(request)
        elif module == 'upd':
            return FingerView.updInfo(request)
        elif module == 'del':
            return FingerView.delInfo(request)
        else:
            return base.error()

    '''
    分页查看指纹信息
    '''
    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        location = request.GET.get('location')
        appType = request.GET.get('appType')

        qruery = Q();
        if base.isExit(location):
            qruery = qruery & Q(location=int(location))
        if base.isExit(appType):
            qruery = qruery & Q(app__type=int(appType))

        data = models.Fingers.objects.filter(qruery).order_by("-createTime")

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'key': item.key,
                'location': item.location,
                'createTime': item.createTime,
                'appId': item.app.id,
                'appName': item.app.name,
                'appType': item.app.type,
            }
            resl.append(temp)

        pageData = base.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return base.successData(pageData)

    '''
    添加指纹信息
    '''
    def addInfo(request):

        app = models.Apps.objects.get(id=request.POST.get('appId'))

        models.Fingers.objects.create(
            key=request.POST.get('key'),
            location=request.POST.get('location'),
            app=app,
            createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

        return base.success()

    '''
    修改指纹信息
    '''
    def updInfo(request):

        models.Fingers.objects.filter(id=request.POST.get('id')) \
            .update(
            key=request.POST.get('key'),
            location=request.POST.get('location'),
            app=models.Apps.objects.get(id=request.POST.get('appId'))
        )

        return base.success()

    '''
    删除指纹信息
    '''
    def delInfo(request):

        models.Fingers.objects.filter(id=request.POST.get('id')).delete()

        return base.success()

'''
系统扫描处理
'''
class ScanView(View):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return ScanView.getFingerInfo(request)
        else:
            return base.error()

    def getFingerInfo(request):

        url = request.GET.get('url')

        finger = scan.getWebInfo(url)

        return base.successData(finger)
