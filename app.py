from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import requests

app = Flask(__name__)


@app.route('/') # Rota principal para renderizar a dashboard
def index():
    # obter dados da API
    api_url = 'https://brisa-ts.dev.amo.delivery/api/esp32amo?start_at=2023-11-13'
    response = requests.get(api_url)
    data = response.json()

    # transformar dados em DataFrame usando Pandas
    df = pd.DataFrame(data['data'])  # Use 'data' para obter a lista de dados

    # converta a coluna 'created_at' para o tipo de dados de data/hora
    df['created_at'] = pd.to_datetime(df['created_at'])

    # formatar 'created_at' para exibir apenas dia, mês, e hora
    df['Tempo'] = df['created_at'].dt.strftime('%d-%m %H:%M:%S')

    # Calcular a última medida de temperatura interna e externa
    ultima_temperatura_int = df['temperature_int'].iloc[-1]
    ultima_temperatura_ext = df['temperature_ext'].iloc[-1]
    ultima_umidade_int = df['humidity_int'].iloc[-1]
    ultima_umidade_ext = df['humidity_ext'].iloc[-1]

    # Criar gráfico usando Plotly (Temperatura Externa, Interna e do Alimento)
    fig_temp = px.line(df, x="Tempo", y=["temperature_ext", "temperature_int", "temperature_alimento"], title="Temperatura Externa, Interna e do Alimento")
    fig_temp.update_xaxes(type="category")  # Usar categoria para o eixo x
    plot_temp_html = fig_temp.to_html(full_html=False)

    # Criar gráfico usando Plotly (Umidade Interna e Umidade Externa)
    fig_umidade = px.line(df, x="Tempo", y=["humidity_int", "humidity_ext"], title="Umidade Interna e Externa")
    fig_umidade.update_xaxes(type="category")  # Usar categoria para o eixo x
    plot_umidade_html = fig_umidade.to_html(full_html=False)

    # Criar histogramas para os dados atuais


    return render_template("index.html", 
                           plot_temp=plot_temp_html, 
                           plot_umidade=plot_umidade_html, 
                           ultima_temperatura_int=ultima_temperatura_int, 
                           ultima_temperatura_ext=ultima_temperatura_ext,
                           ultima_umidade_int=ultima_umidade_int,
                           ultima_umidade_ext=ultima_umidade_ext
                           )

if __name__ == '__main__':
    app.run(debug=True)
