from permission_learn import settings


def init_permission(current_user, request):
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values(
        'permissions__id',
        'permissions__url'
    )

    permission_list = [item['permissions_url'] for item in permission_queryset]

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list


