import time
import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from openai import OpenAI
import base64


# Função para calcular custo estimado com base na quantidade de tokens
def calcular_custo(tokens):
   # Conforme a política de preços da OpenAI $0.004 por token
   preco_por_token = 0.004  # Preço por token para o modelo gpt-3.5-turbo
   return tokens * preco_por_token


# Função para encerrar o diálogo
def encerrar_dialogo(texto):
   container.write(f'{texto}')
   # Adiciona histórico ao DataFrame
   st.session_state.df_conversas = pd.DataFrame(st.session_state.historico_dialogo)
   container.success("Diálogo encerrado. Os dados foram salvos.")
   # Limpa as informações da sessão
   st.session_state.mensagens = []
   st.session_state.historico_dialogo = []

# Função para criar PDF da conversa
def criar_pdf(df):
   output_filename = "conversa_AssistenteMovieFPDF.pdf"
   # Criar o documento PDF
   pdf = FPDF()
   pdf.add_page()
   pdf.set_font("Arial", size=12)
   for index, row in df.iterrows():
       texto = f"{row['Data e hora']}: {row['role']}: {row['msg_dialogo']}: tokens={row['qtde_tokens']}: custo={row['custo_estimado']}"
       # Adiciona a linha ao PDF
       pdf.multi_cell(0, 10, texto)
   # Salvar o PDF
   pdf.output(output_filename)
   return output_filename


st.markdown("<h4 <styleCine Bot='text-align: center;'>🎞️🎥🍿📽️🎞️🎥🍿📽️🎞️🎥🍿📽️🎞️🎥🍿📽️🎞️🎥🍿📽️</h4", unsafe_allow_html=True)
st.title(":blue[ Cine Bot ]", help="Assistente com melhores dicas de filmes!")
st.subheader(":black[ Assistente com melhores dicas de filmes! ]", divider='gray')

chave = st.sidebar.text_input('Chave da API OpenAI', type='password')
client = OpenAI(api_key=chave)

desabilita_botao_gerar_pdf = True
desabilita_botao_baixar_pdf = True
pdf_filename = ""

# Inicializa o histórico do diálogo e o DataFrame na sessão do Streamlit
if "historico_dialogo" not in st.session_state:
   st.session_state.historico_dialogo = []
   st.session_state.df_conversas = pd.DataFrame(columns=['Data e Hora', 'Role', 'Histórico do Diálogo', 'Qtde Tokens', 'Custo Estimado'])


parametros = st.expander("Configurações do ChatBot. Escolha os parametros:")

col0, col1 = parametros.columns([2, 4])
col2, col3 = parametros.columns([2, 4])
# Mapeamento de opções para valores de max_tokens
opcoes_max_tokens = {'curta': 150, 'média': 300, 'longa': 500}
with col0:
   opcao_tamanho_resposta = st.radio(label='Tamanho da resposta',
                                     options=['curta', 'média', 'longa'],
                                     index=2,
                                     key=None,
                                     help='Escolha um tamanho',
                                     on_change=None,
                                     args=None,
                                     kwargs=None,
                                     disabled=False,
                                     horizontal=False,
                                     label_visibility="visible")  # hidden #collapsed

# Obter o valor correspondente de max_tokens
max_tokens = opcoes_max_tokens[opcao_tamanho_resposta]
rotulos = {0.0: 'conservador', 1.0: 'normal', 2.0: 'arrojado'}
with col1:
   temperatura = st.slider(label='Escolha o nível de criatividade',
                           min_value=min(rotulos.keys()),
                           max_value=max(rotulos.keys()),
                           value=1.0,
                           step=0.1,
                           format='%.1f',
                           key=None,
                           help='Escolha um nível de criatividade: 0-conservador, 1-normal, 2-arrojado',
                           on_change=None,
                           args=None,
                           kwargs=None,
                           disabled=False,
                           label_visibility="visible")

with col2:
   selecao = st.selectbox(label='Estilo do assistente',
                          options=['Amigável', 'Bem humorado', 'Inteligente', 'Objetivo'],
                          index=1,
                          key=None,
                          help='Estilo do assitente',
                          on_change=None,
                          args=None,
                          kwargs=None,
                          disabled=False,
                          label_visibility="visible")
with col3:
   # Criando um componente de upload de arquivos
   uploaded_file = st.file_uploader(label='Carregar arquivo',
       type='txt',
       help='Permite ao usuário subir um arquivo de texto para que a informação do arquivo seja levada em consideração na conversa com o chatbot.',
       accept_multiple_files=False,
       key=None,
       on_change=None,
       args=None,
       kwargs=None,
       disabled=False,
       label_visibility="visible")

containerChat = st.container()
containerChat.subheader("Mensagens do Chat:", divider='gray')


contexto = 'Você será um assistente que vai sugerir filmes para uma pessoa adulta. Sua função é sugerir filmes que a pessoa estiver buscando de acordo com o estado de espírito da pessoa no momento. Use sempre uma linguagem positiva, inteligente e abuse no detalhamento do filme sugerido! Seja um assitente ' + selecao

# Iniciar Histórico Chat

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{"role": 'system', "content": contexto}]
# só para teste  
#st.write(contexto)
#st.write(st.session_state.mensagens)
# Aparecer o Histórico do Chat na tela
# for mensagem in st.session_state.mensagens[1:]:
#     with st.chat_message(mensagem["role"]):
#         st.markdown(mensagem["content"])

if uploaded_file is not None:
   # Lendo o conteúdo do arquivo
   file_contents = uploaded_file.read()
   #st.text(file_contents)  # Exibindo o conteúdo para verificar
   arquivo_texto = file_contents.decode('utf-8')
   #alimenta com as informações do arquivo
   contextoArquivo = f'. Para responder, considere as seguintes informações: \n\n{arquivo_texto}'
   contexto += contextoArquivo
   st.session_state.mensagens.append({"role": "assistant", "content": contexto})

