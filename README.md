# Spotify Music Analysis

Este repositório contém um projeto de análise de dados que utiliza a API do Spotify para coletar informações sobre playlists de diferentes gêneros musicais. O objetivo é identificar as músicas mais tocadas e as preferências musicais de diferentes faixas etárias.

## Descrição
O projeto visa analisar as preferências musicais no Spotify, categorizando as músicas mais tocadas por diferentes faixas etárias e gêneros musicais. Utilizamos scripts em Python para coletar, processar e visualizar os dados. Os resultados são exportados para arquivos CSV, que podem ser importados e visualizados no Power BI.

## Como Executar
Siga os passos abaixo para configurar e executar o projeto:

1. Clone este repositório:
    ```bash
    git clone https://github.com/engdalevedove/spotify-music-analysis.git
    cd spotify-music-analysis
    ```

2. Crie e ative um ambiente virtual (opcional):
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # No Windows, use: myenv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais do Spotify:
    ```plaintext
    SPOTIPY_CLIENT_ID=seu_client_id
    SPOTIPY_CLIENT_SECRET=seu_client_secret
    ```

5. Execute o script para coletar e processar os dados:
    ```bash
    python spotify_music_analysis.py
    ```

## Tecnologias Utilizadas
- **Python**
- **Spotipy** (API do Spotify)
- **Pandas**
- **Matplotlib**
- **Seaborn**
- **Power BI**

## Estrutura do Projeto
- `spotify_music_analysis.py`: Script Python para coleta e análise de dados musicais.
- `musicas_mais_tocadas_por_faixa_etaria.csv`: Arquivo CSV contendo as músicas mais tocadas por faixa etária e gênero.
- `preferencias_musicais_por_faixa_etaria.csv`: Arquivo CSV contendo as preferências musicais por faixa etária.
- `README.md`: Este arquivo, contendo uma descrição detalhada do projeto.
- `requirements.txt`: Lista de dependências do projeto.

## Exemplos de Uso

### Exemplo de Comandos
Para coletar os dados:
```bash
python spotify_music_analysis.py
