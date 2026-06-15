import pandas as pd
import glob
import os
import numpy as np

folder_path = '/home/karassad/VLA-hack/simulation_data_fixed/data/chunk-000'
files = glob.glob(os.path.join(folder_path, "*.parquet"))

all_episode_durations = []

for file in files:
    try:
        # Читаем нужные колонки
        df = pd.read_parquet(file, columns=['episode_index', 'timestamp'])
        
        # Группируем по episode_index
        for ep_idx, group in df.groupby('episode_index'):
            # Длительность = последний timestamp - первый timestamp в эпизоде
            duration = group['timestamp'].iloc[-1] - group['timestamp'].iloc[0]
            all_episode_durations.append(duration)
            
    except Exception as e:
        print(f"Ошибка при чтении {file}: {e}")

if all_episode_durations:
    durations = np.array(all_episode_durations)
    print(f"Всего найдено эпизодов: {len(durations)}")
    print(f"Средняя длительность эпизода: {np.mean(durations):.6f}")
    print(f"Дисперсия длительности: {np.var(durations):.6f}")
    print(f"Минимальная длительность: {np.min(durations):.2f}")
    print(f"Максимальная длительность: {np.max(durations):.2f}")
else:
    print("Данные не найдены.")