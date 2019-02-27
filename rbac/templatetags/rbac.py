from collections import OrderedDict

from django.template import Library
from django.conf import settings

register = Library()


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    menu_dict = request.session[settings.MENU_SESSION_KEY]

    print(request.current_selected_permission)

    # 对字典的key进行排序
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for second_menu in val['children']:
            # second_menu['id']和current_selected_permission存的都是当前点击的二级菜单的一级菜单的id
            if second_menu['id'] == request.current_selected_permission:
                second_menu['class'] = 'active'
                val['class'] = ''

        ordered_dict[key] = val
    return {'menu_dict': ordered_dict}
