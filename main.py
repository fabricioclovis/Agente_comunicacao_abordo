import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# 1. Verificação de Sistemas: Capturando a API Key do ambiente (Render)
# No Render, você configurará a variável de ambiente GROQ_API_KEY
API_KEY = os.environ.get("GROQ_API_KEY")

# Inicializando o cliente Groq se a chave estiver presente
if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    st.error("⚠️ Alerta de Sistema: GROQ_API_KEY não encontrada nas variáveis de ambiente.")

def atualizar_memoria_longo_prazo(resumo_atual, novas_mensagens):
    """
    Função do copiloto para condensar a janela deslizante de mensagens.
    """
    prompt_sistema = """
    Você é um copiloto especialista em síntese de dados e gestão de contexto para sistemas de IA.
    REGRAS DE SÍNTESE:
    1. Extraia apenas fatos, decisões tomadas, dados técnicos citados e intenções do usuário.
    2. Elimine saudações, conversas fiadas e redundâncias.
    3. Se o usuário mudou de assunto, registre explicitamente o novo foco do estado atual.
    
    FORMA DE SAÍDA:
    Um texto em tópicos curtos (máximo 3 a 4 linhas) representando o estado consolidado da conversa.
    """
    
    conteudo_usuario = f"RESUMO ATUAL:\n{resumo_atual}\n\nNOVAS MENSAGENS DESCARTADAS PELA JANELA:\n{novas_mensagens}"

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": conteudo_usuario}
            ],
            model="llama3-70b-8192", # Modelo otimizado da Groq para análise rápida
            temperature=0.2, # Baixa temperatura para manter precisão factual e técnica
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro nos instrumentos de comunicação: {e}"

# 2. Interface do Painel de Controle (Streamlit)
st.set_page_config(page_title="Gestão de Contexto de Voo", page_icon="✈️")
st.title("✈️ Painel de Síntese de Memória de Bordo")

# Inicializando estados da sessão (nossa caixa preta de dados)
if "resumo_memoria" not in st.session_state:
    st.session_state.resumo_memoria = "Nenhum histórico de voo anterior."
if "mensagens_recentes" not in st.session_state:
    st.session_state.mensagens_recentes = ""

st.subheader("Estado Atual da Memória de Longo Prazo")
st.info(st.session_state.resumo_memoria)

st.subheader("Entrada de Dados da Janela Deslizante")
novas_mensagens_input = st.text_area("Insira as mensagens descartadas pela janela recente para condensação:")

if st.button("🔄 Processar e Condensar Memória"):
    if novas_mensagens_input and API_KEY:
        with st.spinner("Analisando logs de voo..."):
            novo_resumo = atualizar_memoria_longo_prazo(
                st.session_state.resumo_memoria, 
                novas_mensagens_input
            )
            st.session_state.resumo_memoria = novo_resumo
            st.success("Memória atualizada com sucesso!")
            st.rerun()
    elif not novas_mensagens_input:
        st.warning("Insira mensagens de log para processar.")
