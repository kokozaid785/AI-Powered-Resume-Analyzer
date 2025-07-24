# AI-Powered Resume Analyzer

## Overview
This project is an **AI-powered resume analysis tool** designed to:
- Extract text from resumes (PDF format)
- Analyze skills using NLP (Natural Language Processing)
- Generate a skill report for quick evaluation

## Features
- **Resume Parsing:** Extracts candidate information and skills from uploaded PDF resumes.
- **NLP Skill Matching:** Uses custom rules and NLP models to detect skills.
- **Skill Report:** Generates a summary PDF of detected skills.

## Project Structure
AI-Powered Resume Analyzer/
│── app.py # Main application entry point
│── requirements.txt # Python dependencies
│── Sample PDF # Example resume for testing
│── resume_skill_report.pdf # Example skill analysis output
│── utils/
│ ├── init.py # Utility module initializer
│ ├── nlp_matcher.py # NLP-based skill matching
│ └── parser.py # Resume parsing functions


## Installation & Usage
1. Clone the repository:
   git clone <repo_url>
   cd AI-Powered-Resume-Analyzer
Install dependencies:

pip install -r requirements.txt
Run the application:

python app.py
Upload a resume (PDF) and view the generated skill analysis report.

Requirements
Python 3.8+

Libraries listed in requirements.txt

Sample Output
Sample PDF – input resume

resume_skill_report.pdf – generated skill summary

License
This project is open source and available under the MIT License.