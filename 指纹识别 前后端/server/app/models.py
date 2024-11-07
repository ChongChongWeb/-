from django.db import models

'''
用户信息
类型：
    0 系统管理员
    1 普通管理员
'''
class Users(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    userName = models.CharField('用户账号',  db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码',  db_column='pass_word', max_length=32, null=False)
    name = models.CharField('用户姓名', max_length=20, null=False)
    gender = models.CharField('用户性别', max_length=4, null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    type = models.IntegerField('用户身份', null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_users'

'''
应用信息
类型：
    0 CMS
    1 前端技术框架
    2 服务器
    3 其他
'''
class Apps(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('应用名称',  max_length=32, null=False)
    type = models.IntegerField('应用类型', null=False)
    details = models.CharField('应用描述',  max_length=256, null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_apps'

'''
指纹信息
位置：
    0 title
    1 header
    2 body
'''
class Fingers(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    key = models.CharField('关键信息',  max_length=256, null=False)
    location = models.IntegerField('所在位置',  null=False)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE, db_column='app_id')
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_fingers'
