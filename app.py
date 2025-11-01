# app.py
import streamlit as st
import google.generativeai as genai
import time

def configurar_ia():
    """
    Configura a API do Gemini usando a chave armazenada nos Secrets do Streamlit.
    """
    # Acessando a chave de API dos "Secrets" do Streamlit
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        return True
    except KeyError:
        # Se a chave não for encontrada
        st.error("Chave de API do Google não encontrada. Configure-a nos Secrets do Streamlit.")
        return False
    except Exception as e:
        st.error(f"Erro ao configurar a API: {e}")
        return False

def gerar_roteiro_ia(destino, duracao, estilo, orcamento, interesses):
    """
    Chama a IA do Google Gemini para gerar o roteiro de viagem.
    """
    
    # 1. Construção do Prompt (A instrução para a IA)
    prompt_para_ia = f"""
    Aja como um especialista em viagens global. Quero que você crie um roteiro de viagem 
    personalizado e detalhado, dia a dia.

    **Contexto da Viagem:**
    * **Destino:** {destino}
    * **Duração:** {duracao} dias
    * **Estilo de Viagem:** {estilo}
    * **Orçamento:** {orcamento}
    * **Interesses Principais:** {interesses}

    **Sua Tarefa:**
    1.  Crie um itinerário dia a dia (Dia 1, Dia 2, ...).
    2.  Para cada dia, sugira atividades (manhã, tarde, noite) que se encaixem 
        perfeitamente no estilo de viagem e nos interesses mencionados.
    3.  Inclua sugestões de tipos de restaurantes ou pratos locais (alinhados ao orçamento).
    4.  Dê dicas práticas sobre transporte local ou costumes.
    5.  O tom deve ser empolgante e encorajador.
    6.  O formato da resposta deve ser em Markdown, bem estruturado.
    """
    
    # Inicializa o modelo
    # Usando o 1.5-flash que é rápido e ótimo para essa tarefa
    model = genai.GenerativeModel('gemini-2.5-flash-lite') 
    
    # 2. Geração de conteúdo
    try:
        response = model.generate_content(prompt_para_ia)
        return response.text
    except Exception as e:
        st.error(f"Erro ao gerar o roteiro: {e}")
        return "Desculpe, não foi possível gerar seu roteiro no momento."

# --- Configuração da Página do Streamlit ---
st.set_page_config(page_title="Roteiro de Viagem IA", page_icon="🗺️", layout="wide")

# --- Interface do Usuário (UI) ---
st.title("🗺️ Gerador de Roteiros de Viagem com IA")
st.markdown("Descreva a viagem dos seus sonhos e deixe que a inteligência artificial planeje cada detalhe para você.")

st.divider()

# Colunas para organizar os inputs
col1, col2 = st.columns(2)

with col1:
    destino = st.text_input("Para onde você quer ir?", placeholder="Ex: Kyoto, Japão")
    duracao = st.number_input("Quantos dias você pretende ficar?", min_value=1, max_value=90, value=5)

with col2:
    estilo = st.selectbox(
        "Qual é o seu estilo de viagem preferido?",
        ("Aventura (Trilhas, esportes)", 
         "Tranquilo (Praias, Spas, Relaxar)", 
         "Cultural (Museus, História)", 
         "Gastronômico (Comida e bebida)",
         "Mochilão (Econômico, flexível)")
    )
    orcamento = st.select_slider(
        "Qual o seu orçamento (sem passagens)?",
        options=["Econômico", "Moderado", "Confortável", "Luxo"],
        value="Moderado"
    )

interesses = st.text_area(
    "Quais são seus interesses principais ou coisas que você não quer perder?",
    placeholder="Ex: Gosto de arquitetura moderna, comida de rua, trilhas leves e cafés charmosos."
)

st.divider()

if st.button("✨ Gerar Meu Roteiro Personalizado!"):
    # Validações
    if not destino or not interesses:
        st.error("Por favor, preencha o destino e seus interesses para um roteiro incrível!")
    else:
        # 1. Tenta configurar a IA (verifica se a API Key existe)
        if configurar_ia():
            # 2. Se a chave OK, gera o roteiro
            with st.spinner(f"Mapeando a viagem perfeita de {estilo} para {destino}..."):
                roteiro_gerado = gerar_roteiro_ia(destino, duracao, estilo, orcamento, interesses)
                st.success("Seu roteiro está pronto!")
                st.markdown(roteiro_gerado)
