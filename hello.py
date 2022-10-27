# for i in range(12):
#     print(i)
#     if i < 11:
#         print('翻页')

import numpy as np
import pandas as pd

rows = []

row1 = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
row2 = [4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6]
row3 = [7, 8, 9, 7, 8, 9, 7, 8, 9, 7, 8, 9]

rows.append(row1)
rows.append(row2)
rows.append(row3)

np.array(rows)

df2 = pd.DataFrame(np.array(rows),
                   columns=['标题', '正文', '报纸名', '报纸级别', '作者名', '关键词', '报道日期', '版名', '版号',
                            '专辑', '专题', '分类号'])

print(df2)

df2.to_excel('cnki.xlsx', sheet_name='cnki')
