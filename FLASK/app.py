from flask import Flask,request,jsonify
import pickle

app=Flask(__name__) #Flask object

model = pickle.load(open('xgb.pkl','rb'))

@app.route('/predict',methods=['GET','POST'])
def predict():
    query = request.args
    input_1 = float(query.get('input_1'))
    input_2 = float(query.get('input_2'))
    input_3 = float(query.get('input_3'))
    input_4 = float(query.get('input_4'))
    input_5 = float(query.get('input_5'))
    input_6 = float(query.get('input_6'))                  
    input_7 = float(query.get('input_7'))
    input_8 = float(query.get('input_8'))
    pred_name = model.predict([[input_1,input_2,input_3,input_4,input_5,input_6,input_7,input_8]]).tolist()[0]
    return jsonify({'prediction':pred_name})
    
if __name__=="__main__":
    app.run(debug=True) #Not required for the server