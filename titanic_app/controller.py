
# coding: utf-8

import flask
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = flask.Flask(__name__) #init
app.config['DEBUG'] = True  # so that changes are automated



#-------- MODEL -----------#

df = pd.read_csv('titanic.csv')
include = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Survived']

# Create dummies and drop NaNs
df['Sex'] = df['Sex'].apply(lambda x: 0 if x == 'male' else 1)
df = df[include].dropna()

X = df[['Pclass', 'Sex', 'Age', 'Fare', 'SibSp']]
y = df['Survived']

PREDICTOR = RandomForestClassifier(n_estimators=100).fit(X, y)



#-------- ROUTES-----------#

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/hello")
def hello2():
	return "<strong> HELLO </strong>"  # can do html directly!


@app.route("/greet/<name>")
def greet(name):
    return "hello, my name is %s" %name


#-------- INPUT FORM ROUTE-----------#

@app.route('/input_page')
def send_form():
  return flask.render_template('input_page.html')  # run the html template in the template folder!



@app.route('/make_it_happen', methods=['POST']) 

# post allow us to accept inputs from user 
# cannot go to this 'url' directly

def say_hi():
  name = flask.request.form['myname']     # request from the input_page html file
  excitement_level = flask.request.form['mylevel']   # request from the input_page html file
  return flask.render_template('stuff_you_know.html', name=name, lvl=excitement_level) # run the html template

#-------- MODELLING INPUT WEBPAGE ROUTE-----------#

@app.route('/titanic_input')
def page():
   return flask.render_template('titanic_input.html')

@app.route('/titanic_result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':

       inputs = flask.request.form

       pclass = inputs['pclass'][0]
       sex = inputs['sex'][0]
       age = inputs['age'][0]
       fare = inputs['fare'][0]
       sibsp = inputs['sibsp'][0]

       item = np.array([pclass, sex, age, fare, sibsp]).reshape(1, -1)
       score = PREDICTOR.predict_proba(item)
       results = {'survival chances': score[0,1], 'death chances': score[0,0]}
       return flask.jsonify(results)


#-------- MODELLING API ROUTE-----------#

@app.route('/predict', methods=["GET"])
def predict():
    pclass = flask.request.args['pclass']
    sex = flask.request.args['sex']
    age = flask.request.args['age']
    fare = flask.request.args['fare']
    sibsp = flask.request.args['sibsp']

    item = np.array([pclass, sex, age, fare, sibsp]).reshape(1,-1)
    score = PREDICTOR.predict_proba(item)
    results = {'survival chances': score[0,1], 'death chances': score[0,0]}
    return flask.jsonify(results)




if __name__ == '__main__':   # more of like ensuring you are not running other stuff
    app.run()

