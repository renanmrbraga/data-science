import pandas as pd
import seaborn as sns
import plotly.io as pio
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import cufflinks as cf
import plotly.graph_objects as go
import plotly.express as px
import os

# Definir caminho base
caminho_base = os.path.join('..', 'Materiais')

# Carregar base de vendas
caminho_vendas = os.path.join(caminho_base, 'varejo.xlsx')
vendas = pd.read_excel(caminho_vendas)

# Substituir valores inconsistentes na coluna 'idcanalvenda'
vendas['idcanalvenda'] = vendas['idcanalvenda'].str.replace('APP', 'Aplicativo')

# Corrigir espaços na coluna 'Nome_Departamento'
vendas['Nome_Departamento'] = vendas['Nome_Departamento'].str.replace(' ', '_')

# Tratar valores nulos na coluna 'estado'
vendas['estado'] = vendas['estado'].fillna('MS')

# Tratar valores nulos na coluna 'Preço'
media_preco = vendas['Preço'].mean()
vendas['Preço'] = vendas['Preço'].fillna(media_preco)

# Filtrar registros onde o preço está correto
vendas_correto = vendas.query('Preço < Preço_com_frete').copy()

# Criar nova coluna 'mes' a partir da data
vendas_correto['mes'] = vendas_correto['Data'].dt.month

# Carregar base de clientes
try:
    caminho_cliente = os.path.join(caminho_base, 'cliente_varejo.xlsx')
    cliente = pd.read_excel(caminho_cliente)
    cliente = cliente.astype({'renda': 'float'})
    
    # Juntar as bases
    vendas_cliente = vendas_correto.merge(cliente, how='left', on='cliente_Log')
except FileNotFoundError:
    print("Arquivo de clientes não encontrado.")

# Criar agregações para gráficos
agg_idcanal_renda = round(vendas_cliente.groupby('idcanalvenda')['renda'].agg('mean').sort_values(ascending=False).reset_index(), 2)
agg_idade_bandeira = round(vendas_cliente.groupby('bandeira')['idade'].agg('mean').sort_values(ascending=False).reset_index(), 2)
agg_dept_preco = round(vendas_correto.groupby('Nome_Departamento')['Preço_com_frete'].agg('mean').sort_values(ascending=False).reset_index(), 2)
venda_por_data = vendas_correto.groupby('Data').idcompra.nunique().reset_index()

# Gráfico 1 com plotly
fig1 = px.bar(agg_idade_bandeira, x='bandeira', y='idade')
pio.show(fig1) # Exibir o gráfico diretamente no VSCode

# Gráfico 2 com plotly
fig2 = px.line(venda_por_data, x='Data', y='idcompra')
pio.show(fig2) # Exibir o gráfico diretamente no VSCode
