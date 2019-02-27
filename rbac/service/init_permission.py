from permission_learn import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user:当前用户对象
    :param request:请求相关所有数据
    :return:
    """
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                      'permissions__url').distinct()
    permission_list = [item['permissions_url'] for item in permission_queryset]
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
