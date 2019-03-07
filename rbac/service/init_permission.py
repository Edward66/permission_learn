from permission_learn import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user:  当前登录用户
    :param request:
    :return:
    """
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values(
        'permissions__id',
        'permissions__title',
        'permissions__is_menu',
        'permissions__icon',
        'permissions__url'
    )

    # 获取权限 + 菜单信息

    menu_list = []
    permission_list = []
    for item in permission_queryset:
        permission_list.append(item['permissions__url'])  # 权限
        if item['permissions__is_menu']:
            menu_info = {
                'title': item['permissions__title'],
                'icon': item['permissions__icon'],
                'url': item['permissions__url'],
            }
            menu_list.append(menu_info)  # 菜单

    # 将权限信息和菜单信息放入到session中
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_list
