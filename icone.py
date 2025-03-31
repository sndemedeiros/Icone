import streamlit as st
from gtts import gTTS

# Título do aplicativo
st.title("Comunicação por Ícones")

# Mensagem de boas-vindas
st.write("Bem-vindo ao 'Comunicação por Ícones'! Este aplicativo ajuda você a montar frases de forma rápida e prática em situações de necessidade.")

# Inicializar a sessão para a frase montada
if "text" not in st.session_state:
    st.session_state.text = ""

# Função para identificar o pronome mais recente
def detectar_pronome(frase):
    pronomes = {
        "Eu": "1s", "Você": "2s", "Ele": "3s", "Ela": "3s",
        "Nós": "1p", "Eles": "3p", "Elas": "3p"
    }
    for palavra in reversed(frase.split()):
        if palavra in pronomes:
            return pronomes[palavra]
    return None

# Função para conjugar verbos
def conjugar_verbo(verbo_base, pronome):
    conjugacoes = {
        "Querer": {"1s": "quero", "2s": "quer", "3s": "quer", "1p": "queremos", "3p": "querem"},
        "Estar": {"1s": "estou", "2s": "está", "3s": "está", "1p": "estamos", "3p": "estão"},
        "Ir": {"1s": "vou", "2s": "vai", "3s": "vai", "1p": "vamos", "3p": "vão"},
        "Sentir": {"1s": "sinto", "2s": "sente", "3s": "sente", "1p": "sentimos", "3p": "sentem"},
        "Poder": {"1s": "posso", "2s": "pode", "3s": "pode", "1p": "podemos", "3p": "podem"},
        "Fazer": {"1s": "faço", "2s": "faz", "3s": "faz", "1p": "fazemos", "3p": "fazem"}
    }
    if pronome in conjugacoes[verbo_base]:
        return conjugacoes[verbo_base][pronome]
    return verbo_base.lower()

# Função para adicionar verbo conjugado
def adicionar_verbo(verbo_base):
    pronome = detectar_pronome(st.session_state.text)
    if pronome:
        verbo_conjugado = conjugar_verbo(verbo_base, pronome)
        st.session_state.text += verbo_conjugado + " "
    else:
        st.warning("Selecione um pronome antes de adicionar um verbo!")

# Exibir frase montada
def exibir_frase_montada():
    st.sidebar.subheader("Frase Montada:")
    st.sidebar.write(st.session_state.text)
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Limpar Frase"):
            st.session_state.text = ""
    with col2:
        if st.button("🔊 Ouvir Frase"):
            if st.session_state.text.strip():
                tts = gTTS(st.session_state.text.strip(), lang='pt')
                tts.save("frase.mp3")
                st.audio("frase.mp3")
            else:
                st.sidebar.warning("Crie uma frase antes de ouvir!")

# Adicionar seção de Principais Frases na barra lateral
st.sidebar.header("Principais Frases")
frase_selecionada = st.sidebar.selectbox(
    "Escolha uma frase:",
    [
        "Selecione uma frase...",
        "------------------",  # Separador visual
        "🔷 **Necessidades Básicas**:",
        "Preciso ir ao banheiro.",
        "Estou com fome.",
        "Preciso de água.",
        "Preciso de um remédio.",
        "------------------",
        "🔶 **Sensações e Conforto**:",
        "Estou com calor.",
        "Estou com frio.",
        "Preciso reposicionar.",
        "A luz está forte.",
        "------------------",
        "🔷 **Emoções e Estado**:",
        "Estou feliz.",
        "Estou triste.",
        "Estou irritado(a).",
        "Estou chorando.",
        "------------------",
        "🔶 **Pedidos de Ajuda**:",
        "Preciso conversar.",
        "Pode chamar o médico?",
        "Pode trazer meu celular?",
        "Preciso de ajuda.",
        "------------------",
        "🔷 **Preferências Simples**:",
        "Ouvir música.",
        "Ler um livro.",
        "Assistir TV.",
        "Sair ao ar livre."
    ]
)

if frase_selecionada and frase_selecionada != "Selecione uma frase...":
    if st.sidebar.button("Adicionar Frase"):
        st.session_state.text += frase_selecionada.replace("**", "").replace("🔷 ", "").replace("🔶 ", "") + " "

# Inicializar a lista de frases personalizadas, se ainda não existir
if "minhas_frases" not in st.session_state:
    st.session_state.minhas_frases = []

# Seção para gerenciar frases personalizadas
st.sidebar.header("Gerenciar Frases Personalizadas")

