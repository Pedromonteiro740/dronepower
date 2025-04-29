DronePower - Extração e Análise de Metadados de Imagens
📁 Estrutura de Pastas
Organize seus arquivos da seguinte forma:

dronepower/ ├── imagens/ │ ├── T.193/ │ ├── T.200/ │ └── T.216/ ├── scripts/ │ ├── extrair_metadados.py │ └── consultas.py ├── imagens_metadata.db └── README.md

🛠️ Requisitos
Python 3.x
Bibliotecas Python:
Pillow
matplotlib
Instale as bibliotecas necessárias com:

pip install Pillow matplotlib

📝 Passo a Passo
Organize as imagens: Coloque as pastas T.193, T.200 e T.216 dentro da pasta imagens/.

Extraia os metadados: Execute o script extrair_metadados.py para processar as imagens e armazenar os metadados no banco de dados SQLite.

cd scripts python extrair_metadados.py

Realize consultas e gere gráficos: Execute o script consultas.py para realizar as consultas solicitadas e gerar os gráficos correspondentes.
python consultas.py

Os gráficos gerados serão salvos no diretório atual com os nomes:

imagens_por_mes.png
distribuicao_tamanhos.png
quantidade_por_pasta.png
🧾 Consultas Realizadas
Imagens por Mês: Lista e gráfico da quantidade de imagens capturadas por mês.
Imagens Maiores que 3MB: Lista e gráfico da distribuição de tamanhos de imagens superiores a 3MB.
Quantidade por Pasta: Lista e gráfico da quantidade de imagens em cada pasta.
📌 Observações
Certifique-se de que as imagens possuem metadados EXIF válidos para extração de data e coordenadas.
O banco de dados imagens_metadata.db será criado na raiz do projeto após a execução do script de extração.
