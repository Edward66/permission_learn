import re

from django.template import Library

from django.conf import settings

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
