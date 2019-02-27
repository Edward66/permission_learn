from django.conf import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user:当前用户对象
    :param request:请求相关所有数据
    :return:
    """
    permission_menu_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                           'permissions__title',
                                                                                           'permissions__url',
                                                                                           'permissions__menu_id',
                                                                                           'permissions__menu__title',
                                                                                           'permissions__menu__icon'
                                                                                           ).distinct()

    # 3.获取权限 + 菜单信息

    permission_list = []
    menu_dict = {}
    for item in permission_menu_queryset:
        permission_list.append(item['permissions__url'])

        menu_id = item['permissions__menu_id']

        if not menu_id:
            continue

        node = {'title': item['permissions__title'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ]
            }
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict
