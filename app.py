import streamlit as st 
from st_pages import Page, show_pages

show_pages(
    [
        Page("app.py", "Início", "🏠"),
        Page("pages/Modelo de Potabilidade de Agua.py", "Modelo de Potabilidade Agua", "🚰:"),
        Page("pages/Assistente de Cinema.py", "ChatBot Cinema", "🎦"),      
        Page("pages/Sobre.py", "Sobre", "ℹ️")   
    ]
)

st.header('Reconhecimento de Padrões - Hands On', divider='gray')

# Texto com sintaxe Markdown
texto_markdown = """
Reunir em um WebApp Streamlit as tarefas solicitadas em aula, isto é, esse WebApp deve conter as seguintes páginas:

- O deploy de pelo menos um modelo de Machine Learning.
- O chatbot com um assistente definido por vocês e com as características solicitadas no exercício. 
- Uma página 'Sobre', com os nomes dos envolvidos na criação do app e informações adicionais que julgarem pertinentes.
"""

# Exibindo o texto formatado com Markdown
container = st.container(border=True)
container.markdown(texto_markdown)