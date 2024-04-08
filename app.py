from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from transformers import pipeline
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/fyp'
app.config['SECRET_KEY'] = 'your_secret_key'  
db = SQLAlchemy(app)




class DPS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), primary_key=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password= db.Column(db.String(20), nullable=False)
    


@app.route('/')
def home():
     return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        passw = request.form["password"]
        data = DPS.query.filter_by(username=username).first()

        if data is None:
            print("No such user found.")
        else:
            if data.password == passw:
                return render_template('HomeReal.html', name=data.username)
            else:
                print("Incorrect Password")
    return render_template('login.html')



@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        '''Add entry to the database'''
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = DPS(username=username, email = email, password = password )
        db.session.add(entry)
        db.session.commit()
        return render_template('home.html')
    return render_template('signup.html')











qa_pairs = {
    "What is FBS or Fasting Blood Sugar?": "FBS refers to the blood sugar level measured after fasting for a certain period, usually overnight. It's an important indicator for diagnosing diabetes and monitoring blood sugar control.",
    "How does family history affect diabetes risk?": "Having a family history of diabetes can increase your risk of developing the condition. Genetic factors play a significant role in predisposing individuals to diabetes.",
    "What lifestyle factors affect diabetes risk?": "Lifestyle factors such as lack of exercise, unhealthy diet, smoking, and obesity can significantly increase the risk of developing diabetes.",
    "What is Gestational Diabetes?": "Gestational diabetes is a type of diabetes that occurs during pregnancy. It can lead to complications for both the mother and the baby if not properly managed.",
    "How does pregnancy affect diabetes risk?": "Pregnancy can increase the risk of developing gestational diabetes, especially in women with pre-existing risk factors such as obesity or a family history of diabetes.",
    "What should I do if the diabetes prediction system shows diabetes in my future?": "If the diabetes prediction system indicates a risk of developing diabetes in the future, it's important to take proactive steps to manage your health. This may include adopting a healthy diet, increasing physical activity, and regular monitoring of blood sugar levels. Consulting with a healthcare professional for personalized advice is also recommended.",
    "How accurate is the diabetes prediction system?": "The accuracy of the diabetes prediction system depends on various factors including the quality of data, the predictive model used (in this case, logistic regression), and the completeness of risk factors considered. While the system can provide valuable insights, it's important to interpret the results in conjunction with medical advice.",
    "Can diabetes be prevented?": "While certain risk factors for diabetes such as genetics cannot be changed, adopting a healthy lifestyle can significantly reduce the risk. This includes maintaining a healthy weight, eating a balanced diet, staying physically active, and avoiding smoking.",
    "What are the long-term complications of diabetes?": "Diabetes can lead to various complications including cardiovascular disease, kidney damage, nerve damage, eye problems, and foot problems. Proper management and control of diabetes can help reduce the risk of these complications.",
    "Hy or Hi hy or how r U": "How can i help you?",
    "What does BMI mean?": "BMI stands for Body Mass Index. It's a measure that uses your height and weight to estimate if you have a healthy body weight.",
    "Why does exercise matter for diabetes?": "Exercise helps your body use insulin better and can lower your blood sugar levels. It also helps you maintain a healthy weight and improves overall health.",
    "What is a healthy diet for diabetes?": "A healthy diet for diabetes includes plenty of fruits, vegetables, whole grains, lean proteins, and healthy fats. It's important to limit sugary foods and drinks.",
    "Can diabetes affect my eyesight?": "Yes, diabetes can affect your eyesight over time. It can lead to eye problems such as diabetic retinopathy, which can cause vision loss if not treated.",
    "Is it possible to reverse diabetes?": "In some cases, making lifestyle changes such as eating healthier and exercising more can help manage or even reverse type 2 diabetes, especially in the early stages.",
    "What are the signs of high blood sugar?": "Signs of high blood sugar include feeling thirsty, urinating more often than usual, feeling tired, blurry vision, and slow healing of cuts or wounds.",
    "How can I check my blood sugar at home?": "You can check your blood sugar at home using a blood glucose meter. You prick your finger and place a drop of blood on a test strip, then insert the strip into the meter for a reading.",
    "What should I do if I have a family history of diabetes?": "If you have a family history of diabetes, it's important to be proactive about managing your health. This includes eating a healthy diet, staying active, and getting regular check-ups with your doctor.",
    "Can stress affect diabetes?": "Yes, stress can affect blood sugar levels and make it harder to manage diabetes. Finding ways to manage stress, such as exercise, meditation, or talking to a friend, can help.",
    "What are the early signs of diabetes?": "Early signs of diabetes can include feeling very thirsty, feeling very hungry even when you've eaten, blurry vision, and tingling or numbness in the hands or feet."
}


