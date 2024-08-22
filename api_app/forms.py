from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
#LANGUAGE_CODE = 'pt-br'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'address', 'phone', 'password1', 'password2')
        labels = {
            'username': 'Nome de Usuário alterado:',
            'email': 'E-mail alterado:',
            'address': 'Endereço alterado:',
            'phone': 'Telefone alterado :',
            'password1': 'Senha Alterada:',
            'password2': 'Confirmação de Senha: Alterada',
        }
        help_texts = {
            'username': "",
        }

        error_messages = {
            'username': {
                'required': 'Por favor, insira um nome de usuário.',
                'max_length': 'O nome de usuário não pode ter mais que 150 caracteres.',
                'invalid': 'Use apenas letras, números e os caracteres @/./+/-/_ para o nome de usuário.',
            },
            'email': {
                'required': 'Por favor, insira um endereço de e-mail válido.',
            },
            'password': {
                'required': 'Por favor, insira uma senha.',
                'password_too_similar': 'Sua senha não pode ser muito parecida com suas outras informações pessoais.',
                'password_too_short': 'Sua senha deve ter pelo menos 8 caracteres.',
                'password_too_common': 'Sua senha é muito comum.',
                'password_entirely_numeric': 'Sua senha não pode ser inteiramente numérica.',
            },
            'password2': {
                'required': 'Por favor, confirme sua senha.',
                'password_mismatch': 'As senhas inseridas não correspondem.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'address', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'