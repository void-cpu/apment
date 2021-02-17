from django.db import models

from urith.baseModels import BaseMode


class UserModels(BaseMode):
    UserName = models.CharField(max_length=20, verbose_name='用户名', null=True)
    UserPwd = models.CharField(max_length=30, verbose_name='用户密码')
    phone = models.CharField(max_length=20, unique=True, verbose_name='用户的手机号密码')

    class Meta:
        db_table = 'uneatable'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
