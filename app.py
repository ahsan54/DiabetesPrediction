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
    "What are the early signs of diabetes?": "Early signs of diabetes can include feeling very thirsty, feeling very hungry even when you've eaten, blurry vision, and tingling or numbness in the hands or feet.",
      "Type 1 Diabetes?": "Type 1 diabetes is a chronic condition where the pancreas produces little or no insulin. It often develops in children or young adults, and people with Type 1 diabetes need to take insulin injections for the rest of their lives.",
    "Type 2 Diabetes?": "Type 2 diabetes is a chronic condition where the body becomes resistant to insulin or doesn't produce enough insulin to maintain normal blood sugar levels. It is often associated with lifestyle factors such as obesity, physical inactivity, and unhealthy diet.",
    "What causes Type 2 Diabetes?": "Type 2 diabetes is primarily caused by lifestyle factors such as being overweight or obese, lack of physical activity, and unhealthy eating habits. Genetics and family history also play a role in predisposing individuals to Type 2 diabetes.",
    "How is Type 2 Diabetes managed?": "Type 2 diabetes is typically managed through lifestyle changes such as adopting a healthy diet, increasing physical activity, and losing weight if necessary. In some cases, medication or insulin therapy may also be prescribed to help control blood sugar levels.",
    "What are the risk factors for Type 2 Diabetes?": "Risk factors for Type 2 diabetes include obesity, lack of physical activity, unhealthy diet, family history of diabetes, age (risk increases with age), and certain ethnicities (such as African American, Hispanic, Native American, and Asian American populations).",
    "What are the complications of Type 2 Diabetes?": "Untreated or poorly managed Type 2 diabetes can lead to various complications including heart disease, stroke, kidney damage, nerve damage (neuropathy), eye problems (diabetic retinopathy), and foot problems (diabetic neuropathy). It's important to manage Type 2 diabetes effectively to reduce the risk of complications.",
    "What are the symptoms of Type 2 Diabetes?": "Symptoms of Type 2 diabetes may include increased thirst, frequent urination, unexplained weight loss, fatigue, blurred vision, slow wound healing, and frequent infections. However, some people with Type 2 diabetes may not experience any symptoms initially.",
    "Can Type 2 Diabetes be reversed?": "In some cases, Type 2 diabetes can be managed or even reversed through lifestyle changes such as weight loss, healthy eating, and regular physical activity. However, this depends on individual factors such as the duration of the condition and overall health status. It's important to consult with a healthcare professional for personalized advice and management.",
    "What is the difference between Type 1 and Type 2 Diabetes?": "Type 1 diabetes is an autoimmune condition where the body's immune system attacks and destroys insulin-producing cells in the pancreas, leading to a lack of insulin production. Type 2 diabetes, on the other hand, is characterized by insulin resistance (where the body's cells don't respond properly to insulin) and/or insufficient insulin production. Type 1 diabetes typically develops in childhood or young adulthood, while Type 2 diabetes is more common in adults and is often associated with lifestyle factors such as obesity and physical inactivity.",
    "How common is Type 2 Diabetes?": "Type 2 diabetes is the most common form of diabetes, accounting for approximately 90-95% of all diagnosed cases of diabetes. It affects millions of people worldwide and its prevalence is increasing, particularly due to rising obesity rates and sedentary lifestyles.",
    "What are the treatment options for Type 2 Diabetes?": "Treatment for Type 2 diabetes may include lifestyle changes such as diet and exercise, oral medications to lower blood sugar levels, and/or insulin therapy. The goal of treatment is to manage blood sugar levels effectively and reduce the risk of complications.",
    "Can Type 2 Diabetes lead to other health problems?": "Yes, if left untreated or poorly managed, Type 2 diabetes can lead to various health problems including heart disease, stroke, kidney damage, nerve damage, eye problems, and foot problems. It's important to manage Type 2 diabetes effectively to reduce the risk of complications.",
     "What is Type 1 Diabetes?": "Type 1 diabetes is a chronic autoimmune condition in which the immune system mistakenly attacks and destroys insulin-producing beta cells in the pancreas. As a result, the body produces little to no insulin, a hormone necessary to regulate blood sugar levels.",
    "What causes Type 1 Diabetes?": "The exact cause of Type 1 diabetes is not fully understood, but it is believed to involve a combination of genetic predisposition and environmental factors, such as viral infections or exposure to certain toxins, that trigger the autoimmune response.",
    "Who is at risk for Type 1 Diabetes?": "Type 1 diabetes can develop at any age, but it is most commonly diagnosed in children, adolescents, and young adults. It is not directly linked to lifestyle factors such as diet or physical activity, and there is often a genetic predisposition involved.",
    "How is Type 1 Diabetes managed?": "Type 1 diabetes is typically managed with insulin therapy, which involves injecting insulin to replace the hormone that the body is unable to produce. Individuals with Type 1 diabetes also need to monitor their blood sugar levels regularly and make adjustments to their insulin doses based on factors such as food intake, physical activity, and illness.",
    "What are the symptoms of Type 1 Diabetes?": "Symptoms of Type 1 diabetes may include increased thirst, frequent urination, extreme hunger, unexplained weight loss, fatigue, irritability, blurred vision, and slow-healing wounds or sores. These symptoms can develop rapidly over a short period of time.",
    "Can Type 1 Diabetes be prevented?": "Currently, there is no known way to prevent Type 1 diabetes. It is not caused by lifestyle factors such as diet or exercise, and there is no proven method for preventing the autoimmune response that leads to the destruction of insulin-producing cells in the pancreas.",
    "What are the complications of Type 1 Diabetes?": "Untreated or poorly managed Type 1 diabetes can lead to various complications including heart disease, stroke, kidney damage, nerve damage (neuropathy), eye problems (diabetic retinopathy), and foot problems (diabetic neuropathy). It's important to manage Type 1 diabetes effectively to reduce the risk of complications.",
    "What is the difference between Type 1 and Type 2 Diabetes?": "Type 1 diabetes is an autoimmune condition where the body's immune system attacks and destroys insulin-producing cells in the pancreas, leading to a lack of insulin production. Type 2 diabetes, on the other hand, is characterized by insulin resistance (where the body's cells don't respond properly to insulin) and/or insufficient insulin production. Type 1 diabetes typically develops in childhood or young adulthood, while Type 2 diabetes is more common in adults and is often associated with lifestyle factors such as obesity and physical inactivity.",
    "How common is Type 1 Diabetes?": "Type 1 diabetes is less common than Type 2 diabetes, accounting for approximately 5-10% of all diagnosed cases of diabetes. It affects millions of people worldwide, and its prevalence varies by region.",
    "how r U": "How can i help you?",
     "hyyyyyyyyyyy hyyyyyy hyyyy hyyy hy ": "How can i help you?",
       "What is sugar disease?": "Sugar disease, also known as diabetes, is a condition where your blood sugar levels become too high. It can cause serious health problems if not managed properly.",
    "How do I know if I have sugar disease?": "You might have sugar disease if you feel very thirsty, pee a lot, feel very hungry even after eating, or have blurry vision. See a doctor for a check-up.",
    "Can sugar disease go away on its own?": "No, sugar disease doesn't go away by itself. It needs treatment, like medicine, healthy habits, and regular check-ups with a doctor.",
    "How can I prevent sugar disease?": "To prevent sugar disease, eat healthy foods like fruits, veggies, and whole grains. Avoid sugary drinks and snacks. Stay active by walking or doing other activities.",
    "Is sugar disease dangerous?": "Yes, sugar disease can be dangerous if not managed well. It can cause heart disease, kidney damage, and eye problems. Follow your doctor's advice seriously.",
    "What foods should I avoid if I have sugar disease?": "Avoid sugary and starchy foods like sweets, sugary drinks, white bread, and fried foods. Eat more fruits, veggies, and whole grains instead.",
    "Can sugar disease affect my eyes?": "Yes, sugar disease can hurt your eyes if not managed. It can cause blurry vision, glaucoma, or even blindness. Get regular eye check-ups if you have sugar disease.",
    "How do I check my blood sugar?": "Use a glucometer. Prick your finger, put a drop of blood on a strip, and insert it into the glucometer. It shows your blood sugar level.",
       "Cure for Type 1 Diabetes?": "No cure yet.",
    "Cure for Type 2 Diabetes?": "Not fully, but can be managed.",
    "Can Type 1 Diabetes be reversed?": "No.",
    "Can Type 2 Diabetes be reversed?": "Sometimes, with lifestyle changes.",
    "Any treatments to cure diabetes?": "No cure, but treatments help manage.",
    "Latest research on curing diabetes?": "Researchers are still studying."



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
    BMI = float(request.form['n1'])
    FBS = float(request.form['n2'])
    Pragnancy = (request.form['n3'])
    GestationalDiabetes = (request.form['n4'])
    FamilyHistory = (request.form['n5'])
    Exercise = (request.form['n6'])
    HealthyDiet = (request.form['n7'])

    input_data = pd.DataFrame({
        'BMI': [BMI],
        'FBS': [FBS],
        'Pragnancy': [Pragnancy],
        'GestationalDiabetes': [GestationalDiabetes],
        'FamilyHistory': [FamilyHistory], 
        'Exercise': [Exercise],  
        'HealthyDiet': [HealthyDiet]  
    })


    pipeline = joblib.load('D:\DPS\DPS updated\ModelFemalData.pkl')

    predictions = pipeline.predict(input_data)


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


    result_message = "You Will Get Diabetes In Future" if predictions[0] == 1 else "You Will Not Get Diabetes Soon"



    return render_template('resultmale.html', result=result_message, result_message=result_message)


if __name__ == '__main__':
    app.run(debug=True)


