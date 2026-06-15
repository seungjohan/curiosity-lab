SELECT *
FROM read_csv_auto('/Users/seungjohan/Cursor/brainstorming/raw/michelin_wine_list.csv')
WHERE Award = 'Selected Restaurants';