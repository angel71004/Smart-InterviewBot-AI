# 💼 AI-Powered Interview Question Generator with Resume Analysis

An intelligent system that analyzes resumes, extracts skills, matches them with job requirements, and generates personalized interview questions using NLP and machine learning.

## 🎯 Project Overview

This application helps job seekers prepare for interviews by:
1. **Uploading Resumes**: Supports PDF and DOCX formats
2. **Skill Extraction**: Automatically identifies technical and soft skills using NLP
3. **Job Role Matching**: Matches resume skills with job role requirements
4. **Question Generation**: Generates personalized interview questions based on:
   - Extracted resume skills
   - Selected job role
   - Question relevance ranking using TF-IDF
5. **Analysis & Insights**: Provides match scores, missing skills, and recommendations

## 🚀 Features

### Core Features
- ✅ Resume text extraction from PDF/DOCX files
- ✅ Automatic skill detection using keyword matching and NLP
- ✅ Job role selection from predefined roles
- ✅ Skill matching and match score calculation
- ✅ Personalized interview question generation
- ✅ Question categorization (Technical, Behavioral, Scenario-based)
- ✅ Difficulty level assignment (Easy, Medium, Hard)
- ✅ Question ranking by relevance to resume
- ✅ CSV export functionality

### Advanced Features
- 📊 Resume match score percentage
- ⚠️ Missing skills identification
- 💡 Recommendations based on match score
- 📈 Statistics and insights dashboard
- 🎨 Beautiful, modern UI with Streamlit

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit**: Web application framework
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **spaCy**: Natural language processing
- **scikit-learn**: Machine learning (TF-IDF, cosine similarity)
- **pandas**: Data manipulation
- **numpy**: Numerical computing

## 📁 Project Structure

```
AI_Interview_Question_Generator/
│
├── app.py                          # Main Streamlit application
├── utils.py                        # Utility functions
├── requirements.txt                # Python dependencies
├── job_roles.csv                   # Job roles and required skills
├── interview_questions.csv         # Interview questions database
├── README.md                       # Project documentation
│
├── datasets/                       # Dataset files
│   ├── resume_dataset.csv
│   ├── hr_questions.csv
│   ├── software_engineering_questions.csv
│   ├── coding_questions.csv
│   └── resume_and_jobdescription.csv
│
└── sample_resumes/                 # Sample resume files (optional)
    ├── resume1.pdf
    └── resume2.docx
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd AI_Interview_Question_Generator
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

## 🎮 How to Run

1. **Activate virtual environment** (if using one)
2. **Run the Streamlit app**:
```bash
streamlit run app.py
```

3. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## 📖 Usage Guide

### Step 1: Upload Resume
1. Go to the **"📄 Resume Upload"** tab
2. Click "Choose a resume file" and select a PDF or DOCX file
3. Wait for the system to extract text and skills
4. Review the extracted skills displayed

### Step 2: Select Job Role
1. Go to the **"🔍 Analysis & Questions"** tab
2. Select a job role from the dropdown menu
3. View the skill matching analysis:
   - Match score percentage
   - Matched skills (highlighted in green)
   - Missing skills (highlighted in red)

### Step 3: Review Questions
1. Scroll down to see personalized interview questions
2. Questions are categorized into:
   - **Technical Questions**: Skills and knowledge-based
   - **Behavioral Questions**: Experience and situation-based
   - **Scenario-based Questions**: Problem-solving and decision-making
3. Each question shows a difficulty level (Easy/Medium/Hard)

### Step 4: Download Questions
1. Click the **"📥 Download Questions as CSV"** button
2. Save the CSV file with all generated questions
3. Use it for interview preparation

### Step 5: View Statistics
1. Go to the **"📊 Statistics"** tab
2. View resume statistics and match insights
3. Get recommendations based on your match score

## 🔧 Configuration

### Adding New Job Roles
Edit `job_roles.csv` and add new rows:
```csv
Job_Role,Key_Skills
New Role,Skill1,Skill2,Skill3
```

### Adding New Questions
Edit `interview_questions.csv` and add new rows:
```csv
Job_Role,Question_Type,Question,Difficulty
Software Engineer,Technical,Your question here?,Medium
```

### Customizing Skills Vocabulary
Edit `utils.py` and modify the `TECH_SKILLS` list to add/remove skills.

## 🧠 How It Works

### 1. Resume Processing
- **Text Extraction**: Uses PyPDF2 for PDFs and python-docx for DOCX files
- **Skill Extraction**: 
  - Keyword matching against a predefined skills vocabulary
  - NLP-based extraction using spaCy for additional skill detection

### 2. Skill Matching
- Compares extracted resume skills with job role requirements
- Calculates match score: `(matched_skills / total_required_skills) * 100`
- Identifies missing skills for recommendations

### 3. Question Generation
- Filters questions by job role and question type
- Ranks questions by relevance using TF-IDF vectorization
- Calculates cosine similarity between resume text and questions
- Returns top N most relevant questions

### 4. Difficulty Assessment
- Uses heuristic-based difficulty calculation
- Analyzes question keywords and complexity
- Assigns Easy, Medium, or Hard labels

## 📊 Workflow Diagram

```
[Upload Resume] 
    ↓
[Extract Text] 
    ↓
[Extract Skills] 
    ↓
[Select Job Role] 
    ↓
[Match Skills] → [Calculate Match Score]
    ↓
[Generate Questions] → [Rank by Relevance]
    ↓
[Display Questions] → [Download CSV]
```

## 🧪 Testing

### Test with Sample Resumes
1. Create sample resumes with various skills (Python, Java, SQL, etc.)
2. Upload them and verify skill extraction
3. Test with different job roles
4. Verify question generation and ranking

### Expected Results
- ✅ Resume text is extracted correctly
- ✅ Skills are detected accurately
- ✅ Relevant questions appear under correct categories
- ✅ Download feature works
- ✅ Match score is calculated correctly

## 🐛 Troubleshooting

### Issue: spaCy model not found
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: PDF extraction fails
**Solution**: 
- Ensure the PDF is not password-protected
- Check if the PDF contains text (not just images)
- Try converting the PDF to DOCX first

### Issue: No skills detected
**Solution**:
- Ensure your resume contains technical keywords
- Check if skills are spelled correctly
- Add skills to the `TECH_SKILLS` list in `utils.py`

### Issue: Questions not showing
**Solution**:
- Verify `interview_questions.csv` exists and has data
- Check if the selected job role exists in the CSV
- Ensure question types match (Technical, Behavioral, Scenario-based)

## 🚀 Deployment

### Deploy on Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy the app

### Deploy on Render
1. Create a `render.yaml` file
2. Set up a web service
3. Configure build and start commands
4. Deploy the application

## 📝 Future Enhancements

- [ ] Support for more file formats (TXT, RTF)
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] AI-powered question generation using GPT models
- [ ] Multi-language support
- [ ] Resume improvement suggestions
- [ ] Interview preparation timeline
- [ ] Practice mode with answers
- [ ] Export to PDF format
- [ ] Integration with calendar for interview scheduling

## 📄 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- spaCy for NLP capabilities
- scikit-learn for ML utilities
- All contributors and testers

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Python and Streamlit**

Happy Interview Preparation! 🎯


http://localhost:8503/
