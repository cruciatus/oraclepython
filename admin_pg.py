# -*- coding: utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import cx_Oracle

# configuration
DEBUG = True
SECRET_KEY = 'jwj2hw82823j1j23njh1hn2h3h8sk289'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/usuario/<user_id>/', methods=['GET', 'POST'])
def userid(user_id):
    opts={}
    user = 'system'
    password = '123'
    host = 'localhost'
    port = '1521'
    SID = 'orcl'
    dsn_tns = cx_Oracle.makedsn(host,port,SID)       
    try:
        conn = cx_Oracle.connect(user,password,dsn_tns)
        if request.method == 'POST':
            cursor = conn.cursor()
            cursor.execute ("select table_name from dba_tab_privs where grantee = '%s'" %(username))
            tablas = cursor.fetchall()
            for tabla in tablas:
                cursor = conn.cursor()
                cursor.execute("revoke all privileges on %s from %s" %(tabla[0],username))
                print "revoke all privileges on %s from %s" %(tabla[0],username)
            for k in request.form.keys():
                if k.startswith("caso_uso_"):
                    for gg in ROL[k.replace("caso_uso_", "")]:
                        cursor = conn.cursor()
                        cursor.execute(gg % (user_id))
                else:
                    for pr in request.values.getlist(k):
                        cursor = conn.cursor()
                        cursor.execute("grant %s on %s to %s" %(pr,k,user_id))
            conn.commit()
        opts["tables"] = []
        opts["casos_uso"] = []
        cursor = conn.cursor()
        cursor.execute ("select table_name from dba_tab_privs where grantee = '%s'" %(username))
        for table in cursor:
            tabs = {}
            cursor1 = conn.cursor()
            cursor1.execute ("select privilege from dba_tab_privs where grantee = '%s' and table_name = '%s'" %(username,table[1]))
            opts["tables"].append({"name":table[1], "privs":[i[0] for i in cursor1.fetchall()]})
        for cc in ROL:
            opts["casos_uso"].append({"name":cc, "selected":False})
    except cx_Oracle.DatabaseError, exc:
        return redirect(url_for('errordb'))
    return render_template('user.html', **opts)


@app.route('/usuarios')
def users():
    opts={}
    user = 'system'
    password = '123'
    host = 'localhost'
    port = '1521'
    SID = 'orcl'
    dsn_tns = cx_Oracle.makedsn(host,port,SID)       
    try:
        conn = cx_Oracle.connect(user,password,dsn_tns)
        cursor = conn.cursor()
        opts["users"] = []
        cursor.execute ("select username,user_id from dba_users where username != '%s' and created >= '04-JUN-2013'" % (user))
        for record in cursor:
			opts["users"].append({"username":record[0], "user_id":record[-1]})
        session["users"] = opts["users"]
    except cx_Oracle.DatabaseError, exc:
        return redirect(url_for('errordb'))
    return render_template('users.html', **opts)


@app.route('/usuario/<user_id>/delete')
def users_del(user_id):
    opts={}
    user = 'system'
    password = 'system'
    host = 'localhost'
    port = '1521'
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(host,port,SID)       
    try:
        conn = cx_Oracle.connect(user,password,dsn_tns)
        cursor = conn.cursor()
        cursor.execute ("delete user_id from dba_users where user_id != '%s''" % (user_id))
    except cx_Oracle.DatabaseError, exc:
        return redirect(url_for('errordb'))
    return render_template('users.html', **opts)



@app.route('/okdb', methods=['GET', 'POST'])
def okdb():
    return render_template('okdb.html')

@app.route('/errordb', methods=['GET', 'POST'])
def errordb():
    return render_template('errordb.html')


@app.route('/crearusuario', methods=['GET', 'POST'])
def createuser():
    opts={}
    user = 'system'
    password = '123'
    host = 'localhost'
    port = '1521'
    SID = 'orcl'
    dsn_tns = cx_Oracle.makedsn(host,port,SID)
    try:
        conn = cx_Oracle.connect(user,password,dsn_tns)

        if request.method == 'POST':
            try:
                username = request.form["username"]
                userpass = request.form["userpass"]
                cursor = conn.cursor()
                cursor.execute("""CREATE USER %s IDENTIFIED BY %s DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE TEMP QUOTA UNLIMITED ON USERS""" % (username, userpass))
                cursor.execute("grant CREATE DATABASE LINK, CREATE MATERIALIZED VIEW, CREATE PROCEDURE, CREATE PUBLIC SYNONYM, CREATE ROLE, CREATE SEQUENCE, CREATE SYNONYM, CREATE TABLE, CREATE TRIGGER, CREATE TYPE, CREATE VIEW to %s" % (username))
                
                cursor.execute("grant resource to %s" %(username))
                cursor.execute("grant connect to %s" % (username))
                conn.commit()
            except Exception as e:
                print e
                opts["errors"] = u"Error en la conexión de la base de datos. Verifique el host o el usuario"
    except cx_Oracle.DatabaseError, exc:
        return redirect(url_for('errordb'))

    return render_template('createuser.html', **opts)



@app.route('/', methods=['GET', 'POST'])
def home():
    opts = {}
    user = 'system'
    password = '123'
    host = 'localhost'
    port = '1521'
    SID = 'orcl'
    dsn_tns = cx_Oracle.makedsn(host,port,SID)       
    try:
        conn = cx_Oracle.connect(user,password,dsn_tns)
        return redirect(url_for('users'))
    except cx_Oracle.DatabaseError, exc:
        return redirect(url_for('errordb'))
    return render_template('index.html', **opts)

if __name__ == '__main__':
    app.run()
