import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from permission_learn import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当前用户请求刚进入时候触发执行
        :param request:
        :return:
        """
        white_list = settings.WHITE_LIST
        current_url = request.path_info
        for valid_url in white_list:
            if re.match(valid_url, current_url):
                # 白名单的url不用进行权限验证
                return None
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return HttpResponse(settings.NOT_LOG_IN)

        flag = False

        for url in permission_list:
            reg = "^%s$" % url
            if re.match(reg, current_url):
                flag = True
                break

        if not flag:
            return HttpResponse(settings.DENIED_INFO)
