import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from permission_learn import settings


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):

        white_list = settings.WHITE_LIST

        current_path = request.path

        for valid_url in white_list:
            if re.match(valid_url, current_path):
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_dict:
            return HttpResponse('请先登录 ')

        has_permission = False

        url_record = [
            {'title': '首页', 'url': '#'}
        ]
        for item in permission_dict.values():
            regex = '^%s$' % item['url']
            if re.match(regex, current_path):
                has_permission = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:  # 选中的是二级菜单
                    url_record.extend([
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                else:  # 选中的是具体权限
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.breadcrumb = url_record  # 通过request，把储存信息传给用户
                break

        if not has_permission:
            return HttpResponse('未获取权限，请先获取权限')
