from operator import index
from flask import Flask, render_template,url_for
import sqlite3

app=Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')







if __name__=='__main__':
    app.run(port=3000,debug=True)
    
    
    
    