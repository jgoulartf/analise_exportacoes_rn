import os
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar a planilha
file_path = 'src/app/dataset_relevancias.xlsx'
data = pd.read_excel(file_path)

# Carregar o arquivo Excel para HeatMap
file_path_heat = 'src/app/dataset_relevancias_por_ano.xlsx'
data_heat = pd.read_excel(file_path_heat)

# Filtrar colunas para garantir que temos as necessárias
st.title("Relevância dos Produtos ao Longo dos Anos")

coluna_filtro = 'Descrição SH6'
# Selecionar a coluna 'sh6' e o valor de relevância ao longo dos anos
if coluna_filtro not in data.columns:
    st.error(f"A coluna {coluna_filtro} não foi encontrada no dataset. Verifique se a coluna existe e tente novamente.")
else:
    # Selecionar produtos por 'sh6'
    produtos_unicos = data[coluna_filtro].unique()
    produtos_selecionados = st.multiselect("Selecione os produtos pela descrição Sh6:", produtos_unicos)

    # Adicionar o filtro de ano
    ano_inicial, ano_final = st.slider(
        "Selecione o intervalo de anos",
        min_value=1997,
        max_value=2024,
        value=(1997, 2024),
        step=1
    )

    # Filtrar dados com base na seleção do usuário
    dados_filtrados = data[data[coluna_filtro].isin(produtos_selecionados)]
    dados_filtrados = dados_filtrados[(dados_filtrados['Ano'] >= ano_inicial) & (dados_filtrados['Ano'] <= ano_final)]

    # Garantir que NaN (ausência de dados) seja tratado corretamente
    dados_filtrados['Relevância'] = pd.to_numeric(dados_filtrados['Relevância'], errors='coerce')

    # Criar gráfico de descontinuidades com Altair
    if not dados_filtrados.empty:
        chart = alt.Chart(dados_filtrados).mark_line().encode(
            x='Ano:O',  # 'O' significa tipo ordinal, que é adequado para os anos
            y='Relevância:Q',  # 'Q' significa variável quantitativa
            color='Descrição SH6:N',  # 'N' significa variável nominal (categórica)
        ).properties(
            title='Relevância dos Produtos ao Longo dos Anos',
            width=650,  # Largura configurada via controle
            height=530  # Altura configurada via controle
        ).configure_legend(
            orient='bottom'  # Colocar a legenda abaixo do gráfico
        ).interactive()

        # Exibir o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para o intervalo de anos selecionado.")




# Filtrar colunas para garantir que temos as necessárias
st.title("Mapa de calor da relevância dos produtos ao longo dos anos")
# Criando o Mapa de Calor

# Carregar o dataset e limpar os dados como feito anteriormente
data_heat.columns = ["Produto", "Código SH6", "Descrição"] + list(range(1997, 2025))
data_heat_cleaned = data_heat.drop(columns=["Produto", "Descrição"]).set_index("Código SH6")

# Preencher valores ausentes com zero
data_heat_cleaned_filled = data_heat_cleaned.fillna(0)
print(data_heat_cleaned_filled.head())

# Gerar o mapa de calor com o índice de Código SH6 no eixo y
plt.figure(figsize=(21, 21))
sns.heatmap(data_heat_cleaned_filled, cmap="Oranges", cbar_kws={'label': 'Relevância'}, annot=False)

# Título e rótulos dos eixos
plt.title("Mapa de Calor das Relevâncias por Ano")
plt.xlabel("Ano")
plt.ylabel("Código SH6")

st.pyplot(plt)

