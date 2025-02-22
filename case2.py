import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Definir caminho base
caminho_base = os.path.join(os.getcwd(), 'materiais')

# Verificar se o arquivo 'varejo.xlsx' existe
caminho_vendas = os.path.join(caminho_base, 'varejo.xlsx')
if os.path.exists(caminho_vendas):
    print("Arquivo de vendas encontrado!")
    # Carregar base de vendas
    vendas = pd.read_excel(caminho_vendas)
else:
    print("Arquivo de vendas NÃO encontrado. Verifique o caminho.")

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

# Criando o gráfico de barras
fig1 = go.Bar(x=agg_idade_bandeira['bandeira'], y=agg_idade_bandeira['idade'])

# Criando o gráfico de linha
fig2 = go.Scatter(x=venda_por_data['Data'], y=venda_por_data['idcompra'], mode='lines')

# Criando subplots
fig = make_subplots(rows=1, cols=2,  # 1 linha, 2 colunas
                    subplot_titles=("Gráfico de Barras", "Gráfico de Linha"))

# Adicionando os gráficos nas subplots
fig.add_trace(fig1, row=1, col=1)
fig.add_trace(fig2, row=1, col=2)

# Exibindo o gráfico
fig.update_layout(title_text="Gráficos Combinados", showlegend=False)
fig.show()
