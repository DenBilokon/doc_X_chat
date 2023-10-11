from users.models import Avatar


def avatar_url(request):
    """
    The avatar_url function is a context processor that adds the avatar_url variable to all templates.
        This allows us to display the user's avatar in any template by simply using {{avatar_url}}.
    
    :param request: Get the user id of the current logged in user
    :return: The url of the avatar image
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return {'avatar_url': avatar.image.url if avatar else None}
