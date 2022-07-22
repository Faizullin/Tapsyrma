import sqlite3,random

_filename='static/db/main.db'
_table='hotels'

def try_do(func,*args,**kwargs):
	try:
		func(*args,**kwargs)
	except Exception as err:
		res =' '.join(err.args)
		return res
	return None
def insert(row,condition='',_commit=False):
	keys = tuple([c for c in row.keys()])
	vals = tuple([c for c in row.values()])
	return execute('INSERT INTO {} {} VALUES{} {}'.format(_table,keys,vals,condition),_commit=_commit)

def update( key,val,condition=''):
	if type(val) is str: val=f'\'{val}\''
	command='UPDATE {} SET {} = {} {}'.format(_table,key,val,condition)
	execute(command)

def delete(condition=''):
	command='DELETE FROM {} {}'.format(_table,condition)
	execute(command)

def execute(text,_b=False,_commit=True):
	with sqlite3.connect(_filename) as f:
		data=f.cursor().execute(text)
		if _commit:f.commit()
	if _b:
		return data

def select(el='*',condition='',_to_dict=False):
	command ='SELECT {} FROM {} {}'.format(el,_table,condition)
	with sqlite3.connect(_filename) as f:
		if _to_dict:f.row_factory = sqlite3.Row
		data = f.cursor().execute(command).fetchall()
	return data

def descriptin():
	res = execute('SELECT * FROM {}'.format(_table),_commit=False,_b=True).description
	return [i[0] for i in res]