def find_best_match(user_query):
    best_match_score = 0
    best_match_question = None
    for question in qa_pairs.keys():
        score = similarity_score(user_query, question)
        if score > best_match_score:
            best_match_score = score
            best_match_question = question
    return best_match_question

def similarity_score(str1, str2):
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())
    return len(words1.intersection(words2))

def get_bot_response(user_query):
    best_match_question = find_best_match(user_query)
    if best_match_question is not None:
        return qa_pairs[best_match_question]
    else:
        return "I'm sorry, I don't understand. Could you please rephrase your question?"

@app.route('/chatbot', methods=['POST'])
def chatbot():
    text = request.json.get('text')
    response = get_bot_response(text)
    return jsonify({'response': response})






@app.route('/ChatBot')
def chatbot_page():
    return render_template('ChatBot.html')

@app.route('/HomeReal')
def HomeReal():
    return render_template('HomeReal.html')

@app.route('/predict')
def predict():
    return render_template('index.html')

@app.route('/predictmale')
def predictmale():
    return render_template('indexmale.html')

@app.route('/RiskCal')
def Risk():
    return render_template('risk.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/aboutus')
def aboutus():
    return render_template('Aboutus.html')

@app.route('/IndexMale')
def male():
    return render_template('IndexMale.html')

@app.route('/NutriFitJourney')
def nutri():
    return render_template('NutriFitJourney.html')




@app.route('/result', methods=['POST'])
def result():
    Pragnancy = float(request.form['n2'])
    GestationalDiabetes = float(request.form['n3'])
    BMI = float(request.form['n4'])
    FBS = float(request.form['n5'])
    FamilyHistory = float(request.form['n7'])
    Exercise = float(request.form['n8'])
    IsDietHealthy = float(request.form['n9'])

    input_data = pd.DataFrame({
        'Pragnancy': [Pragnancy],
        'GestationalDiabetes': [GestationalDiabetes],
        'BMI': [BMI],
        'FBS': [FBS],
        'FamilyHistory': [FamilyHistory], 
        'Exercise': [Exercise],  
        'IsDietHealthy': [IsDietHealthy]  
    })

    # Load the trained model and scaler for female prediction
    model_Female = joblib.load('D:/DPS/DPS updated/ModelFemalData.pkl')
    scaler_Female = joblib.load('D:/DPS/DPS updated/ScalerFemalData.pkl')

    # Preprocess the input data for female prediction
    input_data_scaled = scaler_Female.transform(input_data)

    # Make predictions using the loaded model for females
    predictions = model_Female.predict(input_data_scaled)

    result_message = "You Will Get Diabetes In Future" if predictions[0] == 1 else "You Will Not Get Diabetes Soon"

    return render_template('result.html', result=result_message, result_message=result_message)






@app.route('/resultmale', methods=['POST'])
def resultmale():
    Age = float(request.form['nn1'])
    BMI = float(request.form['nn2'])
    HbA1c = float(request.form['nn3'])
    FamilyHistory = str(request.form['nn4'])
    Exercise = str(request.form['nn6'])
    Smoking = str(request.form['nn5'])
    HealthyDiet = str(request.form['nn7'])

    input_data = pd.DataFrame({
        'Age': [Age], 
        'BMI': [BMI],
        'HbA1c': [HbA1c],
        'FamilyHistory': [FamilyHistory],
        'Exercise': [Exercise],
        'Smoking': [Smoking],
        'HealthyDiet': [HealthyDiet]
    })

    # Load the trained model and preprocessor pipeline for male prediction
    pipeline = joblib.load('D:/DPS/DPS updated/ModelMaleData.pkl')

    # Make predictions using the loaded pipeline for males
    predictions = pipeline.predict(input_data)

    # Determine result message based on predictions
    if predictions[0] == 1:
        result_message = "You Will Get Diabetes In Future"
    elif predictions[0] == 2:
        result_message = "You Will Get Pre-Diabetes In Future"
    else:
        result_message = "You Will Not Get Diabetes Soon"

    return render_template('result.html', result=result_message, result_message=result_message)


if __name__ == '__main__':
    app.run(debug=True)