for mensagem in st.session_state.mensagens[1:]:
   # Verificar o papel da mensagem
   if mensagem["role"] == "user" or mensagem["role"] == "system":
       with st.chat_message(mensagem["role"]):
           st.markdown(mensagem["content"])


# React to user input
prompt = st.chat_input("Digite alguma coisa")

if prompt:
   # Display user message in chat message container
   with st.chat_message("user"):
       st.markdown(prompt)
   # Registra o timestamp da mensagem
   timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
   #armazena o que o usuário digitou para salvar no diálogo
   st.session_state.historico_dialogo.append({"Data e hora": timestamp,
       "role": "user",
       "msg_dialogo": f"Usuário: {prompt}",
       "qtde_tokens": 0,
       "custo_estimado": 0
   })
   st.session_state.mensagens.append({"role": "user", "content": prompt})
   # Antes de chamar a resposta do OPENAI vai chamar a moderação
   moderation = client.moderations.create(input=prompt)
   output = moderation.results[0]
   df = pd.DataFrame(dict(output.category_scores).items(), columns=['Category', 'Value'])
   df = df.sort_values(by='Value', ascending=False).round(5)  # Armazena o DataFrame ordenado
   top_5_linhas = df.sort_values(by='Value', ascending=False).head(5)
   traducao_categorias = {
       'violence': 'violência',
       'sexual': 'sexual',
       'harassment': 'assédio',
       'hate': 'ódio',
       'self-harm': 'autolesão',
       'self_harm_intent': 'intenção de autolesão',
       'harassment_threatening': 'assédio/ameaça',
       'harassment/threatening': 'assédio/ameaça',
       'violence_graphic': 'violência/gráfico',
       'violence/graphic': 'violência/gráfico',
       'hate_threatening': 'ódio/ameaça',
       'hate/threatening': 'ódio/ameaça',
       'self-harm_intent': 'autolesão/intenção',
       'self-harm/intent': 'autolesão/intenção',
       'sexual_minors': 'sexual/menores',
       'sexual/minors': 'sexual/menores',
       'sexual': 'sexual'
   }
   top_5_linhas = df.sort_values(by='Value', ascending=False).head(5)
   if top_5_linhas['Value'].max() > 0.1:
       mensagem_padrao = 'Este diálogo será finalizado por violar as seguintes regras:'
       for index, linha in top_5_linhas.iterrows():
           categoria_traduzida = traducao_categorias.get(linha['Category'], linha['Category'])
           mensagem_padrao += f' {categoria_traduzida},'
       mensagem_padrao = mensagem_padrao.rstrip(',')
       st.warning(mensagem_padrao)
       # Adiciona mensagem de moderação ao histórico
       st.session_state.historico_dialogo.append({
           "Data e hora": timestamp,
           "role": "moderation",
           "msg_dialogo": f"Assistente: {mensagem_padrao}",
           "qtde_tokens": 0,
           "custo_estimado": 0
       })
   else:
       chamada_openai = client.chat.completions.create(
           model='gpt-3.5-turbo',
           messages=st.session_state.mensagens,
           temperature=temperatura,
           max_tokens=max_tokens
       )
       resposta = chamada_openai.choices[0].message.content
       info_uso = chamada_openai.usage
       if info_uso is not None:
           qtde_tokens_resposta = info_uso.total_tokens
           custo_estimado = calcular_custo(qtde_tokens_resposta)
           # Adiciona mensagem ao histórico
           st.session_state.historico_dialogo.append({
               "Data e hora": timestamp,
               "role": "system",
               "msg_dialogo": resposta,
               "qtde_tokens": qtde_tokens_resposta,
               "custo_estimado": custo_estimado,
           })
       # Display assistant response in chat message container
       with st.chat_message("system"):
           st.markdown(resposta)
       # Add assistant response to chat history
       st.session_state.mensagens.append({"role": "system", "content": resposta})

# Adiciona espaço para melhorar o layout
st.markdown("<br>", unsafe_allow_html=True)

container = st.container(border=True)
col0, col1, col2 = container.columns([3,3,3])
with col0:
   if st.button(label = 'Encerrar o diálogo',
       help = 'Encerra o diálogo',
       type = 'primary', # 'primary' ou 'secondary'
       disabled = False,
       use_container_width = True,
       on_click = encerrar_dialogo,
       args = None,
       kwargs = {'texto': ''}
   ):
       desabilita_botao_gerar_pdf = False
with col1:
   if st.button(label='Gerar PDF', help='Gera o PDF da conversa', type='primary', disabled=desabilita_botao_gerar_pdf, use_container_width=True):
       #st.write("Criando o pdf...")
       pdf_filename = criar_pdf(st.session_state.df_conversas)
       # Exibe mensagem de encerramento
       st.success("PDF gerado")
       desabilita_botao_baixar_pdf = False
with col2:
   # Verifica se o arquivo PDF existe
   #if os.path.exists(pdf_filename):
   with open("conversa_AssistenteMovieFPDF.pdf", "rb") as pdf_file:
       PDFbyte = pdf_file.read()
   st.download_button(label='Baixar PDF conversa',
                          data=PDFbyte,
                          file_name='conversa_AssistenteMovie.pdf',
                          mime='application/octet-stream',
                          key=None,
                          help='Baixa o PDF conversa salva em PDF',
                          on_click=None,
                          args=None,
                          kwargs=None,
                          disabled=desabilita_botao_baixar_pdf,
                          use_container_width=False)
