import pandas as pd
import sqlalchemy

DATABASE_URL='postgres://postgres:postgres@db:5432/packtrack?'

engine = sqlalchemy.create_engine(DATABASE_URL)
con = engine.connect()

tables = pd.ExcelFile('TABLAS.xlsx')

for tab in tables.sheet_names:
	df = tables.parse(tab, dtype=object)
	print(df.info())
	print(df)
	df.to_sql(tab, con=engine, index=False, if_exists='append')
	engine.execute(f'SELECT * FROM {tab}').fetchall()

