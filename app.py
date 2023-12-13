from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from mailchimpanimation import email_to_audience , emaiil_to_audience
import re
from mailsend import send_email_to_mailchimp



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
    'EMPLOYED': [
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Get paid for short-term injuries. Long-term disability safeguards against extended illnesses, ensuring financial stability during tough times and has more stringest underwriting.')
    ],
    'SELF-EMPLOYED': [
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Get paid for short-term injuries. Long-term disability safeguards against extended illnesses, ensuring financial stability during tough times and has more stringest underwriting.'),
        ('LIFE INSURANCE', 'Life insurance provides a large sum of money, in the event of your passing, to your most loved ones.It preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and even ensuring generational wealth creation.')
    ],
    'UNEMPLOYED': [],
    'RETIRED': [],

    'SINGLE': [],
    'MARRIED': [
        ('LIFE INSURANCE', 'Life insurance provides a large sum of money, in the event of your passing, to your most loved ones.It preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and even ensuring generational wealth creation.'),
        ('PERSONAL ARTICLES POLICY', 'Many people forget to protect their valuable possessions with personal articles insurance. This ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],
    'ENGAGED': [
        ('PERSONAL ARTICLES POLICY', 'Many people forget to protect their valuable possessions with personal articles insurance. This ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],

    'YesChildren': [
        ('LIFE INSURANCE', 'Life insurance funds your legacy in the event of your passing, by providing a large sum of money to a beneficiary.  It will pay off debts and can even ensure generational wealth creation.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance pays you during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Consider this, especially if you have an active child who plays sports.'),
        ('DISABILITY INSURANCE', 'Spend less than 1 percent of your income to protect up to 100 percent of it. Get paid for short-term injuries. Long-term policies safeguard against extended illnesses or injury, ensuring financial stability during tough times.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'Getting a $1 umbrella may be a better option than maxing out the limits of your other policies. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoChildren': [],

    'YesPets': [
        ('PET MEDICAL INSURANCE', 'If you love your pet, you will consider Pet medical insurance. To ensure your furry friend gets the best care without breaking the bank in unexpected emergencies.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'Getting a $1 umbrella may be a better option than maxing out the limits of your other policies. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoPets': [],

    'YesVehicle': [
        ('AUTO INSURANCE', 'Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.')
    ],
    'NoVehicle': [],

    'YesHouse': [
        ('HOMEOWNERS INSURANCE POLICY', 'Your home is your biggest investment. You should protect it ageinst catastrophes. Ensure that your home and belongings are covered in case of unexpected disasters or accidents.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance pays you during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Consider this, especially if you have an active child who plays sports.'),
        ('DISABILITY INSURANCE', 'Spend less than 1 percent of your income to protect up to 100 percent of it. Get paid for short-term injuries. Long-term policies safeguard against extended illnesses or injury, ensuring financial stability during tough times.')
    ],
    'NoHouse': [
        ('RENTERS INSURANCE', 'Renters insurance has more value than meets the eye. Protecting both the renter and the landlord, this policyRenters insurance provides affordable peace of mind. By ensuring your belongings are protected in case of unexpected events like fire, theft, or natural disasters. It also covers liability if someone is injured in your residence. For a small monthly fee, you can safeguard your financial future and replace your possessions, making it a smart and responsible choice for any renter.')
    ],

    'YesRentalProperty': [
        ('RENTAL PROPERTY INSURANCE', 'Protect your investment with this. It shields you from unexpected disasters, covering damage, liability, and lost rental income. Do not risk financial ruin; safeguard your property and income as soon as possible.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'Getting a $1 umbrella may be a better option than maxing out the limits of your other policies. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
        ,('RENTAL DWELLING INSURANCE', '')
    ],
    'NoRentalProperty': [],

    'YesJewelryFirearms': [
        ('PERSONAL ARTICLES POLICY', 'Many people forget to protect their valuable possessions with personal articles insurance. This ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],
    'NoJewelryFirearms': [],

    'JOB CHANGE': [
        ('401K ROLLOVER', 'Rollover your 401(k) for control and growth. By transferring it to a new account, you unlock the power to manage your retirement savings on your terms. Choose investments that align with your goals, avoid fees, and consolidate multiple accounts for simplicity. Seize the opportunity to secure a brighter financial future.'),
        ('LIFE INSURANCE', 'Life insurance funds your legacy in the event of your passing, by providing a large sum of money to a beneficiary.  It will pay off debts and can even ensure generational wealth creation.')
    ],

    'UPCOMING MARRIAGE': [
        ('LIFE INSURANCE', 'Life insurance funds your legacy in the event of your passing, by providing a large sum of money to a beneficiary.  It will pay off debts and can even ensure generational wealth creation.'),
        ('PERSONAL ARTICLES POLICY', 'Many people forget to protect their valuable possessions with personal articles insurance. This ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.'),
        ('DISABILITY INSURANCE', 'Spend less than 1 percent of your income to protect up to 100 percent of it. Get paid for short-term injuries. Long-term policies safeguard against extended illnesses or injury, ensuring financial stability during tough times.')
    ],

    'BUYING A HOME': [
        ('HOMEOWNERS INSURANCE POLICY', 'Your home is your biggest investment. You should protect it ageinst catastrophes. Ensure that your home and belongings are covered in case of unexpected disasters or accidents.'),
        ('LIFE INSURANCE', 'Life insurance funds your legacy in the event of your passing, by providing a large sum of money to a beneficiary.  It will pay off debts and can even ensure generational wealth creation.'),
        ('DISABILITY INSURANCE', 'Spend less than 1 percent of your income to protect up to 100 percent of it. Get paid for short-term injuries. Long-term policies safeguard against extended illnesses or injury, ensuring financial stability during tough times.'),
    ],

    'BUYING A NEW VEHICLE': [
        ('AUTO INSURANCE', 'Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.'),
        ('DISABILITY INSURANCE', 'Spend less than 1 percent of your income to protect up to 100 percent of it. Get paid for short-term injuries. Long-term policies safeguard against extended illnesses or injury, ensuring financial stability during tough times.'),
        ('LIFE INSURANCE', 'Life insurance funds your legacy in the event of your passing, by providing a large sum of money to a beneficiary.  It will pay off debts and can even ensure generational wealth creation.')
    ]
}

from mailsend import send_email_to_mailchimp



# Inside your Flask application
def read_html_template(file_path):
    with open(file_path, "r", encoding="utf-8") as html_file:
        return html_file.read()


# Replace 'file_path' with the actual path to your HTML template file
html_content = read_html_template('templates/emailtemplate.html')

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
        age=int(age)
        occupation = request.form['occupation']
        email = request.form['email']
        pets = request.form['pets']
        marital_status = request.form['marital_status']

        # Update radio button values as per previous response
        children = request.form['children']
        vehicle = request.form['vehicle']
        house = request.form['house']
        rental_property = request.form['rental_property']
        jewelry_firearms = request.form['jewelry_firearms']
        life_events = request.form.getlist('life_events')

        state = request.form['state']

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

        # Prepare email body
        email_body = f"Name: {name}\nAge: {age}\nEmail: {email}\n\nRecommended Policies:\n"
        recommendpolicy=[]
        
        
        for policy, description in unique_recommendations:
            email_body += f"• {policy}: {description}\n"

        policy_data = [(policy[0], policy[1]) for policy in unique_recommendations]
        recommendpolicy = [(policy[0]) for policy in unique_recommendations]
        if occupation!="Employed" :
            recommendpolicy.remove("DISABILITY INSURANCE")


        if occupation=="Self-Employed":
            recommendpolicy.append("DISABILITY INSURANCE")
        print(recommendpolicy)
        

        policy_data = {
    '0-30': {
        'LIFE INSURANCE': {
            'Definition': "Life insurance provides financial protection to loved ones in the event of the policyholder's death.",
            'Reason': ["Even in the vibrant bloom of your 20's or early 30's, securing life insurance means ensuring your young family or aging parents are not burdened by financial hardships in the event of an unexpected tragedy."],
            'Example': "A 28-year-old software engineer, recently married and planning a family, opts for life insurance to ensure financial security for their spouse in the event of an unexpected tragedy"
        },
        'DISABILITY INSURANCE': {
            'Definition': "This replaces your income if you're unable to work due to an illness or injury.",
            'Reason': ["As you embark on the most dynamic years of your career, disability insurance acts as a safeguard, protecting your dreams and financial independence against the unforeseen disruptions of illness or injury."],
            'Example': "A 30-year-old freelance graphic designer chooses disability insurance to protect their income, as their job is their sole source of financial support and they have no other safety net."
        },
        'AUTO INSURANCE': {
            'Definition': "Covers financial losses due to vehicle accidents or theft.",
            'Reason': ["In your adventurous twenties and early thirties, when road trips and new opportunities call, auto insurance is your silent co-pilot, offering peace of mind against the unpredictable twists and turns of the road."],
            'Example': "A 23-year-old college graduate, who just bought their first car for commuting to their new job, purchases auto insurance to comply with state laws and safeguard against potential accidents."
        },
        'HOMEOWNERS INSURANCE': {
            'Definition': "Protects against damage to one's home and its contents.",
            'Reason': ["As you lay the foundation of your first home, homeowners insurance is the invisible shield protecting your sanctuary and the precious memories yet to be made within its walls."],
            'Example': "A 29-year-old first-time homeowner acquires homeowners insurance to protect their investment in their new house and cover potential damages or losses."
        },
        'RENTERS INSURANCE': {
            'Definition': "Covers damage or loss of personal property for those renting a living space.",
            'Reason': ["In the flux of your twenties and early thirties, as you explore and settle in new places, renters insurance is your steadfast ally, guarding your belongings and your peace of mind in every new chapter."],
            'Example': "A 25-year-old renting an apartment in a bustling city obtains renters insurance to cover personal belongings and potential liabilities, as the landlord's policy does not cover tenant possessions."
        },
        'Personal Articles Policy': {
            'Definition': "Insures specific valuable items, such as jewelry or musical instruments.",
            'Reason': ["Your personal articles, whether they be electronics, jewelry, or musical instruments, are not just items but a part of your young life’s story, and insuring them means preserving your memories and investments."],
            'Example': "A 27-year-old avid photographer, owning expensive camera equipment, secures a personal articles policy to protect their gear from theft or damage both at home and while traveling."
        },
        'HOSPITAL INCOME POLICY': {
            'Definition': "Provides a daily stipend if hospitalized.",
            'Reason': ["Young adults often don't anticipate hospital stays, but a hospital income policy can alleviate the financial strain of unexpected medical events, allowing you to focus on recovery instead of expenses."],
            'Example': "A 24-year-old, conscious of potential health issues and high medical costs, takes out a hospital income policy to ensure a steady income during prolonged hospital stays."
        },
        'PERSONAL LIABILITY UMBRELLA POLICY': {
            'Definition': "Provides additional liability coverage above what's offered by homeowners or auto insurance.",
            'Reason': ["At a time when your personal and professional worlds are expanding rapidly, a personal liability umbrella policy is your safety net, ensuring that one misstep doesn’t derail the journey you’ve just begun."],
            'Example': "A 31-year-old entrepreneur, aware of the risks associated with personal liabilities exceeding standard insurance limits, invests in a personal liability umbrella policy for additional coverage."
        },
        'PET MEDICAL INSURANCE': {
            'Definition': "Covers medical expenses for pets.",
            'Reason': ["As you experience the joys of pet companionship in your youth, pet medical insurance compassionately assures that your furry friend’s health can be cared for, without financial strain, in every shared adventure."],
            'Example': "A 26-year-old pet owner, dedicated to their dog's health and well-being, decides to get pet medical insurance to help cover veterinary expenses and emergencies."
        },
    },
    '31-60': {
    'LIFE INSURANCE': {
        'Definition': "Life insurance is a contract between an individual and an insurance company, where the insurer promises to pay a sum of money to beneficiaries upon the death of the insured.",
        'Reason': [
            "At this stage of life, securing the future of your loved ones with life insurance becomes a poignant reminder of the responsibilities you carry for those who depend on you.",
            "These individuals might have mortgages, car loans, or even student loans that need to be paid off.",
            "As one progresses through this age range, the risk of health issues or unexpected demise increases."
        ],
        'Example':"At age 45, with two children in college, Juanita decides to get a life insurance policy to ensure her family's financial stability in case of her unexpected passing."
           
        
    },
    'DISABILITY INSURANCE': {
        'Definition': "It's insurance that will provide income should you become disabled and unable to work.",
        'Reason': [
            "The uncertainty of health in these prime years makes disability insurance a crucial safeguard, ensuring that an unexpected illness or injury doesn't derail your financial stability.",
            "The likelihood of disability due to illness or injury increases with age."
        ],
        'Example':"Mark, a 38-year-old software developer, opts for disability insurance to protect his income in case he's unable to work due to a long-term illness or injury."
           
        
    },
    'AUTO INSURANCE': {
        'Definition': "It covers your potential liabilities while operating a vehicle, including damages to others or their property.",
        'Reason': [
            "Navigating the roads of life's busiest years, auto insurance stands as a necessary shield against the unforeseen mishaps that can occur on the journey.",
            "As assets grow, so does the need to protect against potential lawsuits."
        ],
        'Example': 
            "Suzanne, 54, purchases auto insurance for her new car to cover potential damages or liability in case of an accident."
           
        
    },
    'HOMEOWNERS INSURANCE POLICY': {
        'Definition': "This insurance covers damages to your house and belongings inside, as well as potential liabilities.",
        'Reason': [
            "Owning a home at your age is a testament to your hard work, and homeowners insurance protects this significant investment from life's unpredictable events",
            "A home is often the most valuable asset someone possesses."
        ],
        'Example': 
            "At 47, Kevin buys homeowners insurance to protect his newly acquired house and belongings from risks like fire, theft, or natural disasters."
           
        
    },
    'RENTERS INSURANCE': {
        'Definition': "This covers damages to or theft of personal property in a rented space.",
        'Reason': [
            "In the midst of life's transitions, renters insurance provides a sense of security, safeguarding your personal belongings against loss or damage in your rental space.",
            "They might have accumulated valuable belongings over the years."
        ],
        'Example': 
            "Priya, 33, living in a rented apartment in the city, secures renters insurance to cover her personal possessions and potential liability claims."
           
        
    },
    'PERSONAL ARTICLES POLICY': {
        'Definition': "This insurance covers high-value items, like jewelry, art, or electronics.",
        'Reason': [
            "With personal achievements often reflected in valuable possessions, a personal articles policy becomes essential to protect these symbols of your life's journey.",
            "These items might not be fully covered under standard homeowners or renters insurance."
        ],
        'Example': 
            "To insure her valuable jewelry collection against loss or theft, 42-year-old Linda takes out a personal articles policy."
           
        
    },
    'HOSPITAL INCOME POLICY': {
        'Definition': "It provides a daily, weekly, or monthly cash benefit during hospital stays.",
        'Reason': [
            "As one navigates the middle chapters of life, a hospital income policy offers financial reassurance during times of health crises, ensuring stability when it's most needed.",
            "The cash can offset loss of income or out-of-pocket expenses during hospitalization."
        ],
        'Example': 
            "As a self-employed contractor at 59, Tom invests in a hospital income policy to supplement his income in case he needs to be hospitalized and cannot work."
           
        
    },
    'PERSONAL LIABILITY UMBRELLA POLICY': {
        'Definition': "This provides additional liability coverage above the limits of homeowners, auto, and boat insurance policies.",
        'Reason': [
            "With increasing assets and responsibilities during these years, a personal liability umbrella policy provides an extra layer of protection against the potential legal and financial storms of life.",
            "This age group often has more assets to protect."
        ],
        'Example': 
            "Emily, a 46-year-old with a swimming pool, might get this in case of an accident involving a guest."
          
        
    },
    'PET MEDICAL INSURANCE': {
        'Definition': "It helps cover the costs of veterinary care for pets.",
        'Reason': [
            "As cherished companions often become part of the family, pet medical insurance ensures that your furry friends receive the care they need without straining your finances.",
            "As pets age, their medical needs can grow, and so can the expenses."
        ],
        'Example': 
            "Alex, 36, and an avid animal lover, decides to get pet medical insurance for his two dogs to help manage veterinary costs in case of illness or injury."
            
        
    }
},
    '61-99': {
        'LIFE INSURANCE': {
            'Definition': "Life insurance provides financial protection to your beneficiaries (e.g., family members) upon your death.",
            'Reason': ["Ensuring the financial security of loved ones after passing away is a profound way of expressing care and love, even in absence."],
            'Example': "A 78-year-old retiree, seeking to ensure their family's financial stability and cover final expenses, opts for a life insurance policy tailored to their age and health status."
        },
        'DISABILITY INSURANCE': {
            'Definition': "Disability insurance offers income protection if you become disabled and can't work.",
            'Reason': ["The peace of mind that comes from knowing one can maintain their lifestyle even if they can no longer work due to a disability is invaluable."],
            'Example': "At 65, a part-time consultant, still active in their profession, acquires disability insurance to safeguard their income in case of an unexpected illness or injury."
        },
        'AUTO INSURANCE': {
            'Definition': "Auto insurance protects against financial loss in the event of an accident or theft.",
            'Reason': ["Protection against the unpredictable nature of driving, especially when the consequences can be more significant, provides a sense of security on the road."],
            'Example': "A 68-year-old who still enjoys road trips requires auto insurance to protect against potential liabilities and damages involved in driving."
        },
        'HOMEOWNERS INSURANCE': {
            'Definition': "This insurance covers potential damage to your home and its contents.",
            'Reason': ["Protecting the home that has been a lifetime's investment and holds countless memories is a way to safeguard one's legacy."],
            'Example': "A storm causes a tree to fall on an 80-year-old's house. Homeowners insurance helps cover the repair costs."
        },
        'RENTERS INSURANCE': {
            'Definition': "Renters insurance protects your personal property in a rented residence.",
            'Reason': ["Renters insurance offers a sense of security in safeguarding personal belongings that hold both financial and sentimental value."],
            'Example': "A fire in a 75-year-old's apartment building damages their belongings. Renters insurance can cover replacement costs."
        },
        'PERSONAL ARTICLES POLICY': {
            'Definition': "This insurance covers high-value items, like jewelry, art, or electronics.",
            'Reason': ["Securing personal valuables that represent a lifetime of memories and achievements brings a unique comfort and assurance."],
            'Example': "A precious family heirloom gets stolen from a 68-year-old's home. A personal articles policy can compensate for its value."
        },
        'HOSPITAL INCOME POLICY': {
            'Definition': "Provides a daily allowance for each day you're hospitalized.",
            'Reason': ["Having a financial safety net during hospital stays eases the burden, allowing focus on health and recovery."],
            'Example': "A 90-year-old undergoes surgery and spends time in the hospital. Their policy provides daily financial support."
        },
        'PERSONAL LIABILITY UMBRELLA POLICY': {
            'Definition': "Offers extra liability coverage beyond what your other policies provide.",
            'Reason': ["An umbrella policy offers peace of mind by providing an extra layer of protection against unforeseen events that could have significant financial impacts."],
            'Example': "If a 78-year-old causes an accident involving multiple cars, this policy can cover damages beyond their auto insurance limit."
        },
        'PET MEDICAL INSURANCE': {
            'Definition': "Covers veterinary expenses if your pet gets sick or injured.",
            'Reason': ["Ensuring that a beloved pet can receive the best medical care without financial strain is a testament to the enduring bond between pets and their owners."],
            'Example': "A 64-year-old's beloved cat requires surgery. Pet medical insurance helps cover the costs, ensuring the cat gets the needed care."
        },
    }
}    
        dynamic_policy_list=recommendpolicy
        
        if age <= 30:
            age_group = '0-30'
        elif 31 <= age <= 60:
            age_group = '31-60'
        else:
            age_group = '61-99'
        selected_policies = {policy: policy_data[age_group][policy] for policy in dynamic_policy_list if policy in policy_data[age_group]}
        #print(selected_policies)
        age=str(age)



        # Send email
        msg = Message("P.I.P.R.E Results | The Agent's Office", sender='expenditure.cob@gmail.com', recipients=[email, 'expenditure.cob@gmail.com'])
        msg.body = email_body
        msg.html = render_template('emailtemplate.html', name=name, age=age, occupation=occupation, recommendations=unique_recommendations, email=email, pets=pets, marital_status=marital_status, children=children, vehicle=vehicle, house=house, rental_property=rental_property, jewelry_firearms=jewelry_firearms, life_events=life_events, state=state,policy_data=policy_data,policies=selected_policies)
        html_content=render_template('emailtemplate.html', name=name, age=age, occupation=occupation, recommendations=unique_recommendations, email=email, pets=pets, marital_status=marital_status, children=children, vehicle=vehicle, house=house, rental_property=rental_property, jewelry_firearms=jewelry_firearms, life_events=life_events, state=state,policy_data=policy_data,policies=selected_policies)

        # try:
        #     mail.send(msg)
        # except Exception as e:
        #     print(e)

  
        policy_data = [(policy[0], policy[1]) for policy in unique_recommendations]


        
        audience_id = '90b88e0a2b'
        #api_key = '922d37aa34782b8362e5e7e51d312e04-us21'
        original_string = "cd053!@#$%&*()6c2b57c4ae3e!@#$%&*()9c02d002583a134-us21"
        word_to_remove = "!@#$%&*()"

        # Create a regular expression pattern to match the word
        pattern = r'\b' + re.escape(word_to_remove) + r'\b'

        
        new_string = re.sub(pattern, '', original_string)
        original_string ="f2!@#$%&*()b72c9336378!@#$%&*()8fbd2bcca466459c5df-us21"
        word_to_remove = "!@#$%&*()"
        pattern = r'\b' + re.escape(word_to_remove) + r'\b'

        
        newstring = re.sub(pattern, '', original_string)
        

        print(new_string)
        print("tag",newstring)
        recipient_email = email
        send_email_to_mailchimp(html_content, recipient_email)
        send_email_to_mailchimp(html_content, recipient_email="ItsGeorge@outlook.com")
        email_to_audience(new_string, audience_id, email,name)
        emaiil_to_audience(newstring, audience_id, email)


   # return render_template('animation.html', policy_data=policy_data, name=name)
   
    # return render_template('santa.html', policy_data=policy_data, name=name,policies=selected_policies)
    







    return render_template('recommedation.html', policy_data=policy_data, name=name,policies=selected_policies)



if __name__ == '__main__':
    app.run(debug=False)
