import pandas as pd
import re

from sqlalchemy import create_engine
engine = create_engine('postgres://znoczexejlxcgr:fc7eab8a2fa0cfa7f3ac7ad8efee94389de447cf0c0f2fcd95281fa7214612a7@ec2-52-7-115-250.compute-1.amazonaws.com:5432/doai2olijqiuk')

ovid_df = pd.read_csv('owid-covid-data.csv')  
try:
  ovid_df.to_sql('owid', engine,schema=None,if_exists='replace',index=True,index_label=None)
  engine.execute('ALTER TABLE public.owid ADD PRIMARY KEY (index);')
except:
  print("to_sql failure")



mts_df = pd.read_csv('Monthly_Transportation_Statistics.csv')
mts_df.columns = [re.sub(r'\W+', '', x) for x in mts_df.columns]
try:
	mts_df.to_sql('mts', engine,schema=None,if_exists='replace',index=True,index_label=None)
	engine.execute('ALTER TABLE public.mts ADD PRIMARY KEY (index);')
except:
  print("to_sql failure")
