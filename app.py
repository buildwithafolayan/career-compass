from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time

# Initialize Flask and tell it where the HTML file is
app = Flask(__name__, template_folder='templates')
CORS(app)

# --- DATABASE / KNOWLEDGE BASE ---
COURSES = [
    {
        'id': 'cs',
        'title': 'Computer Science',
        'category': 'Technology',
        'description': 'Design the future of software, AI, and digital systems.',
        'req_subjects': ['math', 'phys', 'comp'],
        'req_interests': ['code', 'build', 'sci'],
        'compulsory_subjects': ['math', 'phys'],
        'universities': [
            {'name': 'University of Lagos (UNILAG)', 'cutoff': 260, 'catchment': ['Lagos', 'Ogun', 'Osun', 'Oyo', 'Ekiti', 'Ondo'], 'tuition': '₦55,000', 'duration': '4 Years'},
            {'name': 'Lagos State University (LASU)', 'cutoff': 210, 'catchment': ['Lagos'], 'tuition': '₦150,000', 'duration': '4 Years'},
            {'name': 'FUTA', 'cutoff': 240, 'catchment': ['Ondo', 'Ekiti', 'Osun'], 'tuition': '₦45,000', 'duration': '5 Years'}
        ]
    },
    {
        'id': 'med',
        'title': 'Medicine & Surgery',
        'category': 'Health',
        'description': 'Diagnose, treat, and improve human health.',
        'req_subjects': ['bio', 'chem', 'phys'],
        'req_interests': ['care', 'sci', 'build'],
        'compulsory_subjects': ['bio', 'chem', 'phys'],
        'universities': [
            {'name': 'University of Ibadan (UI)', 'cutoff': 290, 'catchment': ['Oyo', 'Osun', 'Ogun'], 'tuition': '₦60,000', 'duration': '6 Years'},
            {'name': 'LASU College of Medicine', 'cutoff': 270, 'catchment': ['Lagos'], 'tuition': '₦250,000', 'duration': '6 Years'},
            {'name': 'Olabisi Onabanjo University (OOU)', 'cutoff': 250, 'catchment': ['Ogun'], 'tuition': '₦70,000', 'duration': '6 Years'}
        ]
    },
    {
        'id': 'law',
        'title': 'Law',
        'category': 'Humanities',
        'description': 'Interpret the constitution and defend justice.',
        'req_subjects': ['lit', 'govt', 'eng'],
        'req_interests': ['law', 'write', 'care'],
        'compulsory_subjects': ['lit', 'eng'],
        'universities': [
            {'name': 'UNILAG', 'cutoff': 270, 'catchment': ['Lagos', 'Ogun', 'Osun', 'Oyo'], 'tuition': '₦55,000', 'duration': '5 Years'},
            {'name': 'University of Benin (UNIBEN)', 'cutoff': 240, 'catchment': ['Edo', 'Delta'], 'tuition': '₦45,000', 'duration': '5 Years'}
        ]
    },
    {
        'id': 'acct',
        'title': 'Accounting',
        'category': 'Business',
        'description': 'Manage financial health of organizations.',
        'req_subjects': ['math', 'econ', 'eng'],
        'req_interests': ['money', 'law', 'build'],
        'compulsory_subjects': ['math', 'econ'],
        'universities': [
            {'name': 'UNILAG', 'cutoff': 250, 'catchment': ['Lagos', 'Ogun'], 'tuition': '₦55,000', 'duration': '4 Years'},
            {'name': 'Covenant University', 'cutoff': 200, 'catchment': [], 'tuition': '₦900,000', 'duration': '4 Years'}
        ]
    }
]

# --- ROUTES ---

@app.route('/')
def home():
    """Serve the Frontend HTML when users visit the site root"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """SRE Health Check Endpoint"""
    return jsonify({"status": "healthy", "mode": "production"})

@app.route('/recommend', methods=['POST'])
def recommend():
    # Simulate processing time to show off Skeleton Loader
    time.sleep(1) 
    
    data = request.json
    print(f"📥 Received Data: {data}")

    user_grades = data.get('grades', {})
    user_interests = data.get('interests', [])
    user_jamb = data.get('jamb', 0)
    user_state = data.get('state', '')
    
    results = []

    for course in COURSES:
        # 1. Strict Subject Validation
        # If student fails a compulsory subject, they are disqualified immediately.
        qualified = True
        for sub in course.get('compulsory_subjects', []):
            if user_grades.get(sub, 0) < 3: # Less than Credit (C)
                qualified = False
                break
        
        if not qualified:
            continue

        # 2. University Filtering & Catchment Logic
        eligible_universities = []
        for uni in course.get('universities', []):
            effective_cutoff = uni['cutoff']
            
            # Apply Catchment Bonus (Lower cutoff by 20 points)
            if user_state in uni.get('catchment', []):
                effective_cutoff -= 20
            
            # Check if user meets the (possibly lowered) cutoff
            if user_jamb >= effective_cutoff:
                eligible_universities.append(uni)

        # If no university accepts them for this course, skip the course
        if not eligible_universities:
            continue

        # 3. Calculate Match Score
        score = 0
        for sub in course['req_subjects']:
            g = user_grades.get(sub, 0)
            if g >= 4: score += 20    # A/B
            elif g == 3: score += 15  # C
            elif g == 2: score += 5   # D
        
        for interest in course['req_interests']:
            if interest in user_interests: score += 15
                
        # Only show good matches (Score > 20)
        if score >= 20:
            results.append({
                **course, 
                "score": score, 
                "universities": eligible_universities
            })
    
    # Sort results by highest match score
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(results)

if __name__ == '__main__':
    # This is only for local testing. In production, Docker uses Gunicorn.
    app.run(debug=True, port=5000)