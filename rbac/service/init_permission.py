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
        'permissions__pid_id',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    )




    permission_list = []

    menu_dict = {}

    for item in permission_menu_queryset:
        permission_list.append(
            {'id': item['permissions__id'], 'url': item['permissions__url'], 'pid': item['permissions__pid_id']},
        )



        menu_id = item['permissions__menu_id']

        if not menu_id:
            continue

        second_menu = {'id': item["permissions__id"], 'title': item['permissions__title'],
                       'url': item['permissions__url']}

        if menu_id in menu_dict:
            menu_dict[menu_id]['second_menu'].append(second_menu)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'second_menu': [second_menu, ]
            }

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict
