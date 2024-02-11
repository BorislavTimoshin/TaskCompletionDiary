import matplotlib.pyplot as plt
import pandas as pd

# Создаем набор данных
dates = pd.date_range('20220101', periods=1000)
values = pd.Series(range(1000), index=dates)
print(dates)
print(values)
# Строим график
plt.figure(figsize=(10, 6))
plt.plot(values.index, values.values)
plt.title('График результатов')
plt.xlabel('Дата')
plt.ylabel('Значение (м)')
plt.show()
