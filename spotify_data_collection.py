import spotipy
import matplotlib.pyplot as plt
import seaborn as sns
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from collections import Counter
from dotenv import load_dotenv
import os
import random
import geopandas as gpd
from geopy.geocoders import Nominatim
from concurrent.futures import ThreadPoolExecutor

# Carregar variáveis do .env
load_dotenv()

# Obter Client ID e Client Secret das variáveis de ambiente
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# Verificação se as variáveis de ambiente estão definidas
if not client_id or not client_secret:
    raise ValueError(
        "As variáveis de ambiente SPOTIPY_CLIENT_ID e SPOTIPY_CLIENT_SECRET devem ser definidas")

# Autenticação
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager, requests_timeout=30)

# Função para obter playlists de um determinado gênero


def get_genre_playlists(genre, limit=5):
    results = sp.search(q=f'genre:{genre}', type='playlist', limit=limit)
    return results['playlists']['items']

# Função para obter dados das faixas de uma playlist


def get_playlist_tracks(playlist_id, limit=50):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items'][:limit]
    return tracks

# Função para obter as 3 playlists mais tocadas de um determinado gênero


def get_top_playlists(genre, limit=3):
    playlists = get_genre_playlists(genre)
    playlist_counts = []
    for playlist in playlists:
        tracks = get_playlist_tracks(playlist['id'])
        playlist_counts.append((playlist['name'], len(tracks)))
    sorted_playlists = sorted(
        playlist_counts, key=lambda x: x[1], reverse=True)
    return sorted_playlists[:limit]


# Gêneros de interesse
genres = ['sertanejo', 'sertanejo universitario', 'Country',
          'pagode', 'funk', 'pop', 'Reggae', 'Hip Hop/Rap', 'rock', 'Metal', 'jazz', 'Classical', 'Electronic/Dance', 'internacional']

# Coleta de dados
genre_tracks = {}
top_playlists = {}
for genre in genres:
    print(f"Coletando dados para o gênero: {genre}")
    playlists = get_genre_playlists(genre)
    tracks = []
    for playlist in playlists:
        tracks.extend(get_playlist_tracks(playlist['id']))
    genre_tracks[genre] = tracks
    top_playlists[genre] = get_top_playlists(genre)

# Verificar se os dados foram coletados corretamente
if not genre_tracks:
    raise ValueError(
        "Nenhum dado foi coletado. Verifique a conexão com a API do Spotify e os parâmetros de busca.")

# Simulação de dados demográficos para faixas etárias e localização


def simulate_demographics(tracks, genre):
    age_groups = ['Adolescentes', 'Jovens Adultos', 'Adultos', 'Idosos']
    genders = ['Masculino', 'Feminino', 'Outro']
    locations = ['São Paulo', 'Rio de Janeiro', 'Minas Gerais',
                 'Bahia', 'Paraná', 'Pernambuco', 'Rio Grande do Sul']
    periods = pd.date_range(
        start='2023-01-01', end='2023-12-31', freq='ME').strftime("%Y-%m").tolist()
    simulated_data = []
    for track in tracks:
        if track['track'] is not None:
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            album_name = track['track']['album']['name']
            duration_ms = track['track']['duration_ms']
            # Simula múltiplas reproduções por faixa etária e localização
            for _ in range(random.randint(1, 5)):
                age_group = random.choice(age_groups)
                gender = random.choice(genders)
                location = random.choice(locations)
                period = random.choice(periods)
                simulated_data.append({
                    'Track Name': track_name,
                    'Artist': artist_name,
                    'Album': album_name,
                    'Duration (ms)': duration_ms,
                    'Age Group': age_group,
                    'Gender': gender,
                    'Location': location,
                    'Period': period,
                    'Genre': genre
                })
    return simulated_data


# Processamento dos dados para encontrar a música mais tocada por faixa etária e gênero
demographic_data = []
for genre, tracks in genre_tracks.items():
    demographic_data.extend(simulate_demographics(tracks, genre))

df_demographics = pd.DataFrame(demographic_data)

# Verificar se os dados demográficos foram gerados corretamente
if df_demographics.empty:
    raise ValueError(
        "Nenhum dado demográfico foi gerado. Verifique a função de simulação.")

# Encontrar a música mais tocada por faixa etária, localização e gênero
top_tracks = df_demographics.groupby(
    ['Age Group', 'Gender', 'Location', 'Period', 'Genre', 'Track Name']).size().reset_index(name='Count')
top_tracks = top_tracks.sort_values(
    ['Age Group', 'Gender', 'Location', 'Period', 'Count'], ascending=[True, True, True, True, False])

