from pathlib import Path
import pandas as pd

from loader import load_data, print_preview

sample = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'age': [25, 30, 28, 35, 22, 40],
    'score': [88, 92, 85, 90, 80, 95],
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Chengdu']
})

Path('sample.csv').write_text(sample.to_csv(index=False), encoding='utf-8')
sample.to_excel('sample.xlsx', index=False)

print('CSV 测试：')
df_csv = load_data(Path('sample.csv'))
print_preview(df_csv)

print('\nEXCEL 测试：')
df_excel = load_data(Path('sample.xlsx'))
print_preview(df_excel)
