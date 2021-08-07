import random

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from urith.Response import BaseResponse
from urith.ResponseMessage import ResponseMessage
from .serializers import *


class BasePublishViewSet:
    class SameCode:
        def __init__(self, first_pass, second_pass):
            self.first_pass = first_pass
            self.second_pass = second_pass

        @property
        def is_same_code(self):
            return self.first_pass.__str__() == self.second_pass.__str__()

    class None_Dict_value:
        def __init__(self,*args):
            self.args = args

        @property
        def None_Dict_value_Is(self):
            return all(list(self.args))


class UserViewSets(ModelViewSet):
    queryset = UserModels.objects.all()
    serializer_class = UserListSerializers
    # pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = {"UserName": ["exact", "in", "contains"], "phone": ["exact", "contains"]}

    # {"UserName": ['exact', 'lt', 'gt', "in", "contains"], "phone": ['exact', 'lt', 'gt', "in", "contains"]}

    def create(self, request, *args, **kwargs):
        password = request.data['UserPwd'] if 'UserPwd' in request.data else None
        password = make_password(password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(UserPwd=password)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def set_password(self, request, pk=None):
        """
        :param request: - { "phone": "user phone","password": "user password","userNewPassword": "user new password","userNewAgentPassword":"user new password"},
        :param pk:
        :return:
        """
        phone = request.data.get("phone")
        password, userNewPassword, userNewAgentPassword = request.data.get('password'), \
                                                          request.data.get("userNewPassword"), \
                                                          request.data.get("userNewAgentPassword")
        if BasePublishViewSet.None_Dict_value(password, userNewPassword, userNewAgentPassword, phone).None_Dict_value_Is:
            if BasePublishViewSet.SameCode(first_pass=userNewPassword, second_pass=userNewAgentPassword).is_same_code:
                try:
                    _object = UserModels.objects.get(phone=phone)
                    if check_password(password, _object.UserPwd):
                        _object.UserPwd = make_password(userNewPassword)
                        _object.save()
                        return Response(UserListSerializers(_object, many=False).data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(BaseResponse(Message=ResponseMessage.PassWordError.value).__str__(),
                                        status=status.HTTP_404_NOT_FOUND)
                except UserModels.DoesNotExist:
                    return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(BaseResponse(Message=ResponseMessage.PassWordErrorMessage.value).__str__(),
                                        status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                            status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializers
        elif self.action == 'update':
            return UserUpdateSerializers
        else:
            return UserListSerializers

    @action(methods=['post'], detail=True)
    def login(self, request, pk=None):
        """
        - request {"username":"user phone", password="user password"}
        """
        username, password = request.data.get("username"), request.data.get("password")
        if BasePublishViewSet.None_Dict_value(username,password).None_Dict_value_Is:
            return Response(BaseResponse(Message=ResponseMessage.NullMessage.value).__str__(),
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            _object = UserModels.objects.get(user_name=username)
        except UserModels.DoesNotExist:
            return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                            status=status.HTTP_404_NOT_FOUND)
        if check_password(password, _object.pass_word):
            return Response(UserListSerializers(_object, many=False).data, status=status.HTTP_200_OK)
        else:
            return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                            status=status.HTTP_404_NOT_FOUND)

    @action(methods=["get", "post"], detail=True)
    def PhoneCode(self, request, pk=None):
        """
        get:得到手机验证码 request {"Phone": Phone}
        post:手机验证码验证 request {"Phone": Phone, "PhoneCode_01": GetPhoneCode, "PhoneCode_02":SetPhoneCode}
        """
        if request.method == "GET":
            Phone = request.data.get('Phone')
            if not BasePublishViewSet.None_Dict_value(Phone).None_Dict_value_Is:
                return Response(BaseResponse(Message=ResponseMessage.NullMessage.value).__str__(),
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                code = random.randint(10000, 999999)
                cache.set(Phone, code, 60)
                return Response(BaseResponse(Message="successfully", Phone=Phone).__str__(),
                                status=status.HTTP_200_OK)
        elif request.method == "POST":
            Phone = request.data.get('Phone')
            PhoneCode = request.data.get("PhoneCode")
            if not BasePublishViewSet.SameCode(Phone,PhoneCode).is_same_code:
                return Response(BaseResponse(Message=ResponseMessage.NullMessage.value).__str__(),
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                PhoneodeRedis = str(cache.get(Phone)) if cache.has_key(Phone) else str(None)
                return Response(BaseResponse(Message=ResponseMessage.Code(
                    is_True=BasePublishViewSet.SameCode(str(PhoneCode), PhoneodeRedis.__str__())).__str__(),
                                             Phone=Phone).__str__(),
                                status=status.HTTP_401_UNAUTHORIZED)
