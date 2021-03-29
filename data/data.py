import pandas as pd
import re
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)

ovid_df = pd.read_csv('owid-covid-data.csv')  
try:
  ovid_df.to_sql('owid', engine,schema=None,if_exists='replace',index=True,index_label=None)
  engine.execute('ALTER TABLE public.owid ADD PRIMARY KEY (index);')
except:
  print("to_sql failure")



# mts_df = pd.read_csv('Monthly_Transportation_Statistics.csv')
# mts_df.columns = [re.sub(r'\W+', '', x) for x in mts_df.columns]
# try:
# 	mts_df.to_sql('mts', engine,schema=None,if_exists='replace',index=True,index_label=None)
# 	engine.execute('ALTER TABLE public.mts ADD PRIMARY KEY (index);')
# except:
#   print("to_sql failure")
