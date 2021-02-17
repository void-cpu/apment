# -*- coding: utf-8 -*-
# @Time    : 2021/2/17 下午4:16
# @Author  : void bug
# @FileName: urls.py
# @Software: PyCharm
from rest_framework.routers import DefaultRouter

from app.user_App.views import UserViewSets

routers = DefaultRouter()
routers.register("user", UserViewSets, basename="UserViewSets")
