from flask import Flask, render_template, request, redirect, url_for,flash
from config import *
import sql,logging

app=Flask(__name__)

@app.route('/')
def on_home():
	return render_template('htmls/home.html',info_path=info_path)

@app.route('/search/')
def on_search():
	info_path['blocks'] = sql.select()
	return render_template('htmls/search.html',info_path=info_path)

@app.route('/active_relax')
def on_active_relax():
	return render_template('htmls/active_relax.html',info_path=info_path)

@app.route('/nature')
def on_nature():
	return render_template('htmls/nature.html',info_path=info_path)

@app.route('/razvl')
def on_razvl():
	city='Нур-Султан'
	return render_template('htmls/razvl.html',info_path=info_path,razvl=razvl,city=city)

@app.route('/admin/')
def on_admin():
	data={
		'vals':sql.select(),
		'description':sql.descriptin(),
		'op_vals':{'place':places,'place_type':place_types}
	}
	return render_template('htmls/admin.html',data=data)

@app.route('/admin/add/',methods=['POST'])
def on_admin_add():
	res = request.form
	row={}
	for i in res:
		row[i] = res[i]
	app.logger.info(row)
	res=sql.try_do(sql.insert,row) 
	if not res:res=''
	return res

@app.route('/admin/delete/',methods=['POST'])
def on_admin_delete():
	res = request.get_json()['data']
	res=','.join([i[0] for i in res])
	app.logger.info(res)
	sql.delete(condition='WHERE id in ({})'.format(res))
	return ''

@app.route('/bye')
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return "До свидание"

if __name__=='__main__':
	app.run(debug=True)