# Adicionando as 3 playlists mais tocadas ao DataFrame
top_playlists_data = []
for genre, playlists in top_playlists.items():
    for playlist in playlists:
        top_playlists_data.append({
            'Genre': genre,
            'Playlist Name': playlist[0],
            'Track Count': playlist[1]
        })
df_top_playlists = pd.DataFrame(top_playlists_data)

# Simulação de dados demográficos para preferências musicais (ajuste conforme necessário)
preferences_demographics = {
    'Adolescentes': {'sertanejo': 15, 'sertanejo universitario': 5, 'pagode': 15, 'funk': 30, 'pop': 25, 'rock': 5, 'jazz': 5, 'Country': 5, 'Reggae': 5, 'Hip Hop/Rap': 10, 'Metal': 5, 'Classical': 5, 'Electronic/Dance': 5, 'internacional': 5},
    'Jovens Adultos': {'sertanejo': 10, 'sertanejo universitario': 15, 'pagode': 20, 'funk': 25, 'pop': 30, 'rock': 10, 'jazz': 5, 'Country': 5, 'Reggae': 5, 'Hip Hop/Rap': 10, 'Metal': 5, 'Classical': 5, 'Electronic/Dance': 5, 'internacional': 5},
    'Adultos': {'sertanejo': 5, 'sertanejo universitario': 5, 'pagode': 10, 'funk': 15, 'pop': 20, 'rock': 30, 'jazz': 20, 'Country': 5, 'Reggae': 5, 'Hip Hop/Rap': 10, 'Metal': 5, 'Classical': 5, 'Electronic/Dance': 5, 'internacional': 5},
    'Idosos': {'sertanejo': 5, 'sertanejo universitario': 0, 'pagode': 5, 'funk': 10, 'pop': 10, 'rock': 20, 'jazz': 50, 'Country': 5, 'Reggae': 5, 'Hip Hop/Rap': 10, 'Metal': 5, 'Classical': 5, 'Electronic/Dance': 5, 'internacional': 5}
}

# Criação do DataFrame para preferências musicais
data_preferences = {'Age Group': list(preferences_demographics.keys())}
data_preferences.update({genre: [preferences_demographics[age][genre]
                        for age in preferences_demographics.keys()] for genre in genres})
df_preferences = pd.DataFrame(data_preferences)

# Unir as informações em um único DataFrame
df_combined = top_tracks.copy()

# Adicionar colunas para playlists mais tocadas
df_combined = df_combined.merge(df_top_playlists, on='Genre', how='left')

# Adicionar colunas para preferências musicais
for genre in genres:
    df_combined[f'{genre}_preference'] = df_combined['Age Group'].apply(
        lambda x: preferences_demographics[x][genre])

# Geocodificação das localizações
geolocator = Nominatim(user_agent="geoapiExercises")


def geocode(location):
    try:
        loc = geolocator.geocode(location)
        return pd.Series({'Latitude': loc.latitude, 'Longitude': loc.longitude})
    except:
        return pd.Series({'Latitude': None, 'Longitude': None})


# Geocodificação em paralelo
with ThreadPoolExecutor() as executor:
    results = list(executor.map(geocode, df_combined['Location']))

df_combined[['Latitude', 'Longitude']] = pd.DataFrame(results)

# Remover linhas com coordenadas não encontradas
df_combined = df_combined.dropna(subset=['Latitude', 'Longitude'])

# Caminho para salvar o arquivo CSV
output_path = 'spotify_music_insights_with_geo.csv'

# Exportar para CSV
df_combined.to_csv(output_path, index=False)

# Exibição dos DataFrames
print("Dados combinados:")
print(df_combined)

# Plotagem dos dados de preferências musicais (opcional)
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='Age Group', y='value', hue='variable',
                 data=pd.melt(df_preferences, ['Age Group']))
plt.title('Preferências Musicais por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Percentual')
plt.legend(title='Gênero')

# Adiciona a porcentagem em cada barra
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='edge')

plt.show()

# Carregar um mapa base a partir de um arquivo shapefile local
world = gpd.read_file(
    r'C:/Users/engda/OneDrive/Área de Trabalho/projeto_BI/ne_110m_admin_0_countries.shp')

# Criar um GeoDataFrame
gdf = gpd.GeoDataFrame(df_combined, geometry=gpd.points_from_xy(
    df_combined.Longitude, df_combined.Latitude))

# Plotar o mapa
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
gdf.plot(ax=ax, color='red', markersize=gdf['Count']*10, alpha=0.5)

# Adicionar rótulos
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['Location']):
    ax.text(x, y, label, fontsize=12, ha='right', color='black')

plt.title('Distribuição de Reproduções por Localização')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
