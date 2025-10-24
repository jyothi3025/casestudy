from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_bmr(age, weight_kg, height_cm, gender):
    # Mifflin-St Jeor Equation
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return bmr

def activity_multiplier(level):
    # Simple mapping of activity level to multiplier
    mapping = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return mapping.get(level, 1.2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        age = int(request.form.get('age', 0))
        weight = float(request.form.get('weight', 0))  # in kg
        height = float(request.form.get('height', 0))  # in cm
        gender = request.form.get('gender', 'female')
        activity = request.form.get('activity', 'sedentary')

        bmr = calculate_bmr(age, weight, height, gender)
        tdee = bmr * activity_multiplier(activity)

        result = {
            'age': age,
            'weight': weight,
            'height': height,
            'gender': gender,
            'bmr': round(bmr, 2),
            'tdee': round(tdee, 2),
            'activity': activity
        }
        return render_template('result.html', result=result)
    except Exception as e:
        return f"Error processing request: {e}", 400

if __name__ == '__main__':
    # listen on 0.0.0.0 for container/k8s
    app.run(host='0.0.0.0', port=5000)
