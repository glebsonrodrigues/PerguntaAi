from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Certifique-se de que está correto
import requests
import json
import os
from django.conf import settings

# Função para carregar o JSON de configuração
def load_json_config():
    config_path = os.path.join(settings.BASE_DIR, 'config', 'api_config.json')
    with open(config_path, 'r') as file:
        return json.load(file)

# Página inicial com chat
@login_required
def index(request):
    response_text = ''
    chat_history = request.session.get('chat_history', [])  # Recuperar histórico do chat da sessão

    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            config = load_json_config()
            config["prompt"] = prompt
            
            try:
                # Enviar solicitação para a API
                response = requests.post('http://187.103.205.100:22500/v1/completions', json=config)
                response.raise_for_status()  # Levantar exceção se houver erro
                response_data = response.json()

                # Processar a resposta da API
                response_text = response_data.get('choices', [{}])[0].get('text', '')

                # Adicionar ao histórico de chat
                chat_history.append({'user': True, 'text': prompt})
                chat_history.append({'user': False, 'text': response_text})
                request.session['chat_history'] = chat_history  # Salvar histórico na sessão

            except requests.exceptions.RequestException as e:
                response_text = "Erro ao se comunicar com a API: " + str(e)

    return render(request, 'api_app/index.html', {'chat_history': chat_history})

# Página de registro de usuário
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Formulário de registro personalizado
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api_app/pages/register/register.html', {'form': form})

# Página de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'api_app/pages/login/login.html', {'form': form})

# Função de logout
def logout_view(request):
    auth_logout(request)
    return redirect('/')