# Campo de entrada para adicionar novas frases
nova_frase = st.sidebar.text_input("Escreva uma nova frase:", key="nova_frase")
if st.sidebar.button("Salvar Frase", key="salvar_frase"):
    if nova_frase.strip():
        st.session_state.minhas_frases.append(nova_frase)
        st.sidebar.success("Frase adicionada com sucesso!")
    else:
        st.sidebar.error("Por favor, insira uma frase válida.")

# Exibir e gerenciar frases personalizadas
if st.session_state.minhas_frases:
    st.sidebar.subheader("Frases Salvas:")
    for frase in st.session_state.minhas_frases:
        col1, col2 = st.sidebar.columns([3, 1])  # Divisão entre botões
        with col1:
            if st.button(f"{frase}", key=f"adicionar_{frase}"):
                st.session_state.text += frase + " "  # Seleciona a frase ao clicar
        with col2:
            if st.button("❌", key=f"remover_{frase}"):
                st.session_state.minhas_frases.remove(frase)
                st.sidebar.success(f"Frase '{frase}' removida!")# Categorias adicionais na lateral
st.sidebar.header("Categorias Adicionais")
categoria = st.sidebar.selectbox(
    "Selecione uma Categoria:",
    ["Necessidades Básicas", "Sensações e Conforto", "Emoções e Estado", "Pedidos de Ajuda", "Preferências Simples"]
)

# Mostrar pronomes e verbos na tela principal
st.header("Pronomes e Verbos")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("😊 Eu"):
        st.session_state.text += "Eu "
    if st.button("👍 Querer"):
        adicionar_verbo("Querer")
    if st.button("🧍 Estar"):
        adicionar_verbo("Estar")
with col2:
    if st.button("👉 Você"):
        st.session_state.text += "Você "
    if st.button("➡️ Ir"):
        adicionar_verbo("Ir")
    if st.button("💗 Sentir"):
        adicionar_verbo("Sentir")
with col3:
    if st.button("👥 Nós"):
        st.session_state.text += "Nós "
    if st.button("👐 Poder"):
        adicionar_verbo("Poder")
    if st.button("🛠️ Fazer"):
        adicionar_verbo("Fazer")

st.header("Conjunções")
col4, col5 = st.columns(2)
with col4:
    if st.button("🤝 Com"):
        st.session_state.text += "Com "
    if st.button("🚫 Sem"):
        st.session_state.text += "Sem "
    if st.button("➕ E"):
        st.session_state.text += "e "
with col5:
    if st.button("⚡ Mas"):
        st.session_state.text += "mas "
    if st.button("🔀 Ou"):
        st.session_state.text += "ou "
    if st.button("⏳ Agora"):
        st.session_state.text += "Agora "

# Exibir categorias adicionais na parte principal
if categoria == "Necessidades Básicas":
    st.header("Necessidades Básicas")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚰 Água"):
            st.session_state.text += "Água "
        if st.button("🍽️ Comer"):
            st.session_state.text += "Comer "
    with col2:
        if st.button("💊 Remédio"):
            st.session_state.text += "Remédio "
        if st.button("🚻 Banheiro"):
            st.session_state.text += "Banheiro "

elif categoria == "Sensações e Conforto":
    st.header("Sensações e Conforto")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🥵 Calor"):
            st.session_state.text += "Calor "
        if st.button("🥶 Frio"):
            st.session_state.text += "Frio "
    with col2:
        if st.button("🪑 Reposicionar"):
            st.session_state.text += "Reposicionar "
        if st.button("💡 Luz"):
            st.session_state.text += "Luz "

elif categoria == "Emoções e Estado":
    st.header("Emoções e Estado")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("😊 Feliz"):
            st.session_state.text += "Feliz "
        if st.button("😢 Triste"):
            st.session_state.text += "Triste "
    with col2:
        if st.button("😡 Irritado"):
            st.session_state.text += "Irritado "
        if st.button("😭 Chorando"):
            st.session_state.text += "Chorando "

elif categoria == "Pedidos de Ajuda":
    st.header("Pedidos de Ajuda")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗣️ Conversar"):
            st.session_state.text += "Conversar "
        if st.button("🔔 Chamar"):
            st.session_state.text += "Chamar "
    with col2:
        if st.button("🚑 Emergência"):
            st.session_state.text += "Emergência "
        if st.button("📞 Telefone"):
            st.session_state.text += "Telefone "

elif categoria == "Preferências Simples":
    st.header("Preferências Simples")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎵 Música"):
            st.session_state.text += "Música "
        if st.button("📖 Ler"):
            st.session_state.text += "Ler "
    with col2:
        if st.button("📺 Assistir TV"):
            st.session_state.text += "Assistir TV "
        if st.button("🌳 Sair"):
            st.session_state.text += "Sair ao ar livre "

# Exibir frase montada na barra lateral
exibir_frase_montada()