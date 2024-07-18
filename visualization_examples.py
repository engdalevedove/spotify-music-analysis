import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dados Simulados
data_age_group = {
    'Age Group': ['Adolescentes', 'Adolescentes', 'Adolescentes', 'Jovens Adultos', 'Jovens Adultos', 'Jovens Adultos', 'Adultos', 'Adultos', 'Adultos', 'Idosos', 'Idosos', 'Idosos'],
    'Genre': ['pop', 'rock', 'funk', 'pop', 'rock', 'funk', 'pop', 'rock', 'funk', 'pop', 'rock', 'funk'],
    'Count': [120, 90, 150, 200, 180, 160, 110, 130, 100, 70, 60, 50]
}

data_gender = {
    'Gender': ['Masculino', 'Masculino', 'Masculino', 'Feminino', 'Feminino', 'Feminino', 'Outro', 'Outro', 'Outro'],
    'Genre': ['pop', 'rock', 'funk', 'pop', 'rock', 'funk', 'pop', 'rock', 'funk'],
    'Count': [150, 130, 120, 180, 170, 160, 90, 80, 70]
}

data_period = {
    'Period': ['2023-01', '2023-01', '2023-01', '2023-02', '2023-02', '2023-02', '2023-03', '2023-03', '2023-03'],
    'Genre': ['pop', 'rock', 'funk', 'pop', 'rock', 'funk', 'pop', 'rock', 'funk'],
    'Count': [300, 250, 200, 320, 270, 220, 340, 290, 240]
}

data_playlists = {
    'Playlist Name': ['Playlist A', 'Playlist B', 'Playlist C', 'Playlist D', 'Playlist E', 'Playlist F'],
    'Genre': ['pop', 'pop', 'rock', 'rock', 'funk', 'funk'],
    'Track Count': [120, 110, 130, 125, 140, 135]
}

df_age_group = pd.DataFrame(data_age_group)
df_gender = pd.DataFrame(data_gender)
df_period = pd.DataFrame(data_period)
df_playlists = pd.DataFrame(data_playlists)

# Função para adicionar porcentagens nas barras


def add_percentage(ax):
    total = sum([p.get_height() for p in ax.patches])
    for p in ax.patches:
        percentage = '{:.1f}%'.format(100 * p.get_height() / total)
        x = p.get_x() + p.get_width() / 2 - 0.05
        y = p.get_height()
        ax.annotate(f'{p.get_height()}\n({percentage})',
                    (x, y), ha='center', va='bottom')


# Gráfico 1: Distribuição de Músicas Mais Tocadas por Faixa Etária
plt.figure(figsize=(12, 8))
ax1 = sns.barplot(x='Age Group', y='Count', hue='Genre', data=df_age_group)
add_percentage(ax1)
plt.title('Distribuição de Músicas Mais Tocadas por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Número de Reproduções')
plt.legend(title='Gênero Musical')
plt.xticks(rotation=45)
plt.show()

# Gráfico 2: Popularidade de Gêneros Musicais por Gênero dos Usuários
plt.figure(figsize=(12, 8))
ax2 = sns.barplot(x='Gender', y='Count', hue='Genre', data=df_gender)
add_percentage(ax2)
plt.title('Popularidade de Gêneros Musicais por Gênero dos Usuários')
plt.xlabel('Gênero do Usuário')
plt.ylabel('Número de Reproduções')
plt.legend(title='Gênero Musical')
plt.show()

# Gráfico 3: Evolução das Reproduções ao Longo do Tempo
plt.figure(figsize=(12, 8))
ax3 = sns.lineplot(x='Period', y='Count', hue='Genre',
                   marker='o', data=df_period)
for line in ax3.lines:
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        ax3.annotate(f'{y}', (x, y), textcoords="offset points",
                     xytext=(0, 5), ha='center')
plt.title('Evolução das Reproduções ao Longo do Tempo')
plt.xlabel('Período')
plt.ylabel('Número de Reproduções')
plt.legend(title='Gênero Musical')
plt.show()

# Gráfico 4: Top Playlists Mais Tocadas por Gênero
plt.figure(figsize=(12, 8))
ax4 = sns.barplot(x='Playlist Name', y='Track Count',
                  hue='Genre', data=df_playlists)
add_percentage(ax4)
plt.title('Top Playlists Mais Tocadas por Gênero')
plt.xlabel('Nome da Playlist')
plt.ylabel('Número de Faixas')
plt.legend(title='Gênero Musical')
plt.xticks(rotation=45)
plt.show()
