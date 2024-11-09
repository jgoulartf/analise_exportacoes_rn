import streamlit as st
import pandas as pd
import altair as alt

# Carregar a planilha
file_path = './dataset_relevancias.xlsx'
data = pd.read_excel(file_path)

# Filtrar colunas para garantir que temos as necessárias
st.title("Visualização de Relevância dos Produtos por Ano")

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


