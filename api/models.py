from django.db import models

# Create your models here.

class User(models.Model):
    # 用户信息
    user_name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    student_id = models.CharField(max_length=128, unique=True)
    school = models.CharField(max_length=256)
    real_name = models.CharField(max_length=128, default='')
    mail = models.EmailField()
    gender = models.CharField(max_length=32)
    phone = models.CharField(max_length=256)
    user_class = models.CharField(max_length=128, default='')


class Folder(models.Model):
    # 文件夹信息
    folder_name = models.CharField(max_length=256, unique=True)
    creator = models.CharField(max_length=128)

class Data(models.Model):
    # 文件信息
    res_name = models.CharField(max_length=256)
    folder_name = models.CharField(max_length=256)
    uploader = models.CharField(max_length=128)
    approved = models.BooleanField(default=False)