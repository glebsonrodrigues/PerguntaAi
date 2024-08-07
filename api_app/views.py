# api_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json

@login_required
def index(request):
    result = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            url = 'http://192.168.0.192:22500/v1/completions'
            
            data = {
                "model": "llama-2-7b-chat.Q8_0.gguf",
                "prompt": prompt,
                "best_of": 1,
                "echo": True,
                "frequency_penalty": 0,
                "logit_bias": {},
                "logprobs": 0,
                "max_tokens": 20,
                "n": 1,
                "presence_penalty": 0,
                "stop": ["FIMDARESPOSTA"],
                "stream": False,
                "suffix": "|FIM DA RESPOSTA|",
                "temperature": 1,
                "top_p": 1,
                "user": "string",
                "preset": " ",
                "min_p": 0,
                "dynamic_temperature": False,
                "dynatemp_low": 1,
                "dynatemp_high": 1,
                "dynatemp_exponent": 1,
                "smoothing_factor": 0,
                "smoothing_curve": 1,
                "top_k": 0,
                "repetition_penalty": 1,
                "repetition_penalty_range": 1024,
                "typical_p": 1,
                "tfs": 1,
                "top_a": 0,
                "epsilon_cutoff": 0,
                "eta_cutoff": 0,
                "guidance_scale": 1,
                "negative_prompt": "",
                "penalty_alpha": 0,
                "mirostat_mode": 0,
                "mirostat_tau": 5,
                "mirostat_eta": 0.1,
                "temperature_last": False,
                "do_sample": True,
                "seed": -1,
                "encoder_repetition_penalty": 1,
                "no_repeat_ngram_size": 0,
                "dry_multiplier": 0,
                "dry_base": 1.75,
                "dry_allowed_length": 2,
                "dry_sequence_breakers": "\"\\n\", \":\", \"\\\"\", \"*\"",
                "truncation_length": 0,
                "max_tokens_second": 0,
                "prompt_lookup_num_tokens": 0,
                "custom_token_bans": "",
                "sampler_priority": ["string"],
                "auto_max_new_tokens": False,
                "ban_eos_token": False,
                "add_bos_token": True,
                "skip_special_tokens": True,
                "grammar_string": ""
            }

            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.post(url, data=json.dumps(data), headers=headers)
            
            # Verifica se a resposta é bem-sucedida
            if response.status_code == 200:
                response_data = response.json()
                
                # Extrai o texto da resposta
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    result = response_data['choices'][0].get('text', 'Nenhuma resposta recebida.')
                else:
                    result = 'Nenhuma escolha encontrada na resposta da API.'
            else:
                result = f'Erro ao chamar a API: {response.status_code}'

        else:
            result = 'Nenhuma pergunta fornecida.'
    
    return render(request, 'api_app/index.html', {'result': result})
