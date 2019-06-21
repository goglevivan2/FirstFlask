from flask import Flask,render_template,request,json
import methods
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
import work_xml
import parsing
app = Flask(__name__)
db_url='D:/1mai/stylo.db'
userlist_dir = 'D:/1mai/users/'
Name=''
ID = 1
def pr(a):
    print(a)
def CreateUser(_name, _email,_password):

    data = {'name': _name,
            'email': _email,
            'password': _password}
    with open(userlist_dir+_name, 'w')as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def zakfun():
    return render_template('zakaz.txt')

@app.route("/ord",methods=['POST'])
def ord():
    print('order')
    print('registed order in order_status')
    con = sqlite3.connect(db_url)
    methods.sqlite_insert1(con,'Order_status',{'realization':'start','username':Name})
    con.close()
    print('get ord_id')
    ord_id=0
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select ord_id from Order_status where username = ?;', [Name])
    res = cur.fetchall()
    ord_id = res[0][0]
    cur.close()
    con.close()
    print('add tovar from backets in orders')
    print(ord_id)
    bsk_buff=[]
    cus_id=''
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select cus_id from customers where cus_name = ?;', [Name])
    res = cur.fetchall()
    cus_id = res[0][0]
    cur.close()
    con.close()
    print(cus_id)
    arrayfororder=[]
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select pr_id,bsk_size from backets where cus_id = ?;', [cus_id])
    res = cur.fetchall()
    print(res)
    arrayfororder = res
    cur.close()
    con.close()
    print('make xml file')
    work_xml.xcreate(arrayfororder,Name,ord_id)#

    print(ord_id)
    for i in arrayfororder:
        pr_price=''
        con = sqlite3.connect(db_url)
        cur = con.cursor()
        cur.execute('select pr_price from products where pr_id = ?;', [i[0]])
        res = cur.fetchall()
        pr_price=res[0][0]
        cur.close()
        con.close()
        pr_price=float(pr_price)
        con = sqlite3.connect(db_url)
        cur = con.cursor()
        cur.execute('insert into orders values(?,?,?,?,?);',[ord_id,pr_price,cus_id,i[1],i[0]])
        con.commit()
        cur.close()
        con.close()

    print('clear backets')
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('delete from backets where cus_id = ?;', [cus_id])
    con.commit()
    cur.close()
    con.close()

    return render_template('ord.html')

@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/zakaz")
def zakaz():
    c_id = 0
    price=0
    price =float(price)

    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select cus_id from customers where cus_name = ?;',[Name])
    res = cur.fetchall()
    con.commit()
    c_id = res[0][0]
    cur.close()
    con.close()
    print(c_id)
    tovar = []
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select cus_id,pr_name, backets.pr_id, bsk_size, pr_price, pr_img from backets inner join products on backets.pr_id = products.pr_id where  cus_id = ?;',[c_id])
    res = cur.fetchall()
    con.commit()
    tovar = res
    cur.close()
    con.close()
    print(tovar)
    for i in tovar:
        price=price+i[3]*i[4]
    zn = 0
    zn = float(zn)
    return render_template('zakaz.html',name =Name ,tovar = tovar,itog_price=price, zn=zn)
@app.route("/suc")
def suc():
    global ID

    return render_template('suc.html')


@app.route('/bsk',methods=['POST'])
def bsk():
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select * from products;')
    res = cur.fetchall()
    i=1
    bsk_array=[]
    print(res)
    for r in res:
        try:
            _name = int(request.form['btnBsk'+str(i)])
        except:
            _name = 0
        if _name < 0:
            _name = 0
        if _name > r[3]:
            _name = 0
        if _name != 0:
            tempcase=[]
            tempcase.append(r[0])
            tempcase.append(r[1])
            tempcase.append(float(r[2]))
            tempcase.append(_name)
            bsk_array.append(tempcase)
        i = i+1
    print(bsk_array)
    price = 0
    price = float(price)
    for i in bsk_array:
        price = price+(i[2]*i[3])
    print('price:',price)

    cur.close()
    con.close()

    u_id = 0
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    cur.execute('select "cus_id" from "Customers" where cus_name = "'+Name+'";')
    res = cur.fetchall()
    u_id = res[0][0]
    print('User',u_id)
    cur.close()
    con.close()

    table="Backets"
    id = "cus_id"
    tovar = "pr_id"
    bsk_size ="bsk_size"
    i=0
    for t in bsk_array:
        conn = sqlite3.connect(db_url)
        methods.sqlite_insert1(conn,table,{id: u_id,tovar:bsk_array[i][0],bsk_size:bsk_array[i][3]})
        conn.close()
        conn = sqlite3.connect(db_url)
        cur = conn.cursor()

        cur.execute("update products set pr_size = pr_size - ? where pr_id = ?",(bsk_array[i][3],bsk_array[i][0]))

        conn.commit()
        cur.close()
        conn.close()
        i=i+1
    print('vse')
    return render_template('zakaz.txt')
@app.route("/stylo")
def stylo():
    tovar=[]
    con = sqlite3.connect(db_url)
    cur=con.cursor()
    cur.execute('select * from Products')
    res = cur.fetchall()
    for i in res:
        tovar.append(i)
    cur.close()
    con.close()
    return render_template('stylo.html',tovar = tovar,name = Name)

@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/adminwork')
def adminwork():
    return render_template('adminw.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
@app.route('/signUp',methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _telephone = request.form['inputTelephone']
    _pswd = generate_password_hash(_password,method='sha1' , salt_length = 3)
    print(methods.proverka(_name))
    z = methods.proverka(_name)
    if z:
        CreateUser(_name, _email, _pswd)
        con = sqlite3.connect('D:/1mai/stylo.db')
        methods.sqlite_insert(con,"Customers",{"cus_name":_name,
                                               "cus_tel": _telephone,
                                               "cus_pass":_pswd,
                                               "cus_addr": _email
                                              })



def CheckUser(_name,_password):

    con = sqlite3.connect('D:/1mai/stylo.db')
    cur = con.cursor()
    n = str(_name)
    cur.execute('select "cus_name","cus_pass" from customers;')
    res = cur.fetchall()
    for r in res:
        if r[0] ==_name:
            if check_password_hash(r[1],_password):
                con.commit()
                cur.close()
                con.close()
                return True
    else:
        con.commit()
        cur.close()
        con.close()
        return False


@app.route('/signIn', methods=['POST'])
def signIn():
    _name = request.form['inputName']
    _password = request.form['inputPassword']


    if CheckUser(_name,_password) ==True:
        if _name == "admin":
            return render_template('admin.txt')
        else:
            global Name
            Name = _name
            return render_template('shop.txt')







@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

    # validate the received values

if __name__ == '__main__':
    app.run()
    #app.run(debug = True,use_reloader=True)
