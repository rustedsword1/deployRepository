from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import password_validators_help_texts

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=_('ユーザー名は半角英数字および @/./+/-/_ のみ使用できます。'),
            )
        ],
        error_messages={
            'required': _('この項目は必須です。'),
            'max_length': _('ユーザー名は20文字以内で入力してください。'),
        },
        widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'form-control'}),
        label='ユーザー名',
    )

    class Meta:
        model = User
        fields = ['username', 'email']


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label="ユーザー名",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
        error_messages={
            'required': 'ユーザー名を入力してください。',
            'max_length': 'ユーザー名は20文字以内で入力してください。',
        },
    )
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="パスワード",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username and email and password:
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                raise forms.ValidationError(_("ユーザー名またはメールアドレスが正しくありません。"))

            self.user_cache = authenticate(username=user.username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(_("パスワードが正しくありません。"))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("このアカウントは無効です。"))

        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='ユーザー名',
        max_length=20,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=_('ユーザー名は半角英数字および @/./+/-/_ のみ使用できます。'),
            )
        ],
        error_messages={
            'required': 'ユーザー名は必須です。',
            'max_length': 'ユーザー名は20文字以内で入力してください。',
        },
    )

    email = forms.EmailField(label='メールアドレス', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['password1'].help_text = '<br>'.join(password_validators_help_texts())
        self.fields['username'].widget.attrs['maxlength'] = 20

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 20:
            raise ValidationError(_('ユーザー名は20文字以内で入力してください。'))
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(_('パスワードが一致しません。'))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user