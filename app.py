from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time

app = Flask(__name__, template_folder='templates')
CORS(app)

# --- NATIONAL DATABASE (Universities & Polytechnics) ---
COURSES = [
    {
        'id': 'cs',
        'title': 'Computer Science',
        'category': 'Technology',
        'description': 'Architect the digital future. Build AI, software, and secure systems.',
        'req_subjects': ['math', 'phys', 'comp'],
        'req_interests': ['code', 'build', 'sci'],
        'compulsory_subjects': ['math', 'phys'],
        'career_path': ['Junior Dev', 'Full Stack Engineer', 'System Architect', 'CTO'],
        'universities': [
            # Universities
            {'name': 'University of Lagos (UNILAG)', 'cutoff': 260, 'catchment': ['Lagos', 'Ogun', 'Osun', 'Oyo', 'Ekiti', 'Ondo'], 'tuition': '₦55,000', 'duration': '4 Years'},
            {'name': 'Ahmadu Bello University (ABU)', 'cutoff': 230, 'catchment': ['Kaduna', 'Kano'], 'tuition': '₦45,000', 'duration': '4 Years'},
            {'name': 'Covenant University', 'cutoff': 200, 'catchment': [], 'tuition': '₦1,200,000', 'duration': '4 Years'},
            # Polytechnics (Lower Cutoffs)
            {'name': 'Yaba College of Tech (YABATECH)', 'cutoff': 180, 'catchment': ['Lagos'], 'tuition': '₦40,000', 'duration': '2 Years (ND)'},
            {'name': 'Federal Poly Ilaro', 'cutoff': 170, 'catchment': ['Ogun'], 'tuition': '₦35,000', 'duration': '2 Years (ND)'},
            {'name': 'Lagos State Poly (LASUSTECH)', 'cutoff': 180, 'catchment': ['Lagos'], 'tuition': '₦50,000', 'duration': '4 Years'}
        ]
    },
    {
        'id': 'med',
        'title': 'Medicine & Surgery',
        'category': 'Health',
        'description': 'The pinnacle of healthcare. Diagnose, treat, and save lives.',
        'req_subjects': ['bio', 'chem', 'phys'],
        'req_interests': ['care', 'sci', 'build'],
        'compulsory_subjects': ['bio', 'chem', 'phys'],
        'career_path': ['House Officer', 'Resident Doctor', 'Consultant', 'Chief Medical Director'],
        'universities': [
            {'name': 'University of Ibadan (UI)', 'cutoff': 290, 'catchment': ['Oyo', 'Osun'], 'tuition': '₦60,000', 'duration': '6 Years'},
            {'name': 'University of Ilorin', 'cutoff': 260, 'catchment': ['Kwara'], 'tuition': '₦50,000', 'duration': '6 Years'},
            {'name': 'LASUCOM', 'cutoff': 275, 'catchment': ['Lagos'], 'tuition': '₦250,000', 'duration': '6 Years'},
            {'name': 'Afe Babalola University', 'cutoff': 200, 'catchment': [], 'tuition': '₦2,500,000', 'duration': '6 Years'}
            # Note: Polytechnics do not offer Medicine & Surgery
        ]
    },
    {
        'id': 'pet_eng',
        'title': 'Petroleum Engineering',
        'category': 'Engineering',
        'description': 'Power the nation. Explore, extract, and manage oil & gas resources.',
        'req_subjects': ['math', 'phys', 'chem'],
        'req_interests': ['build', 'money', 'sci'],
        'compulsory_subjects': ['math', 'phys', 'chem'],
        'career_path': ['Field Engineer', 'Drilling Supervisor', 'Reservoir Manager', 'Oil Executive'],
        'universities': [
            {'name': 'University of Benin (UNIBEN)', 'cutoff': 250, 'catchment': ['Edo', 'Delta'], 'tuition': '₦45,000', 'duration': '5 Years'},
            {'name': 'FUPRE (Warri)', 'cutoff': 230, 'catchment': ['Delta', 'Bayelsa'], 'tuition': '₦40,000', 'duration': '5 Years'},
            # Specialized Institute
            {'name': 'Petroleum Training Institute (PTI)', 'cutoff': 160, 'catchment': [], 'tuition': '₦30,000', 'duration': '2 Years (ND)'}
        ]
    },
    {
        'id': 'law',
        'title': 'Law',
        'category': 'Humanities',
        'description': 'Uphold the rule of law. Interpret constitutions and defend rights.',
        'req_subjects': ['lit', 'govt', 'eng'],
        'req_interests': ['law', 'write', 'debating'],
        'compulsory_subjects': ['lit', 'eng'],
        'career_path': ['Associate', 'Senior Counsel', 'Partner', 'SAN / Judge'],
        'universities': [
            {'name': 'UNILAG', 'cutoff': 270, 'catchment': ['Lagos', 'Ogun'], 'tuition': '₦55,000', 'duration': '5 Years'},
            {'name': 'Obafemi Awolowo University (OAU)', 'cutoff': 260, 'catchment': ['Osun', 'Oyo'], 'tuition': '₦45,000', 'duration': '5 Years'},
            {'name': 'Babcock University', 'cutoff': 200, 'catchment': [], 'tuition': '₦1,200,000', 'duration': '5 Years'}
        ]
    },
    {
        'id': 'acct',
        'title': 'Accounting',
        'category': 'Business',
        'description': 'The language of business. Manage finances and audit corporations.',
        'req_subjects': ['math', 'econ', 'eng'],
        'req_interests': ['money', 'law', 'build'],
        'compulsory_subjects': ['math', 'econ'],
        'career_path': ['Audit Trainee', 'Chartered Accountant', 'Finance Manager', 'CFO'],
        'universities': [
            {'name': 'UNILAG', 'cutoff': 250, 'catchment': ['Lagos'], 'tuition': '₦55,000', 'duration': '4 Years'},
            {'name': 'Covenant University', 'cutoff': 200, 'catchment': [], 'tuition': '₦900,000', 'duration': '4 Years'},
            # Polytechnics
            {'name': 'Yaba College of Tech', 'cutoff': 170, 'catchment': ['Lagos'], 'tuition': '₦40,000', 'duration': '2 Years (ND)'},
            {'name': 'Auchi Polytechnic', 'cutoff': 160, 'catchment': ['Edo'], 'tuition': '₦35,000', 'duration': '2 Years (ND)'},
            {'name': 'Kwara State Poly', 'cutoff': 150, 'catchment': ['Kwara'], 'tuition': '₦30,000', 'duration': '2 Years (ND)'}
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "mode": "production"})

@app.route('/recommend', methods=['POST'])
def recommend():
    time.sleep(1.2) # Cinematic delay for skeleton loader
    
    data = request.json
    user_grades = data.get('grades', {})
    user_interests = data.get('interests', [])
    user_jamb = data.get('jamb', 0)
    user_state = data.get('state', '')
    
    results = []

    for course in COURSES:
        # 1. Strict Validation
        qualified = True
        for sub in course.get('compulsory_subjects', []):
            if user_grades.get(sub, 0) < 3: # Need Credit (C4-C6)
                qualified = False
                break
        
        if not qualified: continue

        # 2. University Logic
        eligible_universities = []
        for uni in course.get('universities', []):
            effective_cutoff = uni['cutoff']
            # Catchment Bonus
            if user_state in uni.get('catchment', []):
                effective_cutoff -= 20
            
            if user_jamb >= effective_cutoff:
                eligible_universities.append(uni)

        # Skip course if no institution matches
        if not eligible_universities: continue

        # 3. Match Scoring
        score = 0
        for sub in course['req_subjects']:
            g = user_grades.get(sub, 0)
            if g >= 4: score += 20
            elif g == 3: score += 15
            elif g == 2: score += 5
        
        for interest in course['req_interests']:
            if interest in user_interests: score += 15
                
        if score >= 20:
            results.append({
                **course, 
                "score": score, 
                "universities": eligible_universities
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)