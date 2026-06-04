from datasets import Dataset
import pandas as pd
import glob
import os

folder_path = '/home/karassad/VLA-hack/simulation_data_fixed/data/chunk-000'
all_files = glob.glob(os.path.join(folder_path, "*.parquet"))

dataset_list = []
for f in all_files:
    try:
        # Загружаем как Dataset из HuggingFace
        ds = Dataset.from_parquet(f)
        dataset_list.append(ds)
        print(f"Успешно прочитан: {os.path.basename(f)}")
    except Exception as e:
        print(f"Не удалось прочитать {os.path.basename(f)}: {e}")

if dataset_list:
    # Объединяем все датасеты
    from datasets import concatenate_datasets

    combined_ds = concatenate_datasets(dataset_list)

    # Конвертируем в pandas DataFrame
    df = combined_ds.to_pandas()

    # Сохраняем
    df.to_parquet('combined_data.parquet', engine='pyarrow')
    print("Готово! Данные объединены в combined_data.parquet")
else:
    print("Не удалось загрузить ни одного файла.")