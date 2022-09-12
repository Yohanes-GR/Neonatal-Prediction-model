from flask import Flask, render_template, url_for, flash, redirect
import joblib
from flask import request
import numpy as np

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==12):
        loaded_model = joblib.load('hdp_modelss.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict', methods = ["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        
        if(len(to_predict_list)==12):
            result = ValuePredictor(to_predict_list,12)
    
    if(int(result)==0):
        prediction = "The baby has NEC"
    elif(int(result)==1):
        prediction = "The baby has parental asphyxia"
    elif(int(result)==2):
        prediction = "The baby has RDS"
    else:
        prediction = "The baby has Sepsis !!! :-)"
    return(render_template("prediction_result.html", prediction_text=prediction))       

if __name__ == "__main__":
    # Use below for local flask deployment
    #app.run(debug=True)
    
    #Use below for AWS EC2 deployment
    app.run(host='0.0.0.0',port=8080)
