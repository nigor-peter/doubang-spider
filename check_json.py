import json

with open('movies.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total movies: {len(data)}')
print('\nFirst 3 movies:')
print(json.dumps(data[:3], ensure_ascii=False, indent=2))

# 检查是否有完整的字段
print('\nChecking fields...')
for i, movie in enumerate(data[:5]):
    print(f'\nMovie {i+1}:')
    for key, value in movie.items():
        print(f'  {key}: {value}')