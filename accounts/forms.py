from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(label='メールアドレス', required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and email:
            try:
                user = User.objects.get(username=username)
                if user.email != email:
                    raise forms.ValidationError("ユーザー名とメールアドレスが一致しません。")
            except User.DoesNotExist:
                raise forms.ValidationError("ユーザーが存在しません。")

        return cleaned_data
