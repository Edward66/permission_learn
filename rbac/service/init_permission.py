from permission_learn import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user:  当前登录用户
    :param request:
    :return:
    """
    permission_menu_queryset = current_user.roles.filter(permissions__isnull=False).values(
        'permissions__id',
        'permissions__title',
        'permissions__url',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    ).distinct()

    # 获取权限 + 菜单信息

    permission_list = []
    menu_dict = {}
    for item in permission_menu_queryset:
        permission_list.append(item['permissions__url'])  # 权限

        menu_id = item['permissions__menu_id']  # 一级菜单的id

        if not menu_id:  # 如果没有menu_id，就说明它不能作为二级菜单，这不是我们需要的。
            continue

        permission = {'title': item['permissions__title'], 'url': item['permissions__url']}

        if menu_id in menu_dict:  # 一级菜单和二级菜单是一对多的关系，如果不判断的话，会出现多个重复的一级菜单
            menu_dict[menu_id]['children'].append(permission)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [permission, ]
            }
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict


"""
客户列表	/customer/list/  1  ForeignKey -->  1 客户管理  fa-hdd-o
    添加客户	/customer/add/  null
    编辑客户	/customer/edit/(?P<cid>\d+)/  null
    删除客户	/customer/del/(?P<cid>\d+)/  null

账单列表	/payment/list/  2  ForeignKey --> 2 账单管理  fa-heart
    添加账单	/payment/add/  null
    编辑账单	/payment/edit/(?P<pid>\d+)/  null
    删除账单	/payment/del/(?P<pid>\d+)/  null
"""
