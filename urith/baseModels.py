# -*- coding: utf-8 -*-
# @Time    : 2021/2/17 下午3:55
# @Author  : void bug
# @FileName: baseModels.py
# @Software: PyCharm
from django.db import models


class BaseMode(models.Model):
    """基本模板类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间", help_text="最后修改时间")

    class Meta:
        abstract = True
