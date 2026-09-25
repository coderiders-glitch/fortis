from sqlalchemy.orm import Session

from app.models.doctor import Doctor

SEED_DOCTORS: list[dict[str, str | int]] = [
    {"name": "Dr. Sarah Johnson", "speciality": "Cardiologist", "details": "Board-certified cardiologist specializing in heart disease prevention and cardiovascular care.", "symptoms": "chest pain, shortness of breath, heart palpitations", "experience": 15, "location": "123 Heart Center, Medical District"},
    {"name": "Dr. Michael Chen", "speciality": "Pediatrician", "details": "Provides preventive and ongoing medical care for infants, children, and adolescents.", "symptoms": "fever, cough, childhood illness, allergies", "experience": 12, "location": "45 Children's Health Plaza"},
    {"name": "Dr. Aisha Patel", "speciality": "Dermatologist", "details": "Treats medical and chronic skin conditions and provides comprehensive skin health care.", "symptoms": "rash, acne, eczema, skin irritation", "experience": 10, "location": "210 Oak Street, Suite 4"},
    {"name": "Dr. James Wilson", "speciality": "Neurologist", "details": "Experienced neurologist focused on evaluating and treating disorders of the nervous system.", "symptoms": "headache, migraine, numbness, dizziness", "experience": 18, "location": "88 North Medical Tower"},
    {"name": "Dr. Maria Garcia", "speciality": "Family Medicine", "details": "Offers primary care and preventive health services for patients at every stage of life.", "symptoms": "fatigue, fever, cold, general checkup", "experience": 14, "location": "16 Greenway Family Clinic"},
    {"name": "Dr. Robert Thompson", "speciality": "Orthopedic Surgeon", "details": "Specializes in musculoskeletal conditions, joint care, and sports-related injuries.", "symptoms": "joint pain, back pain, fracture, sprain", "experience": 20, "location": "300 OrthoCare Avenue"},
    {"name": "Dr. Emily Davis", "speciality": "Endocrinologist", "details": "Manages hormone and metabolic disorders with individualized, evidence-based care.", "symptoms": "diabetes, thyroid problems, weight changes, thirst", "experience": 11, "location": "72 Wellness Boulevard"},
    {"name": "Dr. Daniel Kim", "speciality": "Gastroenterologist", "details": "Provides evaluation and treatment for digestive tract and liver conditions.", "symptoms": "abdominal pain, heartburn, nausea, indigestion", "experience": 16, "location": "501 Digestive Health Center"},
    {"name": "Dr. Olivia Brown", "speciality": "Ophthalmologist", "details": "Provides medical eye care and diagnosis of common and complex vision conditions.", "symptoms": "blurred vision, eye pain, dry eyes, redness", "experience": 13, "location": "9 Vision Care Road"},
    {"name": "Dr. William Anderson", "speciality": "Pulmonologist", "details": "Specializes in respiratory health and chronic and acute lung conditions.", "symptoms": "shortness of breath, wheezing, persistent cough, asthma", "experience": 17, "location": "140 Respiratory Center"},
    {"name": "Dr. Sophia Martinez", "speciality": "Obstetrician and Gynecologist", "details": "Offers routine gynecologic care and support through pregnancy and reproductive health.", "symptoms": "pelvic pain, irregular periods, pregnancy care", "experience": 12, "location": "27 Women's Health Lane"},
    {"name": "Dr. Ethan Miller", "speciality": "Psychiatrist", "details": "Provides assessment and treatment for a range of mental health conditions.", "symptoms": "anxiety, depression, insomnia, mood changes", "experience": 9, "location": "64 Mindful Care Street"},
    {"name": "Dr. Grace Lee", "speciality": "Otolaryngologist", "details": "Treats ear, nose, and throat conditions for adults and children.", "symptoms": "earache, sinus pressure, sore throat, hearing loss", "experience": 14, "location": "112 ENT Medical Center"},
    {"name": "Dr. David Robinson", "speciality": "Oncologist", "details": "Coordinates personalized cancer evaluation and medical oncology care.", "symptoms": "cancer care, unexplained weight loss, persistent fatigue", "experience": 19, "location": "400 Hope Oncology Institute"},
    {"name": "Dr. Isabella Clark", "speciality": "Rheumatologist", "details": "Focuses on inflammatory and autoimmune conditions affecting joints and connective tissue.", "symptoms": "joint stiffness, swelling, arthritis, muscle pain", "experience": 8, "location": "35 Arthritis and Joint Clinic"},
    {"name": "Dr. Noah Lewis", "speciality": "Urologist", "details": "Provides care for urinary tract and men's reproductive health conditions.", "symptoms": "urinary difficulty, kidney stones, pelvic discomfort", "experience": 10, "location": "705 Urology Health Center"},
]


def seed_doctors(db: Session) -> int:
    if db.query(Doctor).count() == 0:
        db.add_all([Doctor(**record) for record in SEED_DOCTORS])
        db.commit()
        return len(SEED_DOCTORS)
    return 0
