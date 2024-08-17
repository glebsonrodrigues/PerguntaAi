from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Certifique-se de que está correto
import requests
import json
import os

# Função para carregar o JSON de configuração
def load_json_config():
    config_path = os.path.join('config', 'api_config.json')
    with open(config_path, 'r') as file:
        return json.load(file)

# Página inicial
@login_required
def index(request):
    response_text = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            # Carregar a configuração JSON
            config = load_json_config()
            config["prompt"] = prompt
            
            # Enviar solicitação para a API
            response = requests.post('http://187.103.205.100:22500/v1/completions', json=config)
            response_data = response.json()
            
            # Processar a resposta da API
            response_text = response_data.get('choices', [{}])[0].get('text', '')

    return render(request, 'api_app/index.html', {'response_text': response_text})

# Página de registro de usuário
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use o nome correto aqui
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()  # Use o nome correto aqui
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
