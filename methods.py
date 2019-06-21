from flask import Flask,render_template,request,json
import sqlite3
def proverka(_name):
    "Проверка имени на несуществование в бд"
    con = sqlite3.connect('D:/1mai/stylo.db')
    cur = con.cursor()
    n = str(_name)
    cur.execute('select ? from Customers where cus_name = ?;',("cus_name",n))
    res = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    if res ==[]:
        req = True
    else:
        req = False
    return req
def sqlite_insert(conn, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()
    conn.colse()
def uspsw(_name,_password):
    con = sqlite3.connect('D:/1mai/stylo.db')
    cur = con.cursor()
    cur.execute('select ? from Customers where cus_name = ? and cus_pass = ?;', ("cus_name", _name , _password))
    res = cur.fetchall()
    con.commit()
    cur.close()
    return res
def sqlite_insert1(conn, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()