import spotipy
import matplotlib.pyplot as plt
import seaborn as sns
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from collections import Counter
from dotenv import load_dotenv
import os

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
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Função para obter playlists de um determinado gênero


def get_genre_playlists(genre):
    results = sp.search(q=f'genre:{genre}', type='playlist', limit=10)
    return results['playlists']['items']

# Função para obter dados das faixas de uma playlist


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


# Gêneros de interesse
genres = ['sertanejo', 'sertanejo universitario',
          'pagode', 'funk', 'pop', 'rock', 'jazz']

# Coleta de dados
genre_tracks = {}
for genre in genres:
    print(f"Coletando dados para o gênero: {genre}")
    playlists = get_genre_playlists(genre)
    tracks = []
    for playlist in playlists:
        tracks.extend(get_playlist_tracks(playlist['id']))
    genre_tracks[genre] = tracks

# Processamento dos dados para encontrar a música mais tocada por faixa etária e gênero
age_groups = ['Adolescentes', 'Jovens Adultos', 'Adultos', 'Idosos']
preferences = {
    'Adolescentes': ['sertanejo', 'sertanejo universitario', 'pagode', 'funk', 'pop', 'rock', 'jazz'],
    'Jovens Adultos': ['sertanejo', 'sertanejo universitario', 'pagode', 'funk', 'pop', 'rock', 'jazz'],
    'Adultos': ['sertanejo', 'sertanejo universitario', 'pagode', 'funk', 'pop', 'rock', 'jazz'],
    'Idosos': ['sertanejo', 'sertanejo universitario', 'pagode', 'funk', 'pop', 'rock', 'jazz']
}

top_tracks = {age: {genre: None for genre in genres} for age in age_groups}

for genre, tracks in genre_tracks.items():
    for age_group in age_groups:
        # Aqui, você precisará de dados reais para associar a faixa etária aos ouvintes.
        # Neste exemplo, vamos contar as ocorrências de cada música.
        track_counter = Counter([track['track']['name'] for track in tracks])
        if track_counter:
            most_common_track = track_counter.most_common(1)[0][0]
            top_tracks[age_group][genre] = most_common_track

# Preparação dos dados para o CSV das músicas mais tocadas por faixa etária e gênero
data_top_tracks = {'Faixa Etária': [], 'Gênero': [], 'Música Mais Tocada': []}

for age_group, genres_tracks in top_tracks.items():
    for genre, track in genres_tracks.items():
        data_top_tracks['Faixa Etária'].append(age_group)
        data_top_tracks['Gênero'].append(genre)
        data_top_tracks['Música Mais Tocada'].append(track)

df_top_tracks = pd.DataFrame(data_top_tracks)

# Exportar para CSV
df_top_tracks.to_csv('musicas_mais_tocadas_por_faixa_etaria.csv', index=False)

# Simulação de dados demográficos para preferências musicais (ajuste conforme necessário)
preferences_demographics = {
    'Adolescentes': {'sertanejo': 15, 'sertanejo universitario': 5, 'pagode': 15, 'funk': 30, 'pop': 25, 'rock': 5, 'jazz': 5},
    'Jovens Adultos': {'sertanejo': 10, 'sertanejo universitario': 15, 'pagode': 20, 'funk': 25, 'pop': 30, 'rock': 10, 'jazz': 5},
    'Adultos': {'sertanejo': 5, 'sertanejo universitario': 5, 'pagode': 10, 'funk': 15, 'pop': 20, 'rock': 30, 'jazz': 20},
    'Idosos': {'sertanejo': 5, 'sertanejo universitario': 0, 'pagode': 5, 'funk': 10, 'pop': 10, 'rock': 20, 'jazz': 50}
}

# Criação do DataFrame para preferências musicais
data_preferences = {'faixa_etaria': age_groups}
data_preferences.update({genre: [preferences_demographics[age][genre]
                        for age in age_groups] for genre in genres})

df_preferences = pd.DataFrame(data_preferences)

# Exportar para CSV
df_preferences.to_csv(
    'preferencias_musicais_por_faixa_etaria.csv', index=False)

# Exibição dos DataFrames
print("Músicas mais tocadas por faixa etária e gênero:")
print(df_top_tracks)

print("\nPreferências musicais por faixa etária:")
print(df_preferences)

# Plotagem dos dados de preferências musicais
plt.figure(figsize=(12, 8))
sns.barplot(x='faixa_etaria', y='value', hue='variable',
            data=pd.melt(df_preferences, ['faixa_etaria']))
plt.title('Preferências Musicais por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Percentual')
plt.legend(title='Gênero')
plt.show()
