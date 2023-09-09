import streamlit as st
import requests
import pandas as pd

# Função para testar a conexão com a API
def test_api_connection(access_token):
    if not access_token:
        return "Token de acesso vazio. Por favor, insira um token válido."

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'app_token': 'f3079a0b-a2d5-4eec-9d32-5eb0c2887b17',
        'access_token': access_token
    }

    api_url = 'http://apps.superlogica.net/imobiliaria/api/contratos'  # Substitua pelo URL da sua API

    try:
        response = requests.get(api_url, headers=headers).json()
        contratos = pd.DataFrame(response['data'])

        if isinstance(contratos, pd.DataFrame):
            st.session_state['access_token'] = access_token
            return "Conexão com a API bem-sucedida!"
        else:
            return f"Falha na conexão com a API, tente novamente."
    except Exception as e:
        return f"Erro ao se conectar à API, tente novamente."

# Interface do usuário com Streamlit
def conectaAPIsuperlogica():
    access_token = st.text_input("Digite o token de acesso:")

    if st.button("Testar Conexão"):
        result = test_api_connection(access_token)
        st.write(result)

st.header("Conecte sua licença do Superlógica")
st.write("#### Instruções")
st.write('Passo 1: Na sua licença do Superlógica, clique no canto superior direito, no seu nome de usuário. Depois, clique em Todos os usuários.')
st.write('Passo 2: Desça até a parte inferior da página em API (INTEGRAÇÃO COM OUTRAS PLATAFORMAS), clique em Aplicativos liberados e depois em Liberar aplicativo.')
st.write('Passo 4: Uma janela aparecerá na tela, e nela, você deve clicar em Outro aplicativo, logo abaixo de Meu aplicativo')
st.write('Passo 5: Agora, insira o App Token f3079a0b-a2d5-4eec-9d32-5eb0c2887b17 e clique em liberar')
st.write('Passo 6: Retornando à página de aplicativos liberados, encontre nosso aplicativo na lista e clique em Ver Access Token (essa opção só aparece quando colocamos o mouse sobre a linha do App')
st.write('Passo 7: Copie o Access Token e cole aqui embaixo. Por fim, clique em Testar Conexão. Caso dê certo, uma mensagem irá aparecer e você poderá acessar suas análises.')

if 'access_token' not in st.session_state:
    conectaAPIsuperlogica()
else:
    st.write("Licença já conectada")
