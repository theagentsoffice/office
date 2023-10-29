from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from mailchimpanimation import email_to_audience
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
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.')
    ],
    'SELF-EMPLOYED': [
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.')
    ],
    'UNEMPLOYED': [],
    'RETIRED': [],

    'SINGLE': [],
    'MARRIED': [
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],
    'ENGAGED': [
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],

    'YesChildren': [
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance provides financial support during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Most policies allow you to add your children as a rider. Consider this, especially if you have an active child who plays sports.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'A personal liability umbrella policy is crucial because it provides extra protection beyond your standard insurance coverage. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoChildren': [],

    'YesPets': [
        ('PET MEDICAL INSURANCE', 'Pet medical insurance provides peace of mind, ensuring your furry friend gets the best care without breaking the bank in unexpected emergencies.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'A personal liability umbrella policy is crucial because it provides extra protection beyond your standard insurance coverage. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoPets': [],

    'YesVehicle': [
        ('AUTO INSURANCE', 'Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.')
    ],
    'NoVehicle': [],

    'YesHouse': [
        ('HOMEOWNERS INSURANCE POLICY', 'Homeowners insurance provides financial protection, ensuring that your home and belongings are covered in case of unexpected disasters or accidents, giving you peace of mind.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance provides financial support during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Most policies allow you to add your children as a rider. Consider this, especially if you have an active child who plays sports.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.')
    ],
    'NoHouse': [
        ('RENTERS INSURANCE', 'Renters insurance provides affordable peace of mind, ensuring your belongings are protected in case of unexpected events like fire, theft, or natural disasters. It also covers liability if someone is injured in your residence. For a small monthly fee, you can safeguard your financial future and replace your possessions, making it a smart and responsible choice for any renter.')
    ],

    'YesRentalProperty': [
        ('RENTAL PROPERTY INSURANCE', 'Protect your investment and peace of mind with rental property insurance. It shields you from unexpected disasters, covering damage, liability, and lost rental income. Dont risk financial ruin; safeguard your property and income as soon as possible.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'A personal liability umbrella policy is crucial because it provides extra protection beyond your standard insurance coverage. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
        ,('RENTAL DWELLING INSURANCE', '')
    ],
    'NoRentalProperty': [],

    'YesJewelryFirearms': [
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],
    'NoJewelryFirearms': [],

    'JOB CHANGE': [
        ('401K ROLLOVER', 'Rollover your 401(k) for control and growth. By transferring it to a new account, you unlock the power to manage your retirement savings on your terms. Choose investments that align with your goals, avoid fees, and consolidate multiple accounts for simplicity. Seize the opportunity to secure a brighter financial future.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.')
    ],

    'UPCOMING MARRIAGE': [
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.')
    ],

    'BUYING A HOME': [
        ('HOMEOWNERS INSURANCE POLICY', 'Homeowners insurance provides financial protection, ensuring that your home and belongings are covered in case of unexpected disasters or accidents, giving you peace of mind.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance provides financial support during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Most policies allow you to add your children as a rider. Consider this, especially if you have an active child who plays sports.')
    ],

    'BUYING A NEW VEHICLE': [
        ('AUTO INSURANCE', 'Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.')
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
        #print(recommendpolicy)
        

        policy_data = {
    '0-30': {
        'LIFE INSURANCE': {
            'Definition': "Permanent life insurance is a type of life insurance that provides coverage for your entire lifetime, as long as you pay the premiums. It includes a savings component called cash value, which grows over time and can be used for various purposes.",
            'Reason': ["Having permanent life insurance at a young age (0-30) is a smart financial move because it not only offers a lifelong safety net for your loved ones in case something happens to you, but it also serves as a long-term savings and investment tool. It can help you build wealth and provide financial security for your future, including retirement."],
            'Example': "Imagine you're 25 years old and you purchase a permanent life insurance policy. Over the years, as you pay your premiums, the cash value within the policy grows tax-deferred. Before you know it, you can access this cash value to supplement your retirement income, pay for your children's education, or even use it for a down payment on a home. Plus, your beneficiaries will receive a tax-free death benefit when you pass away, ensuring your loved ones are financially protected."
        },
        'DISABILITY INSURANCE': {
            'Definition': "Disability insurance is a financial safety net that provides you with regular income if you become unable to work due to an illness or injury.",
            'Reason': ["Young adults entering the workforce face the risk of accidents or illnesses that could disrupt their income flow."],
            'Example': "Imagine you're 22 years old and you injure your back in a car accident, making it impossible to do your job for several months. Disability insurance would provide you with a portion of your salary during this time, allowing you to focus on your recovery without worrying about your finances."
        },
        'AUTO INSURANCE': {
            'Definition': "Auto insurance is a financial safety net that helps protect you and others in case of accidents involving your vehicle.",
            'Reason': ["Auto insurance is essential because it's the law in most places, and it shields you from potentially devastating financial consequences. It covers medical bills, repairs, and liability costs, which can add up to thousands of dollars if you're in an accident."],
            'Example': " Imagine you're a 29-year-old driver, and you accidentally rear-end another car at a stoplight. Without auto insurance, you could be personally responsible for paying the other driver's medical bills, repairing their car, and even covering your own medical expenses if you're injured. Auto insurance steps in to cover these costs, saving you from financial ruin."
        },
        'HOMEOWNERS INSURANCE': {
            'Definition': "Homeowners insurance is a type of coverage that protects you financially if you own a home. It typically covers damages to your house, personal belongings, and provides liability protection.",
            'Reason': [" Having homeowners insurance is crucial for young adults because it safeguards your investment in a home, shields you from unexpected disasters, and even covers you in case of certain accidents on your property."],
            'Example': "Imagine you're a 21-year-old who just bought your first house. You're excited about being a homeowner, but then a wildfire sweeps through your area, causing extensive damage to your home. Without homeowners insurance, you'd be left with a massive repair bill, potentially bankrupting you. However, with homeowners insurance, your policy would cover the repair costs, allowing you to rebuild your life without a crippling financial setback."
        },
        'RENTERS INSURANCE': {
            'Definition': "Renters insurance is a type of coverage that protects individuals who rent their homes or apartments. It typically includes coverage for personal belongings, liability protection, and additional living expenses in case your rented home becomes uninhabitable due to a covered event.",
            'Reason': ["If you're between the ages of 18-30 and renting a place to live, renters insurance is essential because it safeguards your personal belongings and financial well-being. It's not just about being responsible; it's about ensuring you're covered when unexpected events occur."],
            'Example': "Imagine you're a 24-year-old renting a cozy apartment. One day, a fire breaks out in the unit next to yours, causing smoke and water damage to your belongings. Without renters insurance, you'd be left to replace your furniture, electronics, and clothes on your own, which could cost thousands of dollars. But with renters insurance, your policy would likely cover the cost of replacing those items, helping you get back on your feet without a crippling financial burden. It's like having a safety net for life's unexpected curveballs."
        },
        'Personal Articles Policy': {
            'Definition': "Insures specific valuable items, such as jewelry or musical instruments.",
            'Reason': ["Young adults between the ages of 18-30 should consider a personal articles policy because it offers specialized protection for items like electronics, jewelry, musical instruments, or collectibles that may not be fully covered or have high deductibles under their regular insurance. It ensures that their valuable possessions are safeguarded against theft, loss, or damage."],
            'Example': "Let's say you're a 25-year-old with a passion for photography, and you own a high-end camera worth $2,000. Unfortunately, your camera gets stolen while you're on vacation. Without a personal articles policy, your standard renters or homeowners insurance might only cover a fraction of its value, leaving you with a substantial out-of-pocket expense. But with a personal articles policy, you can get full coverage for your camera, easing the financial burden and allowing you to replace it without breaking the bank."
        },
        'HOSPITAL INCOME POLICY': {
            'Definition': "A hospital income policy is a type of insurance that provides financial support in case you are hospitalized due to illness or injury. It offers a daily or weekly cash benefit to help cover expenses related to their hospital stay.",
            'Reason': ["Young adults between should consider a hospital income policy because it provides a safety net that can protect their finances during unexpected hospitalizations. At this stage in life, many may not have substantial savings or comprehensive health insurance, making it crucial to have an additional source of financial support when facing medical expenses."],
            'Example': "Imagine you're working and living independently. You're in good health and have a basic health insurance plan. One day, you have an accident that requires a week-long hospitalization. While your health insurance may cover some medical bills, it might not cover daily living expenses or other costs like transportation and meals. A hospital income policy would provide you with a daily cash benefit during your hospital stay, helping you maintain your financial stability and cover those unforeseen expenses, so you can focus on your recovery without worrying about money"
        },
        'PERSONAL LIABILITY UMBRELLA POLICY': {
            'Definition': "A personal liability umbrella policy is a type of insurance that provides additional coverage beyond what your standard auto, home, or renters insurance policies offer. It acts as a safety net to protect your assets and future earnings in case you're involved in a major liability lawsuit.",
            'Reason': ["The main reason young adults need a personal liability umbrella policy is to safeguard their financial future. This age group may not have substantial assets yet, but their potential future earnings are at risk if they're sued for a significant amount. Without this coverage, their savings, future income, and even personal property could be at stake in a lawsuit."],
            'Example': "Let's say you're a 29-year-old with a modest income and some savings in the bank. You accidentally cause a car accident that results in serious injuries to the other party. Your auto insurance covers up to $100,000 in liability, but the injured party's medical bills, lost wages, and pain and suffering claims exceed that amount, totaling $500,000. Without a personal liability umbrella policy, you might be personally responsible for the remaining $400,000, which could wipe out your savings and even lead to wage garnishment in the future. However, if you had a personal liability umbrella policy, it could step in to cover the additional $400,000, protecting your savings and future income."
        },
        'PET MEDICAL INSURANCE': {
            'Definition': "Pet medical insurance is a type of coverage that helps pay for the cost of veterinary care for your pets, such as dogs or cats, in case they get sick or injured.",
            'Reason': ["Many young adults adopt pets. Pet medical insurance provides financial protection and peace of mind. It helps ensure that they can afford unexpected medical expenses for their beloved furry companions without breaking the bank."],
            'Example': "Imagine you're a 28-year-old pet owner, and your energetic dog, Max, suddenly swallows something he shouldn't have. It results in an emergency trip to the vet, surgery, and a hefty bill of $3,000. Without pet medical insurance, you'd have to dig deep into your savings or rack up credit card debt. But with insurance, you only need to pay a manageable deductible, and the policy covers the rest, saving you from financial stress during an already worrying time."
        },
        'RENTAL DWELLING INSURANCE': {
            'Definition': "Landlord insurance is a specialized insurance policy designed for individuals who own rental properties. It provides financial protection for landlords in various situations related to their rental properties.",
            'Reason': ["If you're between the ages of 18-30 and own a rental property, landlord insurance is essential to safeguard your investment. It helps cover potential financial losses and liabilities that can arise from renting out your property to tenants."],
            'Example': "Imagine you're a 25-year-old who owns a small apartment you rent out to tenants. One day, a water pipe bursts, flooding your rental unit and causing significant damage. Without landlord insurance, you'd have to pay for repairs and lose rental income while the unit is uninhabitable. But with landlord insurance, you can make a claim to cover repair costs and even the lost rent during the repairs, helping you avoid a substantial financial setback."
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
        'Definition': "It helps cover the costs of veterinary care for pets.",
        'Reason': [
            "Pets are often considered part of the family.",
            "As pets age, their medical needs can grow, and so can the expenses."
        ],
        'Example': 
            "A 42-year-old's dog might need surgery, and the insurance can help offset the high vet bill."
            
            
        
    },
    'RENTAL DWELLING INSURANCE': {
            'Definition': "31-60",
            'Reason': ["RENTAL DWELLING INSURANCE"],
            'Example': "RENTAL DWELLING INSURANCE"
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
            'Definition': "61-122",
            'Reason': ["RENTAL DWELLING INSURANCE"],
            'Example': "RENTAL DWELLING INSURANCE"
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

        # Remove the word from the string
        new_string = re.sub(pattern, '', original_string)

        #print(new_string)
        recipient_email = email
        send_email_to_mailchimp(html_content, recipient_email)
        send_email_to_mailchimp(html_content, recipient_email="ItsGeorge@outlook.com")
        email_to_audience(new_string, audience_id, email)


   # return render_template('animation.html', policy_data=policy_data, name=name)
   
    # return render_template('santa.html', policy_data=policy_data, name=name,policies=selected_policies)
    







    return render_template('recommedation.html', policy_data=policy_data, name=name,policies=selected_policies)



if __name__ == '__main__':
    app.run(debug=False)
