import re
import spacy
from pdfminer.high_level import extract_text
from datetime import datetime
from textblob import TextBlob
import pdfplumber
import pyttsx3
engine = pyttsx3.init()
import json
import sys

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (default is 200)
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
# def extract_text_from_pdf(file_path):
#     return extract_text(file_path)
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text


# Extract email addresses
def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

# Extract phone numbers
def extract_phone(text):
    phone_pattern = r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    return re.findall(phone_pattern, text)

# Extract skills
def extract_skills(text):
    predefined_skills = ["Python", "Java", "Machine Learning", "NLP", "Data Analysis", "SQL", "C++", "JavaScript"]
    found_skills = [skill for skill in predefined_skills if skill.lower() in text.lower()]
    return found_skills

# Extract education details
def extract_education(text):
    education_keywords = ["Bachelor", "Master", "B.Tech", "M.Tech", "PhD", "B.Sc", "M.Sc", "BE", "ME","University","School"]
    sentences = text.split("\n")
    education_details = [sentence for sentence in sentences if any(keyword in sentence for keyword in education_keywords)]
    return education_details

# Extract work experience
def extract_experience(text):
    experience_keywords = ["experience", "intern", "worked", "job", "role"]
    sentences = text.split("\n")
    experience_details = [sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in experience_keywords)]
    return experience_details

# Extract names (basic implementation)
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

# Extract linked profiles (e.g., LinkedIn, GitHub)
def extract_links(text):
    link_pattern = r'(https?://[\w./-]+)'
    return re.findall(link_pattern, text)

# Extract certifications
def extract_certifications(text):
    certification_keywords = ["certified", "certification", "certificate", "course"]
    sentences = text.split("\n")
    certifications = [sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in certification_keywords)]
    return certifications

# Extract languages
def extract_languages(text):
    predefined_languages = ["English", "Hindi", "Spanish", "French", "German", "Mandarin"]
    found_languages = [language for language in predefined_languages if language.lower() in text.lower()]
    return found_languages

# Extract availability or joining date
def extract_availability(text):
    date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
    dates = re.findall(date_pattern, text)
    parsed_dates = []
    for date in dates:
        try:
            parsed_dates.append(datetime.strptime(date, "%d-%m-%Y"))
        except ValueError:
            try:
                parsed_dates.append(datetime.strptime(date, "%d/%m/%Y"))
            except ValueError:
                continue
    return parsed_dates
def analyze_experience_sentiment(experience_details):
    sentiment_scores = {}
    for i, detail in enumerate(experience_details):
        sentiment = TextBlob(detail).sentiment
        sentiment_scores[f"Experience {i+1}"] = {
            "Text": detail,
            "Polarity": sentiment.polarity,
            "Subjectivity": sentiment.subjectivity #Subjectivity quantifies the amount of personal opinion and factual information contained in the text.
        }
    return sentiment_scores
# Extract achievements
def extract_achievements(text):
    achievement_keywords = ["award", "promotion", "recognized", "achieved", "honored", "distinction", "outstanding", "exceptional"]
    sentences = text.split("\n")
    achievements = [sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in achievement_keywords)]
    return achievements

# Highlight achievements
def highlight_achievements(text):
    achievements = extract_achievements(text)
    highlighted_text = text
    for achievement in achievements:
        highlighted_text = highlighted_text.replace(achievement, f"**{achievement}**")
    return highlighted_text
def score_resume(parsed_data):
    score = 0
    if parsed_data.get("Name"):
        score += 10
    if parsed_data.get("Email"):
        score += 10
    if parsed_data.get("Phone"):
        score += 10
    if parsed_data.get("Skills"):
        score += len(parsed_data["Skills"]) * 5
    if parsed_data.get("Education"):
        score += len(parsed_data["Education"]) * 5
    if parsed_data.get("Experience"):
        score += len(parsed_data["Experience"]) * 10
    if parsed_data.get("Certifications"):
        score += len(parsed_data["Certifications"]) * 5
    if parsed_data.get("Achievements"):
        score += len(parsed_data["Achievements"]) * 5
    if parsed_data.get("Languages"):
        score += len(parsed_data["Languages"]) * 2
    return score
