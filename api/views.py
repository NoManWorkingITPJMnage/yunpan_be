from django.http import HttpResponse, HttpResponseRedirect
import json
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as djUser
from django.views.decorators.csrf import csrf_exempt
from .models import User, Folder, Data
import os
import socket
import zipfile
import datetime, time
from yunpan.settings import DATA_FILE_PATH, TMP_FILE_PATH, HTTP_URL, PORT, DATA_FILE_URL, TMP_FILE_URL


# Create your views here.

def quick_respone(ret = 200, dic = None):
    return HttpResponse(status=ret ,content=json.dumps(dic), content_type = 'application/json,charset=utf-8')


@login_required()
@csrf_exempt
def content(request):
    # 更新与获得用户信息

    user_name = request.user.username
    try:
        user = User.objects.get(user_name=user_name)
    except User.DoesNotExist:
        return quick_respone(404)

    if request.method == 'PUT':
        # 更新用户信息
        body_data = json.loads(request.body)
        user.user_name = body_data.get('user_name')
        user.real_name = body_data.get('real_name')
        user.student_id = body_data.get('student_id')
        user.gender = body_data.get('gender')
        user.user_class = body_data.get('class')
        user.phone = body_data.get('phone')
        user.mail = body_data.get('mail')
        user.save()
        return quick_respone()
    elif request.method == 'GET':
        # 返回用户信息
        ret_dict = dict()
        ret_dict['user_name'] = user.user_name
        ret_dict['real_name'] = user.real_name
        ret_dict['gender'] = user.gender
        ret_dict['student_id'] = user.student_id
        ret_dict['class'] = user.user_class
        ret_dict['mail'] = user.mail
        ret_dict['phone'] = user.phone
        return quick_respone(dic=ret_dict)
    return quick_respone(403)

@csrf_exempt
def login(request):
    # 登录

    if request.method != 'POST':
        return quick_respone(403)

    if request.user.is_anonymous:
        body_data = json.loads(request.body)
        user_name = body_data.get('user_name')
        password = body_data.get('password')
        user = auth.authenticate(username = user_name, password = password)
        if not user:
            return quick_respone(ret = 401, dic={'message':'用户名或密码错误'})
        else:
            auth.login(request, user)
            return quick_respone()
    else:
        return quick_respone()


@csrf_exempt
def register(request):
    # 注册
    
    if request.method != 'POST':
        return quick_respone(403)

    body_data = json.loads(request.body)
    user_name = body_data.get('user_name')
    real_name = body_data.get('real_name')
    student_id = body_data.get('student_id')
    password = body_data.get('password')

    if not user_name or not real_name or not student_id or not password:
        return quick_respone(ret = 403)

    try:
        user = User.objects.get(user_name=user_name)
        return quick_respone(ret=409, dic={'message': '用户名已存在'})
    except User.DoesNotExist:
        user = None

    try:
        user = User.objects.get(student_id=student_id)
        return quick_respone(ret=409, dic={'message': '学号已存在'})
    except User.DoesNotExist:
        user = None

    user = User()
    user.user_name= user_name
    user.password = password
    user.real_name = real_name
    user.student_id = student_id
    user.save()

    djUser.objects.create_user(username=user_name, password=password)

    return quick_respone()

@csrf_exempt
@login_required()
def folders(request):
    # 文件夹操作
    
    if request.method == 'GET':
        # 返回所有文件夹
        folders = Folder.objects.all()
        ret_list = []
        for folder in folders:
            item = dict()
            item['id'] = folder.id
            item['folder_name'] = folder.folder_name
            item['creator'] = folder.creator
            ret_list.append(item)
        return quick_respone(dic=ret_list)
    elif request.method == 'POST':
        # 创建一个文件夹
        body_data = json.loads(request.body)
        folder_name = body_data.get('folder_name')
        if not folder_name:
            return quick_respone(400)

        folder_path = os.path.join(DATA_FILE_PATH, folder_name)
        if os.path.exists(folder_path):
            return quick_respone(400)

        try:
            folder = Folder.objects.get(folder_name=folder_name)
            return quick_respone(409)
        except Folder.DoesNotExist:
            folder = None

        os.makedirs(folder_path)
        if not os.path.exists(folder_path):
            return quick_respone(400)

        user_name = request.user.username
        folder = Folder()
        folder.folder_name = folder_name
        folder.creator = user_name
        folder.save()

        return quick_respone()
    return quick_respone(403)

