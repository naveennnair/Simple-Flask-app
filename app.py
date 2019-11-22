# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:45:37 2019

@author: naveenn
"""

from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)
os.chdir(r'C:\Users\Public\Documents\Python Scripts\Flask\Demo')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST','GET'])
def update():
    if request.method == 'POST':
        name = request.form['user_name']
        house = request.form['home_name']
        place = request.form['user_place']
        amount = int(request.form['user_amount'])
        given = int(request.form['amt_recieved'])
        
        df = pd.DataFrame({'Name' : name, 'House' : house, 'Place' : place, 'Amount' : amount,
                       'Given' : given, 'Balance' : (amount-given)}, index = [0])
        df = df[['Name','House','Place','Amount','Given','Balance']]        
        df.to_csv('User_details.csv', header = False, index = False, mode = 'a')       
#        df.to_csv('C:/Users/naveenn/Desktop/User_details.csv', header = False, index = False, mode = 'a')
        return render_template('signup.html')
    
@app.route('/Preview', methods = ["POST","GET"])
def preview():
    data = pd.read_csv('User_details.csv')
    df_summary = data.groupby(['Name','Home','Place','Given','Balance'])['Amount'].sum()
    df_summary.loc['Grand Total'] = df_summary.sum()
    df_summary = df_summary.reset_index()
    df_summary = df_summary[['Name','Home','Place','Amount','Given','Balance']]
    
    return render_template('preview.html',  tables=[df_summary.to_html(classes ='df_summary', header = "true")])
    
if __name__ == '__main__':
    app.run(debug = True)

