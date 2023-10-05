from django import forms


class UserQuestionForm(forms.Form):
    """
    Form for user questions.

    Allows users to input their questions.

    :param forms.Form: Form for user questions.
    """
    user_question = forms.CharField(max_length=255, label='Your Question')

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['message']
