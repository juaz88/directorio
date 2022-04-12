from flask import Flask, redirect, render_template,url_for
import sqlite3

app=Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/view_admin',methods=['get','post'])
def admin():
    return render_template('view_admin.html')
    
@app.route('/login_admin', methods=['get','post'])
def login_admin():
    return render_template('login_admin.html')

@app.route('/legal')  
def legal():
    return render_template('login_admin.html')


if __name__=='__main__':
    app.run(port=3000,debug=True)
    
    
    
    