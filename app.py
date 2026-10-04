import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# 1. Carregar os dados
df = pd.read_csv('ecommerce_estatistica.csv')

# Tratamento básico da coluna Qtd_Vendidos para conversão em números
def limpar_qtd(val):
    if isinstance(val, str):
        val = val.replace('+', '').replace('mil', '000')
    try:
        return float(val)
    except:
        return 0

df['Qtd_Vendidos_Num'] = df['Qtd_Vendidos'].apply(limpar_qtd)

# 2. Criar os Gráficos
# Gráfico de Notas
fig_notas = px.histogram(df, x='Nota', title='Distribuição de Notas dos Produtos', nbins=20, color_discrete_sequence=['#636EFA'])

# Relação Preço vs Desconto
fig_preco_desconto = px.scatter(df, x='Preço', y='Desconto', color='Gênero', title='Relação entre Preço e Desconto por Gênero')

# Top 10 Marcas
top_marcas = df['Marca'].value_counts().head(10).reset_index()
top_marcas.columns = ['Marca', 'Contagem']
fig_marcas = px.bar(top_marcas, x='Marca', y='Contagem', title='Top 10 Marcas com Mais Produtos', color='Contagem')

# Vendas por Temporada
vendas_temporada = df.groupby('Temporada')['Qtd_Vendidos_Num'].sum().reset_index()
fig_temporada = px.pie(vendas_temporada, values='Qtd_Vendidos_Num', names='Temporada', title='Quantidade de Produtos Vendidos por Temporada')

# 3. Inicializar a aplicação Dash
app = dash.Dash(__name__)

# 4. Layout do App
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1('Dashboard de Estatísticas de E-commerce', style={'textAlign': 'center', 'color': '#2C3E50'}),
    
    html.Div(children='Visualização interativa do catálogo e vendas.', style={
        'textAlign': 'center', 'color': '#7F8C8D', 'marginBottom': '40px'
    }),
    
    html.Div([
        html.Div([dcc.Graph(figure=fig_notas)], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(figure=fig_preco_desconto)], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ]),
    
    html.Div([
        html.Div([dcc.Graph(figure=fig_marcas)], style={'width': '48%', 'display': 'inline-block', 'marginTop': '20px'}),
        html.Div([dcc.Graph(figure=fig_temporada)], style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'marginTop': '20px'}),
    ])
])

# 5. Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)