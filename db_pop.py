import pandas as pd
import sqlalchemy
import os
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))
con = engine.connect()

tables = pd.ExcelFile('TABLAS.xlsx')

for tab in tables.sheet_names:
	df = tables.parse(tab, dtype=object)
	print(df.info())
	print(df)
	df.to_sql(tab, con=engine, index=False, if_exists='append')
	engine.execute(f'SELECT * FROM {tab}').fetchall()