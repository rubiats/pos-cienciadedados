import streamlit as st 
import pandas as pd
import numpy as np
from pycaret.classification import load_model, predict_model
from pycaret.datasets import get_data

# Carrega os dados do arquivo CSV na pasta 'recursos'
dados = pd.read_csv('recursos/water_potability.csv')
modelo = load_model('recursos/modelo_agua_potavel')

st.header('💧Deploy do Modelo da Potabilidade da Água', divider='gray')

st.write('Entre com as caracteristicas da água para fazer uma previsão de potabilidade da água.')


#Widgets para fazer os inputs do modelo

col0, col1, col2 = st.columns([3,3,3])

with col0:
	ph = st.number_input(label = 'PH', 
		min_value=0.0, 
		max_value=14.0, 
		value= 7.0, 
		step=0.5, 
		help='Informe o PH da água - 0 a 14')

	Chloramines = st.number_input(label = 'Cloraminas', 
		min_value = 0.35, 
		max_value = 13.50, 
		value = 2.0, 
		step = 0.5,
		help='Informe o nível de cloraminas da água - 0.35 à 13.50')

	Organic_carbon	= st.number_input(label = 'Carbono orgânico', 
		min_value = 2.0, 
		max_value = 28.0, 
		value = 3.0, 
		step = 0.5,
		help='Informe a quantidade de carbono orgânico na água - 2 à 28.30')

with col1: 
	Hardness = st.number_input(label = 'Dureza da água', 
		min_value = 47.0, 
		max_value = 324.0, 
		value = 50.0, 
		step = 1.0,
		help='Informe nível de dureza da água - varia de 47 a 324')
	
	Sulfate	= st.number_input(label = 'Sulfato', 
		min_value = 129.0, 
		max_value = 482.0, 
		value = 225.0, 
		step = 0.5,
		help='Informe nível de Sulfato da água - 129 à 482')

	Conductivity = st.number_input(label = 'Condutividade', 
		min_value = 181.0, 
		max_value = 754.0, 
		value = 300.0, 
		step = 0.5,
		help='Informe nível de Condutividade da água - 181 à 754')

with col2:
	Solids = st.number_input(label = 'Sólidos dissolvidos totais - TDS', 
		min_value = 320.0, 
		max_value = 62000.0, 
		value = 400.0, 
		step = 0.5,
		help='Informe quantidade de Sólidos da água - 320 à 62000')

	Trihalomethanes = st.number_input(label = 'Trihalometanos', 
		min_value = 0.73, 
		max_value = 124.0,
		step = 0.5,
		help='Informe quantidade de Trihalometanos da água - 0.73 à 124')

	Turbidity = st.number_input(label = 'Turbidez', 
		min_value = 1.45, 
		max_value = 6.74, 
		value = 2.8, 
		step = 0.1,
		help='Informe nível de Turbidez da água - 1.45 à 6.74')


#Criar um DataFrame com os inputs exatamente igual ao dataframe em que foi treinado o modelo
aux = {'ph': [ph],
		'Hardness': [Hardness],
		'Solids': [Solids],
		'Chloramines': [Chloramines],
		'Sulfate': [Sulfate],
		'Conductivity': [Conductivity],
		'Organic_carbon': [Organic_carbon],
		'Trihalomethanes': [Trihalomethanes],
		'Turbidity': [Turbidity]}

prever = pd.DataFrame(aux)

st.write(prever)

#Usar o modelo salvo para fazer previsao nesse Dataframe

_, c1, _ = st.columns([2,3,1])

with c1:
	botao = st.button('Calcular a potabilidade da água',
		type = 'primary',
		use_container_width = True)


if botao:
    previsao = predict_model(modelo, data=prever)
    valor = previsao.loc[0, 'prediction_label']

    # Adicionando a verificação condicional
    resultado_final = 'Potável' if valor == 1 else 'Não Potável'

    st.write(f'### A classificação da água prevista pelo modelo é: {resultado_final}')

