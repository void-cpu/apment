# -*- coding: utf-8 -*-
# @Time    : 2021/2/13 上午2:18
# @Author  : void bug
# @FileName: Pagination.py
# @Software: PyCharm
from rest_framework import pagination


class BasePagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 1000e122222
