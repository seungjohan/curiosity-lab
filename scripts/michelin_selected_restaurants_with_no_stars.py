import pandas as pd

df = pd.read_csv('/Users/seungjohan/researcher/raw/michelin_wine_list.csv')

no_star = df[df['Award'] == 'Selected Restaurants']
print(no_star[['Name', 'Location', 'Cuisine', 'Award']])