def match_job_role(parsed_data):
    # Predefined job roles and their requirements
    job_roles = {
        "Data Scientist": {
            "skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "NLP"],
            "experience_keywords": ["data", "analysis", "machine learning", "modeling"],
            "education_keywords": ["Bachelor", "Master", "PhD"]
        },
        "Software Developer": {
            "skills": ["Python", "Java", "C++", "JavaScript", "SQL"],
            "experience_keywords": ["development", "programming", "software", "coding"],
            "education_keywords": ["Bachelor", "Master", "B.Tech", "M.Tech"]
        },
        "AI Engineer": {
            "skills": ["Python", "Machine Learning", "Deep Learning", "NLP", "TensorFlow"],
            "experience_keywords": ["AI", "machine learning", "deep learning", "neural networks"],
            "education_keywords": ["Bachelor", "Master", "PhD"]
        },
        "Project Manager": {
            "skills": ["Management", "Leadership", "Communication", "Planning"],
            "experience_keywords": ["management", "project", "leadership", "planning"],
            "education_keywords": ["MBA", "Master", "Bachelor"]
        }
    }

    # Calculate match scores for each role
    role_scores = {}
    for role, criteria in job_roles.items():
        score = 0

        # Match skills
        candidate_skills = set(parsed_data.get("Skills", []))
        role_skills = set(criteria["skills"])
        skill_match = len(candidate_skills & role_skills) / len(role_skills) * 100
        score += skill_match * 0.5  # Skills contribute 50% to the score

        # Match experience
        candidate_experience = " ".join(parsed_data.get("Experience", [])).lower()
        experience_match = sum(1 for keyword in criteria["experience_keywords"] if keyword in candidate_experience)
        score += (experience_match / len(criteria["experience_keywords"])) * 30  # Experience contributes 30%

        # Match education
        candidate_education = " ".join(parsed_data.get("Education", [])).lower()
        education_match = sum(1 for keyword in criteria["education_keywords"] if keyword.lower() in candidate_education)
        score += (education_match / len(criteria["education_keywords"])) * 20  # Education contributes 20%

        # Store the score
        role_scores[role] = score

    # Find the best matching role
    best_role = max(role_scores, key=role_scores.get)
    return best_role, role_scores[best_role], role_scores

# Main parser function
def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    
    parsed_data = {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "Education": extract_education(text),
        # "Experience": extract_experience(text),
        "Links": extract_links(text),
        "Certifications": extract_certifications(text),
        "Languages": extract_languages(text),
        "Availability": extract_availability(text)
        # "Sentiment_score": analyze_experience_sentiment():
        # Score the resume
    }
    parsed_data["Score"] = score_resume(parsed_data)
    # Match job role
    best_role, best_score, all_scores = match_job_role(parsed_data)
    parsed_data["Best Role"] = best_role
    parsed_data["Role Match Score"] = best_score
    parsed_data["All Role Scores"] = all_scores
    
    return parsed_data
        
        
    
    
    return parsed_data
# Extract projects with highlighted description
def extract_projects(text):
    project_keywords = ["project", "developed", "built", "created", "designed", "implemented"]
    sentences = text.split("\n")
    projects = [sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in project_keywords)]
    highlighted_projects = {}
    for project in projects:
        highlighted_projects[project] = f"**{project}**"
    return highlighted_projects

# Suggest improvements based on parsed data
def suggest_improvements(parsed_data):
    suggestions = []

    if not parsed_data.get("Name"):
        suggestions.append("Include your name in the resume.")
    if not parsed_data.get("Email"):
        suggestions.append("Add a professional email address.")
    if not parsed_data.get("Phone"):
        suggestions.append("Provide a contact number.")
    if not parsed_data.get("Skills"):
        suggestions.append("List relevant skills that match the job description.")
    if not parsed_data.get("Education"):
        suggestions.append("Mention your educational qualifications.")
    if not parsed_data.get("Experience"):
        suggestions.append("Detail your work experience or internships.")
    if not parsed_data.get("Certifications"):
        suggestions.append("Include any certifications or courses you've completed.")
    if not parsed_data.get("Achievements"):
        suggestions.append("Highlight any awards or achievements.")
    if not parsed_data.get("Languages"):
        suggestions.append("Mention the languages you are proficient in.")

    return suggestions




# # Test the parser
# if __name__ == "__main__":
#     # file_path = "C:\\Users\\91765\\OneDrive\\Desktop\\NLP\\My_Resume1.pdf"  # Replace with the path to your resume file
#     # file_path="C:\\Users\\91765\\OneDrive\\Desktop\\NLP\\22112009_Software Resume_2024-07-21_16_08_53.pdf"
#     file_path="C:\\Users\\91765\\OneDrive\\Desktop\\NLP\\resume1.pdf"
#     # file_path="C:\\Users\\91765\\OneDrive\\Desktop\\NLP\\Resume2_removed.pdf"
    

# # Wait until the speech is finished
#     resume_data = parse_resume(file_path)
#     print(resume_data)
#     # engine.say(resume_data)
#     # engine.runAndWait()
#     text = extract_text_from_pdf(file_path)
#     a=extract_experience(text)
    
#     sentiment_scores = analyze_experience_sentiment(a)
#     for key, sentiment in sentiment_scores.items():
#         print(f"{key}:")
#         print(f"  Text: {sentiment['Text']}")
#         print(f"  Polarity: {sentiment['Polarity']}")
#         print(f"  Subjectivity: {sentiment['Subjectivity']}")
        
#     print("Achievements", extract_achievements(text))
#     # print("Highlighted Achievements", highlight_achievements(text))
#     print("Projects", extract_projects(text))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file path provided"}))
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        resume_data = parse_resume(file_path)
        print(json.dumps(resume_data))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


# # Get suggestions for improvement
# improvement_suggestions = suggest_improvements(resume_data)

# # Display the suggestions
# print("Suggestions for Improvement:")
# for suggestion in improvement_suggestions:
#     print(f"- {suggestion}")
# #JSON OUTPUT
# resume_data_json1 = json.dumps(resume_data, indent=4)
# print(resume_data_json1)

# resume_data_json2 = json.dumps(sentiment_scores, indent=4)
# print(resume_data_json2)

# #suggestion output
# resume_data_json4 = json.dumps(improvement_suggestions, indent=4)
# print(resume_data_json4)