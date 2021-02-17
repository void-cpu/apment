# -*- coding: utf-8 -*-
# @Time    : 2021/2/17 下午4:04
# @Author  : void bug
# @FileName: serializers.py
# @Software: PyCharm
from rest_framework import serializers

from .models import UserModels


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModels
        fields = '__all__'


class UserCreateSerializers(UserListSerializers):
    UserName = serializers.ReadOnlyField(read_only=True)


class UserUpdateSerializers(UserListSerializers):
    UserPwd = serializers.ReadOnlyField(read_only=True)
