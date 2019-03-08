import re
from collections import OrderedDict

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    创建一级菜单
    :param request:
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    current_path = request.path

    for item in menu_list:
        reg = '^%s$' % item['url']
        if re.match(reg, current_path):
            item['class'] = 'active'

    # menu函数里面的返回值是返回到 rbac/templates/rbac/menu.html
    # menu函数里面的返回值也可以说是返回到inclusion_tag所指向的模版路径
    context = {
        'menu_list': menu_list,
        'current_path': current_path
    }

    return context


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    menu_dict = request.session[settings.MENU_SESSION_KEY]

    # 对字典的key进行排序。得到的结果是只包含Key的列表，类似这样的 [1,2,3]
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()  # 有序字典，按照我们想要的顺序展示
    current_path = request.path
    for key in key_list:
        second_menu = menu_dict[key]  # {'title':'客户管理','icon':'fa fa-book','children':[二级菜单1,二级菜单2,...]}
        second_menu['class'] = 'hide'  # 隐藏二级菜单
        for permission in second_menu['children']:
            regex = '^%s$' % (permission['url'])
            if re.match(regex, current_path):
                permission['class'] = 'active'
                second_menu['class'] = ''  # 显示点中的二级菜单

        ordered_dict[key] = second_menu

    context = {
        'second_menu': ordered_dict
    }

    return context
