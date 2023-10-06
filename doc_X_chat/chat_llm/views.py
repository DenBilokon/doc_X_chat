from django.shortcuts import render

# from doc_X_chat.users.models import Avatar


def main(request):

    # avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return render(request, 'chat_llm/index.html', context={})
