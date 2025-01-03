import re
import sys
import json
import spacy
from pdfminer.high_level import extract_text
from datetime import datetime
from textblob import TextBlob

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
def extract_text_from_pdf(file_path):
    return extract_text(file_path)

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
        
        
    }
    
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


# Test the parser
if __name__ == "__main__":
    # file_path = "C:\\Users\\91765\\OneDrive\\Desktop\\NLP\\My_Resume1.pdf"  # Replace with the path to your resume file
    # file_path="C:\\Users\\91765\\OneDrive\\Desktop\\NLP\\22112009_Software Resume_2024-07-21_16_08_53.pdf"
    file_path = sys.argv[1]
    resume_data = parse_resume(file_path)
    print(resume_data)
    # # print(json.dumps(resume_data))    ## added
    # text = extract_text_from_pdf(file_path)
    # a=extract_experience(text)
    
    # sentiment_scores = analyze_experience_sentiment(a)
    # for key, sentiment in sentiment_scores.items():
    #     print(f"{key}:")
    #     print(f"  Text: {sentiment['Text']}")
    #     print(f"  Polarity: {sentiment['Polarity']}")
    #     print(f"  Subjectivity: {sentiment['Subjectivity']}")
        
    # # print("Achievements", extract_achievements(text))
    # # print("Highlighted Achievements", highlight_achievements(text))
    # print("Projects", extract_projects(text))
    