@csrf_exempt
@login_required()
def resources(request):
    # 资源操作
    
    if request.method == 'GET':
        user = request.GET.get('user', None)
        res_id = request.GET.get('res_id', None)
        if user:
            # 根据用户筛选资源
            ret_list = []
            if user == 'all':
                datas = Data.objects.filter(approved=True)
            else:
                datas = Data.objects.filter(uploader=user)
            for data in datas:
                item = dict()
                item['res_id'] = data.id
                item['res_name'] = data.res_name
                item['folder_name'] = data.folder_name
                item['uploader'] = data.uploader
                item['link'] = '%s:%s%s%s/%s' % (
                HTTP_URL, PORT, DATA_FILE_URL, data.folder_name, data.res_name)
                ret_list.append(item)
            return quick_respone(dic=ret_list)
        elif res_id:
            # 返回指定id的资源
            try:
                data = Data.objects.get(id = res_id)
            except Data.DoesNotExist:
                return quick_respone(404)
            item = dict()
            item['res_id'] = data.id
            item['res_name'] = data.res_name
            item['folder_name'] = data.folder_name
            item['uploader'] = data.uploader
            item['link'] = '%s:%s%s%s/%s' % (
            HTTP_URL, PORT, DATA_FILE_URL, data.folder_name, data.res_name)
            return quick_respone(dic=item)
        return quick_respone(403)

    elif request.method == 'POST':
        # 上传资源
        
        res_file = request.FILES.get('file', None)
        if not res_file:
            return quick_respone(403)

        file_name = res_file.name
        folder_id = request.POST.get('folder_id', None)
        if not folder_id:
            return quick_respone(403)

        try:
            folder = Folder.objects.get(id = folder_id)
        except Folder.DoesNotExist:
            return quick_respone(400)

        try:
            res = Data.objects.get(folder_name=folder.folder_name, res_name=file_name)
            return quick_respone(400)
        except Data.DoesNotExist:
            res = None

        file_path = os.path.join(DATA_FILE_PATH, folder.folder_name, file_name)
        if os.path.exists(file_path):
            return quick_respone(409)

        with open(os.path.join(DATA_FILE_PATH, folder.folder_name, file_name), 'wb') as f:
            for line in res_file.chunks() :
                f.write(line)
        res = Data()
        res.uploader = request.user.username
        res.folder_name = folder.folder_name
        res.res_name = file_name
        res.approved = False
        res.save()

        return quick_respone()
    return quick_respone(403)

@csrf_exempt
@login_required()
def logout(request):
    # 登出
    if request.method != 'POST':
        return quick_respone(403)

    auth.logout(request)
    return quick_respone()

@csrf_exempt
@login_required()
def folder(request):
    # 文件夹的详情
    if request.method != 'GET':
        return quick_respone(403)

    folder_id = request.GET.get('folder_id', None)
    if not folder_id:
        return quick_respone(403)

    try:
        folder = Folder.objects.get(id = folder_id)
    except Folder.DoesNotExist:
        return quick_respone(404)

    ret_dict = dict()
    ret_dict['folder_name'] = folder.folder_name
    ret_dict['creator'] = folder.creator
    ret_dict['resources'] = []
    datas = Data.objects.filter(folder_name=folder.folder_name)
    for data in datas:
        item = dict()
        item['res_id'] = data.id
        item['res_name'] = data.res_name
        item['folder_name'] = data.folder_name
        item['uploader'] = data.uploader
        item['link'] = '%s:%s%s%s/%s' % (
            HTTP_URL, PORT, DATA_FILE_URL, data.folder_name, data.res_name)
        ret_dict['resources'].append(item)
    return quick_respone(dic=ret_dict)

@csrf_exempt
@login_required()
def folder_download(request):
    # 文件夹打包下载
    if request.method != 'GET':
        return quick_respone(403)
    username = request.user.username

    folder_id = request.GET.get('folder_id', None)
    if not folder_id:
        return quick_respone(403)

    try:
        folder = Folder.objects.get(id = folder_id)
    except Folder.DoesNotExist:
        return quick_respone(404)

    time_str = datetime.datetime.now().strftime('%Y%m%d')
    zip_file_path = os.path.join(TMP_FILE_PATH, '%s_%s_%s.zip' % (time_str, username, folder.folder_name))
    folder_path = os.path.join(DATA_FILE_PATH, folder.folder_name)

    zipf = zipfile.ZipFile(zip_file_path, 'w')
    pre_len = len(os.path.dirname(folder_path))
    for parent, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

    download_url = '%s:%s%s%s' % (
        HTTP_URL, PORT, TMP_FILE_URL, '%s_%s_%s.zip' % (time_str, username, folder.folder_name))

    return quick_respone(dic={'file':download_url})
