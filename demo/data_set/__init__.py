import pandas as pd
import os, json
from datetime import datetime
class Env(object):
	def __init__(self):
		pass
	def reset(self):
		pass
	def step(self, action):
		observation=None
		reward=None
		done=None
		info=None
		pass
	def render(self):
		pass
	def observation_space(self):
		pass


def get_data_frame(sym, start, end):
	#to_datetime = lambda d: datetime.strptime(d, "%Y-%m-%d")
	path, filename = os.path.split(os.path.abspath(__file__))
	df=pd.read_csv(os.path.join(path,sym+".BK.csv"), index_col=[0],converters={'Date': pd.to_datetime})
	return df[(start.strftime("%Y-%m-%d")<df.index)&(df.index<=end.strftime("%Y-%m-%d"))].copy()

def get_symbol_key():
	path, filename = os.path.split(os.path.abspath(__file__))
	return json.load( open(os.path.join(path,"sym_key.json"),"r"))
def get_set_list():
	path, filename = os.path.split(os.path.abspath(__file__))
	out=[]
	for i in json.load( open(os.path.join(path,"set_list.json"),"r")):
		out.append(i.split('.')[0])
	return out
def new_columns(sym):
	return {
		'Open': sym+'_Open', 
		'High': sym+'_High',
		'Low':sym+'_Low',
		'Close':sym+'_Close',
		'Adj Close': sym,
		'Volume':sym+'_Volume'
		}
def get_adj(sym_list, start, end):
	sym=sym_list[0]
	df1=get_data_frame(sym,start,end)
	df1.rename(columns=new_columns(sym), inplace=True)
	#print(df1)
	df1 = df1[[df1.columns[4]]]
	for sym in sym_list[1:]:
		df2=get_data_frame(sym,start,end)
		df2.rename(columns=new_columns(sym), inplace=True)
		df2 = df2[[df2.columns[4]]]
		df1=pd.merge(df1,df2,how='outer',left_index=True, right_index=True)
	return df1.copy()

