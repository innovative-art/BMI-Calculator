from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Route for landing page
@app.route('/')
def home():
    return render_template('landing.html')  # Landing page (NutraFit Introduction)


# Route for BMI calculator page
@app.route('/calculator')
def bmi_calculator():
    return render_template('index.html')  # BMI Calculator page

# Route to calculate BMI (API endpoint)
@app.route('/calculate', methods=['POST'])
def calculate_bmi():
    try:
        data = request.json

        # Retrieve and validate inputs
        gender = data.get('gender')
        age = data.get('age')
        height_cm = data.get('height')
        weight = data.get('weight')

        if not all([gender, age, height_cm, weight]):
            return jsonify({'error': 'All fields (gender, age, height, weight) are required'}), 400

        age = int(age)
        height_cm = float(height_cm)
        weight = float(weight)

        # Validate height and weight
        if height_cm <= 0:
            return jsonify({'error': 'Height must be greater than 0'}), 400
        if weight <= 0:
            return jsonify({'error': 'Weight must be greater than 0'}), 400

        # Convert height to meters and calculate BMI
        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)

        # Calculate ideal weight range
        min_weight = round(18.5 * (height_m ** 2), 2)
        max_weight = round(24.9 * (height_m ** 2), 2)

        # Provide recommendations with health risks, remedies, and food images
        if bmi < 18.5:
            status = "Underweight"
            diet = "Increase calorie intake with protein-rich and nutrient-dense foods."
            risks = [
                "Weakened immune system.",
                "Increased risk of malnutrition and osteoporosis.",
                "Possible fertility issues."
            ]
            remedies = [
                "Consume meals rich in calories and proteins like nuts, dairy products, and whole grains.",
                "Include regular strength training exercises to build muscle mass.",
                "Avoid skipping meals; eat frequently and prioritize healthy snacks."
            ]
            foods = {
                "Vegetables": [
                    {"name": "Sweet Potatoes", "image": "/static/images/sweet-potato.jpeg", "vegetarian": True},
                    {"name": "Avocados", "image": "/static/images/avocado.jpeg", "vegetarian": True}
                ],
                "Fruits": [
                    {"name": "Bananas", "image": "/static/images/banana.jpeg", "vegetarian": True},
                    {"name": "Mangoes", "image": "/static/images/mango.jpeg", "vegetarian": True}
                ],
                "Dishes": [
                    {"name": "Paneer Curry", "image": "/static/images/paneer-curry.jpeg", "vegetarian": True},
                    {"name": "Nut Butter Sandwich", "image": "/static/images/nut-butter-sandwich.jpeg", "vegetarian": True}
                ]
            }
        elif 18.5 <= bmi <= 24.9:
            status = "Normal"
            diet = "Maintain a balanced diet with proper portions of proteins, carbs, and fats."
            risks = ["Low risk of weight-related health issues."]
            remedies = [
                "Continue eating a balanced diet with fruits, vegetables, whole grains, and lean proteins.",
                "Stay active with regular physical activity like walking, cycling, or yoga.",
                "Monitor weight periodically to ensure stability."
            ]
            foods = {
                "Vegetables": [
                    {"name": "Broccoli", "image": "/static/images/broccoli.jpeg", "vegetarian": True},
                    {"name": "Spinach", "image": "/static/images/spinach.jpeg", "vegetarian": True}
                ],
                "Fruits": [
                    {"name": "Apples", "image": "/static/images/apple.jpeg", "vegetarian": True},
                    {"name": "Berries", "image": "/static/images/berries.jpeg", "vegetarian": True}
                ],
                "Dishes": [
                    {"name": "Grilled Chicken Salad", "image": "/static/images/grilled-chicken-salad.jpeg", "vegetarian": False},
                    {"name": "Vegetable Stir-fry", "image": "/static/images/vegetable-stir-fry.jpeg", "vegetarian": True}
                ]
            }
        elif 25 <= bmi <= 29.9:
            status = "Overweight"
            diet = "Adopt a calorie-controlled diet with an increased focus on vegetables, lean proteins, and healthy fats."
            risks = [
                "Higher risk of cardiovascular diseases.",
                "Possible onset of Type 2 diabetes.",
                "Increased risk of high blood pressure."
            ]
            remedies = [
                "Engage in regular aerobic exercises like jogging, swimming, or brisk walking.",
                "Reduce sugar and processed food intake; prioritize fresh and whole foods.",
                "Incorporate mindfulness techniques like meditation to reduce stress-related overeating."
            ]
            foods = {
                "Vegetables": [
                    {"name": "Cucumbers", "image": "/static/images/cucumber.jpeg", "vegetarian": True},
                    {"name": "Tomatoes", "image": "/static/images/tomato.jpeg", "vegetarian": True}
                ],
                "Fruits": [
                    {"name": "Watermelon", "image": "/static/images/watermelon.jpeg", "vegetarian": True},
                    {"name": "Oranges", "image": "/static/images/oranges.jpeg", "vegetarian": True}
                ],
                "Dishes": [
                    {"name": "Grilled Salmon with Vegetables", "image": "/static/images/grilled-salmon.jpeg", "vegetarian": False},
                    {"name": "Quinoa Salad", "image": "/static/images/quinoa-salad.jpeg", "vegetarian": True}
                ]
            }
        else:
            status = "Obese"
            diet = "Consult a healthcare provider for a personalized plan to reduce weight through a balanced diet and exercise."
            risks = [
                "Severe risk of cardiovascular diseases.",
                "Increased likelihood of Type 2 diabetes.",
                "Greater risk of joint issues and sleep apnea."
            ]
            remedies = [
                "Follow a medically-supervised diet plan tailored to your needs.",
                "Start with low-impact physical activities like swimming or walking.",
                "Avoid crash diets; instead, aim for sustainable lifestyle changes."
            ]
            foods = {
                "Vegetables": [
                    {"name": "Cauliflower", "image": "/static/images/cauliflower.jpeg", "vegetarian": True},
                    {"name": "Carrots", "image": "/static/images/carrot.jpeg", "vegetarian": True}
                ],
                "Fruits": [
                    {"name": "Apples", "image": "/static/images/apple.jpeg", "vegetarian": True},
                    {"name": "Pears", "image": "/static/images/pear.jpeg", "vegetarian": True}
                ],
                "Dishes": [
                    {"name": "Grilled Chicken Breast", "image": "/static/images/grilled-chicken.jpeg", "vegetarian": False},
                    {"name": "Zucchini Noodles", "image": "/static/images/zucchini-noodles.jpeg", "vegetarian": True}
                ]
            }

        return jsonify({
            'bmi': bmi,
            'status': status,
            'diet': diet,
            'risks': risks,  # Display risks first
            'remedies': remedies,  # Display remedies second
            'foods': foods,  # Display food details after risks and remedies
            'ideal_weight_range': f"{min_weight} kg - {max_weight} kg",
            'gender': gender,
            'age': age
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
