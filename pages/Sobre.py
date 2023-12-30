import streamlit as st

def main():
    st.set_page_config(page_title="SOBRE", page_icon=":information_source:")

# Título da página
st.header("Sobre")


    # Descrição da equipe

tab1, tab2, tab3, tab4 = st.tabs(["Informações", "Potabilidade Agua", "ChatBot Cinema", "Equipe"])

with tab1:
    st.markdown(
        """
        ##### Informações

        Neste aplicativo trazemos duas funcionalidades:

        1- Um modelo de Machine Learning para identificar se uma amostra de água é potável ou não. 
        De acordo com as informações fornecidas o modelo será capaz de responder se a água é potável ou não.

        2- Um chat bot que é um assitente virtual de indicação de filmes. Ele vai sugerir filmes de acordo com o que o usuário estiver desejando, 
        sentindo e estado de espírito no momento.
        """
    )

# Lista de membros da equipe
with tab2:
    st.markdown("""
    ##### Potabilidade de Agua
    O modelo de Machine Learning para prever a potabilidade da água conta com um conjunto de 10 variáveis; 9 independentes e uma variável dependente:

    * 1: indica que é potável
    * 0: não potável;

    As variáveis independentes são os parâmetros da água e dependendo do valor informado o modelo irá prever se a água deve ser classisificada como 
    potável ou não. São elas:

    * Valor do pH: O pH é um parâmetro importante na avaliação do equilíbrio ácido-base da água.
    * Dureza: A dureza é causada principalmente por sais de cálcio e magnésio.
    * Sólidos (Sólidos dissolvidos totais - TDS): A água tem a capacidade de dissolver uma ampla gama de minerais ou sais inorgânicos e alguns orgânicos, como potássio, cálcio, sódio, bicarbonatos, cloretos, magnésio, sulfatos etc.
    * Cloraminas: Cloro e cloramina são os principais desinfetantes usados em sistemas públicos de água.
    * Sulfato: Os sulfatos são substâncias naturais encontradas em minerais, solo e rochas.
    * Condutividade: A água pura não é um bom condutor de corrente elétrica, mas sim um bom isolante. O aumento na concentração de íons aumenta a condutividade elétrica da água.
    * Organic_carbon: O carbono orgânico total (TOC) nas águas de nascente vem da matéria orgânica natural em decomposição (NOM), bem como de fontes sintéticas.
    * Trihalometanos: THMs são produtos químicos que podem ser encontrados em água tratada com cloro.
    * Turbidez: A turbidez da água depende da quantidade de matéria sólida presente no estado suspenso.
    * Potabilidade: Indica se a água é segura para consumo humano onde 1 significa Potável e 0 significa Não potável.
    """)

with tab3:
    st.markdown("""
        ##### O Chat Bot - Assistente de Cinema 

        É um assistente virtual que indica filmes de acordo com o que o usuário solicitar. 

        Utiliza informações de contexto.
        
        O usuário pode definir como parametros o tamanho da resposta, o nível de criatividade da resposta e o estilo da escrita da resposta.
        
        Além disso, o assistente tem um escape de moderação, caso a pergunta viole, uma resposta padrão será gerada, finalzando o diálogo.

        """)
    


with tab4:
        st.markdown(
        """
        - Ludmilla Andrade
        - Rubia Teles de Souza
        """
    )


# Adicione mais informações sobre a equipe ou qualquer outra coisa que deseje incluir
# Estilos adicionais usando HTML e CSS
st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
                color: #333;
                font-family: 'Arial', sans-serif;
                margin: 2em;
            }
            .stMarkdown {
                line-height: 1.6;
            }
            header {
                background-color: #4CAF50;
                padding: 1em;
                color: white;
                text-align: center;
                font-size: 1.5em;
            }
            h1, h2, h3 {
                color: #000000;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
