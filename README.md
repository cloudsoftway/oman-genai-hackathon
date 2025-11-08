# AI-Powered HR Recruitment System

An intelligent multi-agent system built with CrewAI that automates CV screening, analysis, and job matching for recruitment workflows.

---

## 📋 Overview

This system uses three specialized AI agents to process candidate CVs and match them against job descriptions:

1. **CV Reader Agent** - Extracts text from PDF resumes
2. **CV Analyzer Agent** - Analyzes and structures CV data with intelligent assessments
3. **Job Matcher Agent** - Matches candidates to job requirements and scores fit

---

## 🏗️ Project Structure

```
.
├── app/
│   ├── config/
│   │   ├── agents.yaml          # Agent configurations
│   │   └── tasks.yaml            # Task definitions
│   ├── tools/
│   │   ├── pdf_reader.py         # PDF extraction tool
│   │   └── __init__.py
│   ├── crew.py                   # CrewAI setup and agents
│   ├── main.py                   # Entry point
│   ├── model.py                  # Pydantic schemas
│   └── __init__.py
├── knowledge/                    # Job description JSONs (knowledge base)
├── CV/                          # Input: PDF resumes
├── preprocessed-CVs/            # Output: Extracted text files
├── processed-CVs/               # Output: Analyzed CV JSONs
├── job-matches-results/         # Output: Match result JSONs
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- OpenAI API key or Gemini API key
- Serper API key (for web search)

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <project-directory>

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Choose your model (Gemini or OpenAI)
MODEL=gemini/gemini-2.0-flash-exp
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here

# OR use OpenAI
MODEL=openai/gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Prepare Your Data

```bash
# Add candidate CVs (PDF format)
# Place PDF files in: CV/

# Add job descriptions (JSON format)
# Place job JSONs in: knowledge/
```

**Example Job Description JSON:**
```json
{
  "job_title": "Junior Machine Learning Engineer",
  "required_skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning"],
  "required_experience_years": 1,
  "education_level": "bachelor",
  "career_level": "entry"
}
```

### 5. Run the System

```bash
python -m app.main
```

---

## 🤖 How It Works

### Agent 1: CV Reader
- **Input**: PDF files from `CV/` folder
- **Process**: Extracts text content from PDFs
- **Output**: Text files saved to `preprocessed-CVs/`
- **Tools**: DirectoryReadTool, PDFReaderTool

### Agent 2: CV Analyzer
- **Input**: Text files from `preprocessed-CVs/`
- **Process**: 
  - Extracts structured data (contact, education, experience, skills)
  - Infers missing information (skill levels, categories)
  - Calculates career metrics
  - Generates intelligent assessment (strengths, weaknesses, recommendations)
- **Output**: Structured JSON files in `processed-CVs/`
- **Schema**: `CandidateCV` (see `model.py`)
- **Tools**: DirectoryReadTool, FileReadTool, FileWriterTool

### Agent 3: Job Matcher
- **Input**: 
  - Candidate JSONs from `processed-CVs/`
  - Job descriptions from `knowledge/` (knowledge base)
- **Process**:
  - Compares candidate skills vs. job requirements
  - Scores match across 4 dimensions:
    - Skills Match (40 points)
    - Experience Match (30 points)
    - Education Match (20 points)
    - Career Level Fit (10 points)
  - Generates match report with recommendations
- **Output**: Match result JSONs in `job-matches-results/`
- **Schema**: `JobMatchResult` (see `model.py`)
- **Tools**: DirectoryReadTool, FileReadTool, FileWriterTool

---

## 📊 Output Examples

### Processed CV (processed-CVs/*.json)
```json
{
  "contact_information": {
    "full_name": "John Doe",
    "email": "john@example.com",
    "location": "New York, USA"
  },
  "skills": [
    {
      "name": "Python",
      "category": "Programming Languages",
      "level": "advanced"
    }
  ],
  "agent_assessment": {
    "overall_rating": "strong",
    "rating_score": 85,
    "strengths": ["Strong ML project portfolio", "Modern tech stack"],
    "suitable_roles": ["ML Engineer", "Data Scientist"]
  }
}
```

### Match Result (job-matches-results/*.json)
```json
{
  "candidate_name": "John Doe",
  "job_title": "Junior ML Engineer",
  "overall_score": 82,
  "breakdown": {
    "skills_score": 35,
    "experience_score": 25,
    "education_score": 15,
    "career_level_score": 7
  },
  "match_category": "strong_match",
  "recommendation": "Strong technical fit. Recommend technical interview."
}
```

---

## 🔧 Configuration Files

### agents.yaml
Defines agent roles, goals, and backstories for:
- `cv_reader` - PDF text extraction specialist
- `cv_analyzer` - CV intelligence analyst
- `job_matcher` - Job matching specialist

### tasks.yaml
Defines task descriptions, expected outputs, and tool usage for:
- `cv_reader_task` - PDF → TXT conversion
- `cv_analyzer_task` - TXT → Structured JSON with assessment
- `job_matching_task` - CV + Job → Match score and recommendation

### model.py
Contains Pydantic schemas:
- `CandidateCV` - Complete CV structure with 15+ fields including agent assessment
- `JobMatchResult` - Match scoring with breakdown and recommendations
- Enums: `EducationLevel`, `EmploymentType`, `SkillLevel`

---

## 📝 Requirements

Key dependencies (see `requirements.txt` for full list):
- `crewai>=0.86.0` - Multi-agent orchestration
- `crewai-tools` - File and directory tools
- `pydantic>=2.0.0` - Data validation
- `python-dotenv` - Environment management
- `PyPDF2` - PDF text extraction

---

## 🎯 Workflow Diagram

```
┌─────────────┐
│   PDF CVs   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  CV Reader      │  Agent 1
│  PDF → TXT      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  CV Analyzer    │  Agent 2
│  TXT → JSON +   │
│  Assessment     │
└──────┬──────────┘
       │
       ▼
  [CV Database]
       │
       │  ┌──────────────┐
       │  │ Job Desc.    │
       │  │ (knowledge/) │
       │  └──────┬───────┘
       │         │
       └─────────┴────────┐
                          ▼
               ┌─────────────────┐
               │  Job Matcher    │  Agent 3
               │  CV + Job →     │
               │  Match Score    │
               └──────┬──────────┘
                      │
                      ▼
               ┌─────────────────┐
               │ Match Results   │
               │ (80+ = Strong)  │
               │ (60-79 = Mod)   │
               │ (<60 = Weak)    │
               └─────────────────┘
```

---


## 📚 API Key Setup

### Gemini API (Recommended for cost)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`

### OpenAI API (Recommended for quality)
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

### Serper API (For web search)
1. Visit [Serper.dev](https://serper.dev/)
2. Create free account (2,500 free searches)
3. Add to `.env`: `SERPER_API_KEY=your_key_here`

---

## 🎯 Project Roadmap

### ✅ Completed
- [x] PDF to text extraction
- [x] Intelligent CV analysis with assessments
- [x] Job matching with scoring
- [x] Structured data validation with Pydantic
- [x] Multi-agent orchestration with CrewAI

### 🚧 In Progress
- [ ] **Email Communication Agent** - Send automated emails to:
  - ✉️ Accepted candidates (interview invitations)
  - ✉️ Rejected candidates (kind rejection with feedback)
- [ ] **Improvement Plan Generator Agent** - Create personalized development plans for:
  - 📋 Waiting list candidates (skill gaps + learning resources)

### 🔮 Planned
- [ ] Candidate classification (Accepted/Potential/Rejected)
- [ ] Interview scheduler integration
- [ ] Create personalized development plans for waiting list.