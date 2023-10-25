from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

app.secret_key = 'klajdokfjwoeijoigjodjf5498wfej38eruf9'

# Configure Flask-Mail for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "expenditure.cob@gmail.com"

app.config['MAIL_PASSWORD'] = "hrhdkdiwwzungmjz"

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Create a dictionary to map inputs to policy recommendations
policy_recommendations = {
    'EMPLOYED': ['DISABILITY INSURANCE'],
    'SELF-EMPLOYED': ['DISABILITY INSURANCE', 'LIFE INSURANCE'],
    'UNEMPLOYED': [],  # No recommendations for unemployed

    'SINGLE': [],  # No recommendations for single
    'MARRIED': ['LIFE INSURANCE', 'PERSONAL ARTICLES POLICY'],
    'ENGAGED': ['PERSONAL ARTICLES POLICY'],

    'Yes': ['LIFE INSURANCE', 'HOSPITAL INCOME POLICY', 'DISABILITY INSURANCE', 'PERSONAL LIABILITY UMBRELLA POLICY'],
    'No': [],  # No recommendations for no children or pets

    'Yes': ['PET MEDICAL INSURANCE', 'PERSONAL LIABILITY UMBRELLA POLICY'],
    'No': [],  # No recommendations for no pets

    'Yes': ['AUTO INSURANCE', 'DISABILITY INSURANCE'],
    'No': [],  # No recommendations for no vehicle

    'Yes': ['HOMEOWNERS INSURANCE POLICY', 'HOSPITAL INCOME POLICY', 'DISABILITY INSURANCE'],
    'No': ['RENTERS INSURANCE'],

    'Yes': ['RENTAL PROPERTY INSURANCE', 'PERSONAL LIABILITY UMBRELLA POLICY'],
    'No': [],  # No recommendations for no rental property

    'Yes': ['PERSONAL ARTICLES POLICY'],
    'No': []  # No recommendations for no jewelry or firearms
}

# Helper function to filter out repeated recommendations
def unique_recommendations(recommendations, existing_recommendations):
    return [r for r in recommendations if r not in existing_recommendations]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        occupation = request.form['occupation']
        email = request.form['email']
        pets = request.form['pets']
        marital_status = request.form['marital_status']
        children = request.form['children']
        vehicle = request.form['vehicle']
        house = request.form['house']
        rental_property = request.form['rental_property']
        jewelry_firearms = request.form['jewelry_firearms']
        life_events = request.form.getlist('life_events')

        # Generate policy recommendations based on user inputs
        recommendations = []

        # Occupation-based recommendations
        if occupation in policy_recommendations:
            recommendations.extend(policy_recommendations[occupation])

        # Marital status-based recommendations
        if marital_status in policy_recommendations:
            recommendations.extend(policy_recommendations[marital_status])

        # Children, Pets, Vehicle, House, Rental Property, Jewelry/Firearms recommendations
        recommendations.extend(policy_recommendations[children])
        recommendations.extend(policy_recommendations[pets])
        recommendations.extend(policy_recommendations[vehicle])
        recommendations.extend(policy_recommendations[house])
        recommendations.extend(policy_recommendations[rental_property])
        recommendations.extend(policy_recommendations[jewelry_firearms])

        # Life Events recommendations
        for event in life_events:
            if event in policy_recommendations:
                recommendations.extend(policy_recommendations[event])

        # Remove duplicate recommendations
        unique_recommendations = list(set(recommendations))

        # You can add any additional logic or formatting for the email body here
        email_body = f"Name: {name}\nAge: {age}\nEmail: {email}\n\nRecommended Policies:\n"
        for recommendation in unique_recommendations:
            email_body += f"• {recommendation}\n"

        msg = Message("P.I.P.R.E Results | The Agent's Office", sender='expenditure.cob@gmail.com', recipients=[email, 'expenditure.cob@gmail.com'])

        msg.body = email_body

        # You can customize the email template as needed
        msg.html = render_template('emailtemplate.html', name=name,age=age, occupation=occupation,recommendations=unique_recommendations, email=email,  pets=pets,marital_status=marital_status, children=children, vehicle=vehicle, house=house, rental_property=rental_property, jewelry_firearms=jewelry_firearms, life_events=life_events)

        try:
            mail.send(msg)
        except Exception as e:
            print(e)

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
