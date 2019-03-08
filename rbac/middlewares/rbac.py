import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from permission_learn import settings


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        white_list = settings.WHITE_LIST
        current_path = request.path_info

        for valid_url in white_list:
            if re.match(valid_url, current_path):
                return None

        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_list:
            return HttpResponse('请先登录')

        has_permission = False

        for url in permission_list:
            reg = '^%s$' % url
            if re.match(reg, current_path):
                has_permission = True
                break

        if not has_permission:
            return HttpResponse('未获取权限，请先获取权限')
