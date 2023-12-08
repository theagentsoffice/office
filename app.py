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
        if occupation!="Employed":
            recommendpolicy.remove("DISABILITY INSURANCE")
        print(recommendpolicy)
        

        policy_data = {
    '0-30': {
        'LIFE INSURANCE': {
            'Definition': "Permanent life insurance provides lifelong coverage with a growing cash value component, as long as premiums are paid.",
            'Reason': ["Acquiring permanent life insurance between ages 0-30 is a wise financial decision, providing lifelong protection and serving as a long-term savings and investment tool for future security."],
            'Example': "As a young person, if you buy a permanent life insurance policy, its tax-deferred cash value grows with each premium. You can later use this for anything you want. Additionally, your beneficiaries get a tax-free death benefit."
        },
        'DISABILITY INSURANCE': {
            'Definition': "Spend less than 1 percent of your income to protect up to 100 percent of it. Get paid for short-term injuries. Long-term policies safeguard against extended illnesses or injury, ensuring financial stability during tough times.",
            'Reason': ["Young adults entering the workforce face the risk of accidents or illnesses that could disrupt their income flow."],
            'Example': "Imagine you're 22 years old and you injure your back in a car accident, making it impossible to do your job for several months. Disability insurance would provide you with a portion of your salary during this time, allowing you to focus on your recovery without worrying about your finances."
        },
        'AUTO INSURANCE': {
            'Definition': "Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.",
            'Reason': ["Car insurance is essential because it's the law in most places, and it shields you from potentially devastating financial consequences. It covers medical bills, repairs, and liability costs, which can add up to thousands of dollars if you're in an accident."],
            'Example': "If you're on the road and rear-end a car or your car is damaged, auto insurance protects you from this financial burden."
        },
        'HOMEOWNERS INSURANCE': {
            'Definition': "Your home is your biggest investment. You should protect it ageinst catastrophes. Homeowners insurance ensures that your home and belongings are covered in case of unexpected disasters or accidents.",
            'Reason': ["Having homeowners insurance is crucial for young adults because it safeguards your investment in a home, shields you from unexpected disasters, and even covers you in case of certain accidents on your property."],
            'Example': "At a young age, you buy your first house. A wildfire damages it. Without homeowners insurance, you face a huge repair bill, risking bankruptcy. With insurance, repairs are covered, saving you from severe financial strain."
        },
        'RENTERS INSURANCE': {
            'Definition': "Renters insurance has more value than meets the eye. Protecting both the renter and the landlord, this policy ensures your belongings are protected in case of unexpected events like fire, theft, or natural disasters. It also covers liability if someone is injured in your residence.",
            'Reason': ["If you're under 30 and renting a place to live, renters insurance is essential because it safeguards your personal belongings and reduces your financial liability in the event you cause major damage."],
            'Example': "You're a young person in a rented apartment and a neighboring fire damages your belongings, without renters insurance, you'd face huge replacement costs. With insurance, those costs are likely covered, providing a financial safety net for life's surprises."
        },
        'PERSONAL ARTICLES POLICY': {
            'Definition': "Insures specific valuable items, such as jewelry or musical instruments.",
            'Reason': ["Adults in your age range should get a personal articles policy to better protect valuables like electronics or jewelry, as regular insurance might not fully cover them against theft, loss, or damage."],
            'Example': "If you're passionate about photography with a $2,000 camera that gets stolen on vacation, standard renters or homeowners insurance might not fully cover its value. However, a personal articles policy ensures full coverage, saving you significant out-of-pocket costs."
        },
        'HOSPITAL INCOME POLICY': {
            'Definition': "Hospital income insurance pays you during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Consider this, especially if you have an active child who plays sports.",
            'Reason': ["Young adults should consider a hospital income policy to safeguard their finances during unexpected hospital stays, especially if they lack significant savings or comprehensive health insurance."],
            'Example': "If hospitalized unexpectedly for a week, health insurance may cover medical bills but not daily expenses like bills and meals. A hospital income policy provides a daily cash benefit during your stay, ensuring you can focus on recovery without financial worries."
        },
        'PERSONAL LIABILITY UMBRELLA POLICY': {
            'Definition': "A $1 umbrella may be a better option than maxing out the limits of your other policies. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.",
            'Reason': ["Young adults need a personal liability umbrella policy to protect their future earnings and assets from potential lawsuits. Without it, their savings, future income, and personal property are at risk."],
            'Example': "If you're under 30 with some savings and cause a car accident leading to injuries costing $500,000, your auto insurance may not fully cover the damages. Without an umbrella policy, you'd be risking your savings and future wages. An umbrella policy covers extra cost, safeguarding your finances."
        },
        'PET MEDICAL INSURANCE': {
            'Definition': "If you love your pet, you will consider Pet medical insurance. To ensure your furry friend gets the best care without breaking the bank in unexpected emergencies.",
            'Reason': ["Many young adults have pets. Pet medical insurance provides financial protection and peace of mind. It helps ensure that they can afford unexpected medical expenses for their beloved furry companions without breaking the bank."],
            'Example': "If you're dog named Max unexpectedly swallows a foreign object, you could face a $3,000 vet bill. Without pet insurance, this means draining savings or accruing debt. With insurance, you pay a small deductible and the rest is covered, sparing you financial strain in a stressful situation."
        },
        'RENTAL DWELLING INSURANCE': {
            'Definition': "Landlord insurance is a specialized insurance policy designed for individuals who own rental properties. It provides financial protection for landlords in various situations related to their rental properties.",
            'Reason': ["If you're between the ages of 18-30 and own a rental property, landlord insurance is essential to safeguard your investment. It helps cover potential financial losses and liabilities that can arise from renting out your property to tenants."],
            'Example': "If you're a 25-year-old with a rented apartment and a burst pipe causes damage, without landlord insurance you'd bear repair costs and lose rent. With insurance, you can claim both repair costs and lost rent, preventing a major financial loss."
        },
    },
    '31-60': {
    'LIFE INSURANCE': {
        'Definition': "Life insurance is a contract between an individual and an insurance company, where the insurer promises to pay a sum of money to beneficiaries upon the death of the insured.",
        'Reason': [
            "Most people in the 31-60 age bracket are in their prime working years. They often have dependents—like children, spouses, or even aging parents.",
            "These individuals might have mortgages, car loans, or even student loans that need to be paid off.",
            "As one progresses through this age range, the risk of health issues or unexpected demise increases."
        ],
        'Example':"A 40-year-old with young children might buy life insurance to ensure that their kids can go to college if something happens to them."
           
        
    },
    'DISABILITY INSURANCE': {
        'Definition': "It's insurance that will provide income should you become disabled and unable to work.",
        'Reason': [
            "This age group is heavily reliant on their income, whether it's for supporting a family, paying off debts, or saving for retirement.",
            "The likelihood of disability due to illness or injury increases with age."
        ],
        'Example':"A 35-year-old construction worker might get this insurance because their job is physically demanding."
           
        
    },
    'AUTO INSURANCE': {
        'Definition': "It covers your potential liabilities while operating a vehicle, including damages to others or their property.",
        'Reason': [
            "Individuals between 31-60 are often on the roads, driving kids around, commuting, or taking trips.",
            "As assets grow, so does the need to protect against potential lawsuits."
        ],
        'Example': 
            "A 45-year-old might need it not just for daily commutes, but also for those family road trips."
           
        
    },
    'HOMEOWNERS INSURANCE POLICY': {
        'Definition': "This insurance covers damages to your house and belongings inside, as well as potential liabilities.",
        'Reason': [
            "Many in this age bracket own homes.",
            "A home is often the most valuable asset someone possesses."
        ],
        'Example': 
            "If a storm damages a 52-year-old's roof, homeowners insurance can help cover repairs."
           
        
    },
    'RENTERS INSURANCE': {
        'Definition': "This covers damages to or theft of personal property in a rented space.",
        'Reason': [
            "Not everyone in this age range owns a home; many rent apartments or houses.",
            "They might have accumulated valuable belongings over the years."
        ],
        'Example': 
            "If a 33-year-old's apartment gets burglarized, renters insurance can cover the loss."
           
        
    },
    'PERSONAL ARTICLES POLICY': {
        'Definition': "This insurance covers high-value items, like jewelry, art, or electronics.",
        'Reason': [
            "Over the years, individuals might acquire more luxury or valuable items.",
            "These items might not be fully covered under standard homeowners or renters insurance."
        ],
        'Example': 
            "A 44-year-old might insure an heirloom necklace passed down through generations."
           
        
    },
    'HOSPITAL INCOME POLICY': {
        'Definition': "It provides a daily, weekly, or monthly cash benefit during hospital stays.",
        'Reason': [
            "As age progresses, hospital visits might become more frequent.",
            "The cash can offset loss of income or out-of-pocket expenses during hospitalization."
        ],
        'Example': 
            "A 58-year-old undergoing surgery might rely on this policy to cover extra costs not handled by health insurance."
           
        
    },
    'PERSONAL LIABILITY UMBRELLA POLICY': {
        'Definition': "This provides additional liability coverage above the limits of homeowners, auto, and boat insurance policies.",
        'Reason': [
            "As wealth grows, so does the potential target on one's back for lawsuits.",
            "This age group often has more assets to protect."
        ],
        'Example': 
            "A 46-year-old with a swimming pool might get this in case of an accident involving a guest."
          
        
    },
    'PET MEDICAL INSURANCE': {
        'Definition': "Pet medical insurance is a policy that covers the cost of veterinary care for pets, including dogs and cats.",
        'Reason': [
            "Having pet medical insurance between ages 31-60 is essential because as pets age, they are more likely to develop health issues, and medical expenses can become a significant financial burden.",
            "As pets age, their medical needs can grow, and so can the expenses."
        ],
        'Example': 
            "For instance, a 45-year-old pet owner might need insurance for their aging dog, who requires surgery for a tumor removal, and without insurance, the procedure could cost thousands of dollars, potentially straining their budget."
            
            
        
    },
    'RENTAL DWELLING INSURANCE': {
            'Definition': "Landlord insurance is a specialized insurance policy designed for individuals who own residential rental properties. It provides coverage for risks and liabilities associated with renting out a property to tenants.",
            'Reason': ["If you're aged 31-60 with a rental property, landlord insurance is vital to safeguard your investment, covering property damage, liability, and rental income losses."],
            'Example': "If you're a 45-year-old with a rental home and your tenant causes a kitchen fire, landlord insurance covers the repair costs, safeguarding your investment and income."
        },
},
    '61-99': {
        'LIFE INSURANCE': {
            'Definition': "Life insurance provides financial protection to your beneficiaries (e.g., family members) upon your death.",
            'Reason': ["As seniors, you might still have financial responsibilities like mortgages, or want to leave an inheritance or gift to loved ones or charities."],
            'Example': "Imagine you passed away unexpectedly, leaving behind unpaid medical bills. A life insurance policy would help cover these bills, ensuring your family doesn't bear the financial weight."
        },
        'DISABILITY INSURANCE': {
            'Definition': "Disability insurance offers income protection if you become disabled and can't work.",
            'Reason': ["While many in this age group might be retired, some are still working. The older you get, the more likely health issues can arise that may prevent working."],
            'Example': "If a 65-year-old still in the workforce suddenly becomes unable to work due to a severe illness, disability insurance can help maintain their lifestyle."
        },
        'AUTO INSURANCE': {
            'Definition': "Auto insurance protects against financial loss in the event of an accident or theft.",
            'Reason': ["Aging may affect driving abilities, increasing the risk of accidents."],
            'Example': "A 70-year-old driver gets into a fender bender. Their auto insurance can cover repair costs without affecting their savings."
        },
        'HOMEOWNERS INSURANCE': {
            'Definition': "This insurance covers potential damage to your home and its contents.",
            'Reason': ["Homes often have accumulated value over time and represent a significant portion of an older individual's net worth."],
            'Example': "A storm causes a tree to fall on an 80-year-old's house. Homeowners insurance helps cover the repair costs."
        },
        'RENTERS INSURANCE': {
            'Definition': "Renters insurance protects your personal property in a rented residence.",
            'Reason': ["Seniors might downsize to rental properties or live in senior communities."],
            'Example': "A fire in a 75-year-old's apartment building damages their belongings. Renters insurance can cover replacement costs."
        },
        'PERSONAL ARTICLES POLICY': {
            'Definition': "This insurance covers high-value items, like jewelry, art, or electronics.",
            'Reason': ["Over time, seniors might have collected valuable items like jewelry, art, or antiques."],
            'Example': "A precious family heirloom gets stolen from a 68-year-old's home. A personal articles policy can compensate for its value."
        },
        'HOSPITAL INCOME POLICY': {
            'Definition': "Provides a daily allowance for each day you're hospitalized.",
            'Reason': ["Older age can come with increased hospital stays or medical procedures."],
            'Example': "A 90-year-old undergoes surgery and spends time in the hospital. Their policy provides daily financial support."
        },
        'PERSONAL LIABILITY UMBRELLA POLICY': {
            'Definition': "Offers extra liability coverage beyond what your other policies provide.",
            'Reason': ["Assets and savings have often grown over a lifetime, and this policy can protect against large lawsuits."],
            'Example': "If a 78-year-old causes an accident involving multiple cars, this policy can cover damages beyond their auto insurance limit."
        },
        'PET MEDICAL INSURANCE': {
            'Definition': "Covers veterinary expenses if your pet gets sick or injured.",
            'Reason': ["Pets can be especially crucial companions for seniors, offering emotional support."],
            'Example': "A 64-year-old's beloved cat requires surgery. Pet medical insurance helps cover the costs, ensuring the cat gets the needed care."
        },
        'RENTAL DWELLING INSURANCE': {
            'Definition': "Landlord insurance is a specialized insurance policy designed for property owners who rent out their homes or apartments to tenants.",
            'Reason': ["Landlords need landlord insurance to protect their investment properties from financial losses caused by damages, liability claims, or loss of rental income."],
            'Example': "A 70-year-old landlord's insurance would cover repair costs and legal fees from a tenant-caused kitchen fire, protecting their retirement income."
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


        
        audience_id = '04ce018b2b'
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
        email_to_audience(new_string, audience_id, email)
        emaiil_to_audience(newstring, audience_id, email)


   # return render_template('animation.html', policy_data=policy_data, name=name)
   
    # return render_template('santa.html', policy_data=policy_data, name=name,policies=selected_policies)
    







    return render_template('recommedation.html', policy_data=policy_data, name=name,policies=selected_policies)



if __name__ == '__main__':
    app.run(debug=False)
