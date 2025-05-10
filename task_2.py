import pandas as pd
import json
from datasketch import HyperLogLog
import timeit

data = []
with open("/Users/anndunska/Downloads/lms-stage-access.log", "r") as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(data)

def count_unique_set(df):
    ip_set = set(df['remote_addr'])
    return len(ip_set)

def count_unique_hyperLogLog(df):
    hll = HyperLogLog()
    all_tags = df['remote_addr']
    for data in all_tags:
        hll.update(data.encode('utf-8'))
    return hll.count()

unique_ip_set = count_unique_set(df)
unique_ip_hyperLogLog = count_unique_hyperLogLog(df)

# Замір часу
set_time = timeit.timeit(lambda: count_unique_set(df), number=1)
hyperLogLog_time = timeit.timeit(lambda: count_unique_hyperLogLog (df), number=1)

# Побудова таблиці результатів згідно вимог
print("Результати порівняння:")
print(f"{'':<30}{'Точний підрахунок':>20}   {'HyperLogLog':>15}")
print(f"{'Унікальні IP-адреси':<30}{unique_ip_set:>20.3f}   {unique_ip_hyperLogLog:>15.3f}")
print(f"{'Час виконання (сек.)':<30}{set_time:>20.6f}   {hyperLogLog_time:>15.6f}")
