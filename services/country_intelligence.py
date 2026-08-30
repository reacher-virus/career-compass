from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SUPPORTED_COUNTRIES = [
    "India",
    "Germany",
    "USA",
    "Canada",
    "Australia",
    "United Kingdom",
    "Singapore",
    "UAE",
    "Japan",
    "France",
    "Netherlands",
    "Sweden",
    "Switzerland",
    "New Zealand",
    "South Korea",
    "Italy",
    "Spain",
    "Belgium",
    "Norway",
    "Denmark",
    "Finland",
    "Ireland",
    "Austria",
    "Portugal",
    "Poland",
]


CAREER_CATEGORY_KEYWORDS = {
    "AI": ["ai", "machine learning", "ml engineer", "deep learning", "llm"],
    "Data": ["data", "analyst", "scientist", "analytics"],
    "Cybersecurity": ["cyber", "security"],
    "Cloud": ["cloud", "devops", "sre"],
    "Software": ["developer", "software", "backend", "frontend", "full stack", "mobile"],
    "Product": ["product manager", "ai product"],
    "Design": ["ux", "designer"],
    "Finance": ["finance", "accounting", "banking", "investment", "valuation"],
    "Marketing": ["marketing", "seo", "content", "brand", "ads", "campaign"],
    "Law": ["law", "lawyer", "legal", "compliance", "contract"],
    "Healthcare": ["health", "medical", "nursing", "pharmacy", "clinical", "public health"],
    "Education": ["teacher", "teaching", "education", "curriculum"],
    "Engineering": ["mechanical", "civil", "electrical", "electronics", "architecture", "agriculture"],
    "Government": ["government", "civil services", "policy", "public administration"],
}


COUNTRY_MARKET_DATA = {
    "India": {
        "currency": "INR",
        "salary_suffix": "LPA",
        "visa_difficulty": "Low",
        "market_growth": "Very High",
        "remote_jobs": "High",
        "top_hiring_companies": ["TCS", "Infosys", "Wipro", "Accenture", "Fractal", "Razorpay"],
        "interview_process": ["Online assessment", "Technical interview", "Managerial round", "HR round"],
        "future_demand": "Very high over the next 5-10 years as AI, cloud, and digital transformation hiring expands.",
        "certifications": ["AWS Cloud Practitioner", "Google Data Analytics", "Microsoft Azure Fundamentals", "NPTEL / IIT role courses"],
        "programming_languages": ["Python", "Java", "SQL", "JavaScript"],
        "frameworks": ["FastAPI", "React", "Spring Boot", "TensorFlow"],
        "country_skills": ["Cloud Deployment", "DSA", "System Design"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "6-10", "mid": "14-25", "senior": "30-55"},
            "Data": {"demand": "High", "entry": "5-9", "mid": "12-22", "senior": "25-45"},
            "Cybersecurity": {"demand": "High", "entry": "5-8", "mid": "12-22", "senior": "25-42"},
            "Cloud": {"demand": "Very High", "entry": "6-10", "mid": "15-28", "senior": "32-60"},
            "Software": {"demand": "High", "entry": "4-8", "mid": "12-24", "senior": "28-55"},
            "Product": {"demand": "High", "entry": "8-14", "mid": "20-35", "senior": "45-80"},
            "Design": {"demand": "Medium", "entry": "4-7", "mid": "10-18", "senior": "22-38"},
        },
    },
    "Germany": {
        "currency": "EUR",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "Medium",
        "top_hiring_companies": ["SAP", "Siemens", "Bosch", "BMW", "Zalando", "Celonis"],
        "interview_process": ["Recruiter screen", "Technical interview", "Practical task", "Team fit interview"],
        "future_demand": "High future demand, especially for AI, cloud, cybersecurity, and industrial software roles.",
        "certifications": ["AWS Solutions Architect", "Azure AI Engineer", "Google Professional ML Engineer", "German B1"],
        "programming_languages": ["Python", "Java", "SQL", "TypeScript"],
        "frameworks": ["FastAPI", "Spring Boot", "React", "Docker"],
        "country_skills": ["German B1", "EU Work Culture", "Cloud Basics"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "55-65", "mid": "70-90", "senior": "95-125"},
            "Data": {"demand": "High", "entry": "50-62", "mid": "65-85", "senior": "90-115"},
            "Cybersecurity": {"demand": "Very High", "entry": "52-65", "mid": "70-92", "senior": "95-130"},
            "Cloud": {"demand": "Very High", "entry": "55-68", "mid": "75-95", "senior": "100-135"},
            "Software": {"demand": "High", "entry": "50-62", "mid": "68-88", "senior": "90-120"},
            "Product": {"demand": "Medium", "entry": "55-70", "mid": "78-100", "senior": "105-140"},
            "Design": {"demand": "Medium", "entry": "42-55", "mid": "58-75", "senior": "78-100"},
        },
    },
    "USA": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "High",
        "market_growth": "Very High",
        "remote_jobs": "Very High",
        "top_hiring_companies": ["Google", "Microsoft", "Amazon", "Meta", "NVIDIA", "OpenAI"],
        "interview_process": ["Recruiter screen", "Coding / technical rounds", "System design", "Behavioral interview"],
        "future_demand": "Very high future demand for AI, platform engineering, cybersecurity, data, and cloud roles.",
        "certifications": ["AWS Solutions Architect", "Google Professional ML Engineer", "CKA", "Security+"],
        "programming_languages": ["Python", "Java", "Go", "TypeScript"],
        "frameworks": ["React", "FastAPI", "Kubernetes", "TensorFlow"],
        "country_skills": ["Cloud Scale", "System Design", "Interview Readiness"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "105-140", "mid": "150-210", "senior": "220-320"},
            "Data": {"demand": "High", "entry": "85-115", "mid": "120-165", "senior": "175-240"},
            "Cybersecurity": {"demand": "Very High", "entry": "90-120", "mid": "125-175", "senior": "185-260"},
            "Cloud": {"demand": "Very High", "entry": "95-130", "mid": "135-190", "senior": "200-285"},
            "Software": {"demand": "High", "entry": "90-125", "mid": "130-185", "senior": "190-280"},
            "Product": {"demand": "High", "entry": "105-140", "mid": "150-210", "senior": "220-330"},
            "Design": {"demand": "Medium", "entry": "75-105", "mid": "110-150", "senior": "155-220"},
        },
    },
    "Canada": {
        "currency": "CAD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "High",
        "top_hiring_companies": ["Shopify", "RBC", "TD", "Microsoft Canada", "Amazon Canada", "Cohere"],
        "interview_process": ["Recruiter screen", "Technical round", "Project discussion", "Behavioral interview"],
        "future_demand": "High future demand in AI, fintech, cloud, cybersecurity, and analytics.",
        "certifications": ["AWS Cloud Practitioner", "Azure Fundamentals", "Google Data Analytics", "Security+"],
        "programming_languages": ["Python", "Java", "SQL", "JavaScript"],
        "frameworks": ["React", "FastAPI", "Django", "Docker"],
        "country_skills": ["Cloud Basics", "Communication", "Portfolio Projects"],
        "categories": {
            "AI": {"demand": "High", "entry": "75-95", "mid": "100-135", "senior": "140-190"},
            "Data": {"demand": "High", "entry": "65-85", "mid": "90-120", "senior": "125-165"},
            "Cybersecurity": {"demand": "High", "entry": "70-90", "mid": "95-130", "senior": "135-180"},
            "Cloud": {"demand": "High", "entry": "75-98", "mid": "105-140", "senior": "145-195"},
            "Software": {"demand": "High", "entry": "70-92", "mid": "95-130", "senior": "135-185"},
            "Product": {"demand": "Medium", "entry": "80-105", "mid": "110-150", "senior": "155-210"},
            "Design": {"demand": "Medium", "entry": "58-78", "mid": "82-110", "senior": "115-150"},
        },
    },
    "Australia": {
        "currency": "AUD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "High",
        "top_hiring_companies": ["Atlassian", "Canva", "Telstra", "Commonwealth Bank", "REA Group", "Xero"],
        "interview_process": ["Recruiter screen", "Technical interview", "Case/project round", "Culture interview"],
        "future_demand": "High future demand, led by cloud, cybersecurity, data, AI adoption, and product engineering.",
        "certifications": ["AWS Solutions Architect", "Azure Administrator", "Google Data Analytics", "Security+"],
        "programming_languages": ["Python", "JavaScript", "Java", "SQL"],
        "frameworks": ["React", "Node.js", "FastAPI", "Docker"],
        "country_skills": ["Cloud Platforms", "Communication", "Local Market Projects"],
        "categories": {
            "AI": {"demand": "High", "entry": "85-110", "mid": "120-155", "senior": "165-220"},
            "Data": {"demand": "High", "entry": "75-95", "mid": "105-135", "senior": "145-190"},
            "Cybersecurity": {"demand": "Very High", "entry": "85-110", "mid": "120-160", "senior": "170-230"},
            "Cloud": {"demand": "Very High", "entry": "90-115", "mid": "125-165", "senior": "175-240"},
            "Software": {"demand": "High", "entry": "75-100", "mid": "105-145", "senior": "150-210"},
            "Product": {"demand": "Medium", "entry": "95-120", "mid": "130-170", "senior": "180-240"},
            "Design": {"demand": "Medium", "entry": "70-90", "mid": "95-125", "senior": "130-170"},
        },
    },
}


DEFAULT_CATEGORY_MARKETS = {
    "Finance": {"demand": "High", "entry": "45-65", "mid": "70-105", "senior": "115-170"},
    "Marketing": {"demand": "High", "entry": "40-58", "mid": "65-95", "senior": "105-150"},
    "Law": {"demand": "Medium", "entry": "45-70", "mid": "75-120", "senior": "130-220"},
    "Healthcare": {"demand": "High", "entry": "42-62", "mid": "70-105", "senior": "115-180"},
    "Education": {"demand": "Medium", "entry": "35-52", "mid": "55-82", "senior": "90-135"},
    "Engineering": {"demand": "High", "entry": "45-65", "mid": "70-105", "senior": "115-170"},
    "Government": {"demand": "Medium", "entry": "35-55", "mid": "60-95", "senior": "100-160"},
    "General": {"demand": "Medium", "entry": "38-58", "mid": "62-92", "senior": "100-150"},
}


PROFESSION_MARKET_PROFILES = {
    "Software": {
        "skills": ["DSA", "System Design", "Cloud", "DevOps", "Testing", "Git"],
        "companies": ["Google", "Microsoft", "Amazon", "Infosys", "TCS", "Atlassian"],
        "certifications": ["AWS Cloud Practitioner", "Meta Back-End Developer", "Oracle Java", "Scrum Fundamentals"],
        "interview": ["Resume Screening", "Online Coding Assessment", "Technical Interview", "System Design Round", "HR Interview"],
        "future_demand": "Product engineering, platform modernization, cloud migration, and secure digital services continue to drive software hiring.",
        "market_insights": [
            "Employers value clean code, debugging ability, system thinking, and shipped projects.",
            "Backend, cloud, mobile, and full-stack teams remain active across product and services companies.",
        ],
        "programming_languages": ["Python", "Java", "JavaScript", "TypeScript"],
        "frameworks": ["React", "FastAPI", "Spring Boot", "Docker"],
    },
    "AI": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "MLOps", "Model Evaluation", "LLMs"],
        "companies": ["OpenAI", "NVIDIA", "Google", "Microsoft", "Fractal", "Turing"],
        "certifications": ["DeepLearning.AI Machine Learning", "AWS Machine Learning Specialty", "Google Professional ML Engineer"],
        "interview": ["Resume Screening", "ML Fundamentals Round", "Modeling Case", "Deployment Discussion", "HR Interview"],
        "future_demand": "Automation, generative AI adoption, model deployment, and AI governance are expanding demand for applied AI talent.",
        "market_insights": [
            "Production proof matters more than notebook-only projects.",
            "Model evaluation, data quality, deployment, and business impact separate stronger candidates.",
        ],
        "programming_languages": ["Python", "SQL"],
        "frameworks": ["PyTorch", "TensorFlow", "FastAPI", "Docker"],
    },
    "Data": {
        "skills": ["Machine Learning", "Statistics", "Python", "SQL", "Data Visualization", "Experiment Design"],
        "companies": ["Fractal", "Mu Sigma", "Deloitte", "Amazon", "RBC", "ZS Associates"],
        "certifications": ["Google Data Analytics", "Microsoft PL-300", "IBM Data Science"],
        "interview": ["Resume Screening", "Statistics Round", "SQL/Python Assessment", "Business Case", "HR Interview"],
        "future_demand": "Decision automation, analytics modernization, and data-driven operations continue to increase demand.",
        "market_insights": [
            "Hiring managers look for business context, clean analysis, and clear storytelling.",
            "Dashboards, SQL depth, and statistical reasoning are strong market signals.",
        ],
        "programming_languages": ["Python", "SQL", "R"],
        "frameworks": ["Pandas", "Power BI", "Tableau"],
    },
    "Cybersecurity": {
        "skills": ["Pen Testing", "SOC", "Incident Response", "SIEM", "Threat Intelligence", "Cloud Security"],
        "companies": ["CrowdStrike", "Palo Alto Networks", "Deloitte", "EY", "Wipro", "Tata Communications"],
        "certifications": ["CompTIA Security+", "CEH", "CISSP", "Splunk Core"],
        "interview": ["Resume Screening", "Security Fundamentals Round", "Scenario Assessment", "Incident Response Discussion", "HR Interview"],
        "future_demand": "Rising cyber risk, compliance pressure, cloud adoption, and ransomware defense are driving security hiring.",
        "market_insights": [
            "Hands-on labs, incident writeups, and detection rules make security profiles stronger.",
            "SOC, cloud security, application security, and GRC remain active hiring areas.",
        ],
        "programming_languages": ["Python", "Bash", "PowerShell"],
        "frameworks": ["MITRE ATT&CK", "NIST CSF", "SIEM"],
    },
    "Cloud": {
        "skills": ["Cloud Platforms", "Linux", "Docker", "Kubernetes", "Terraform", "CI/CD"],
        "companies": ["AWS Partners", "Microsoft", "Google Cloud", "Accenture", "Capgemini", "Infosys"],
        "certifications": ["AWS Solutions Architect", "Azure Administrator", "Google Associate Cloud Engineer", "CKA"],
        "interview": ["Resume Screening", "Cloud Architecture Round", "Infrastructure Task", "Operations Scenario", "HR Interview"],
        "future_demand": "Migration, modernization, cost optimization, and resilient infrastructure continue to drive cloud roles.",
        "market_insights": [
            "Infrastructure as code, monitoring, and incident handling are key differentiators.",
            "Employers prefer candidates who can explain tradeoffs, reliability, and security.",
        ],
        "programming_languages": ["Python", "Bash", "Go"],
        "frameworks": ["Docker", "Kubernetes", "Terraform"],
    },
    "Healthcare": {
        "skills": ["Patient Care", "Clinical Assessment", "Medication Administration", "Infection Control", "Clinical Documentation"],
        "companies": ["Apollo Hospitals", "Fortis", "Max Healthcare", "Narayana Health", "Manipal Hospitals", "NHS"],
        "certifications": ["BLS", "ACLS", "Infection Control", "Critical Care Nursing", "Clinical Pharmacy"],
        "interview": ["Resume Screening", "HR Interview", "Clinical Assessment", "Practical Test", "Department Interview"],
        "future_demand": "Aging populations, hospital expansion, preventive healthcare, and increasing patient volumes continue to drive demand.",
        "market_insights": [
            "Hospitals value patient safety, clinical judgment, documentation, and shift readiness.",
            "Specialized clinical certifications improve access to stronger departments and senior roles.",
        ],
        "programming_languages": [],
        "frameworks": [],
    },
    "Finance": {
        "skills": ["Financial Reporting", "Taxation", "Audit", "SAP", "IFRS", "Financial Modeling"],
        "companies": ["Deloitte", "PwC", "EY", "KPMG", "JP Morgan", "HDFC Bank"],
        "certifications": ["CA", "CFA Level 1", "FMVA", "ACCA", "NISM"],
        "interview": ["Resume Screening", "Finance Technical Round", "Excel/Case Assessment", "Manager Interview", "HR Interview"],
        "future_demand": "Regulatory compliance, digital finance, audit quality, risk management, and business expansion are increasing demand.",
        "market_insights": [
            "Employers value accuracy, controls, reporting discipline, and business judgment.",
            "ERP exposure, statutory knowledge, and financial modeling improve senior progression.",
        ],
        "programming_languages": [],
        "frameworks": ["Excel", "Power BI", "SAP", "Tally"],
    },
    "Marketing": {
        "skills": ["SEO", "Branding", "Campaign Management", "Digital Marketing", "Analytics", "Copywriting"],
        "companies": ["Ogilvy", "WPP", "Dentsu", "HubSpot", "Nykaa", "Zomato"],
        "certifications": ["Google Ads", "HubSpot Content Marketing", "Meta Blueprint", "Google Analytics"],
        "interview": ["Resume Screening", "Portfolio Review", "Campaign Case", "Manager Interview", "HR Interview"],
        "future_demand": "Brand growth, digital channels, performance marketing, and customer retention continue to drive marketing demand.",
        "market_insights": [
            "Campaign outcomes, audience insight, and creative testing matter more than generic tool lists.",
            "SEO, paid media, brand strategy, and analytics remain high-value proof areas.",
        ],
        "programming_languages": [],
        "frameworks": ["Google Analytics", "Google Ads", "Meta Ads", "HubSpot"],
    },
    "Law": {
        "skills": ["Litigation", "Corporate Law", "Legal Research", "Contract Drafting", "Compliance", "Advocacy"],
        "companies": ["Khaitan & Co", "Trilegal", "Cyril Amarchand Mangaldas", "AZB", "Shardul Amarchand"],
        "certifications": ["Contract Drafting", "Corporate Law", "Compliance", "Intellectual Property Law"],
        "interview": ["Resume Screening", "Legal Research Round", "Drafting Test", "Case Discussion", "Partner Interview"],
        "future_demand": "Compliance, contracts, dispute resolution, privacy regulation, and transaction support continue to create legal demand.",
        "market_insights": [
            "Strong drafting samples, case reasoning, and statutory clarity improve hiring outcomes.",
            "Domain specialization helps lawyers progress into counsel and partner tracks.",
        ],
        "programming_languages": [],
        "frameworks": [],
    },
    "Engineering": {
        "skills": ["CAD", "Manufacturing", "Quality Control", "Safety", "Project Planning", "Technical Documentation"],
        "companies": ["Larsen & Toubro", "Siemens", "Bosch", "Tata Motors", "Schneider Electric", "ABB"],
        "certifications": ["AutoCAD Professional", "Six Sigma", "PMP Foundation", "Safety Certification"],
        "interview": ["Resume Screening", "Core Engineering Round", "Design/Process Task", "Site or Plant Scenario", "HR Interview"],
        "future_demand": "Infrastructure investment, manufacturing modernization, energy systems, and automation continue to support engineering demand.",
        "market_insights": [
            "Employers value fundamentals, safety awareness, documentation, and applied project proof.",
            "CAD, simulation, quality, and project controls improve progression.",
        ],
        "programming_languages": [],
        "frameworks": ["AutoCAD", "SolidWorks", "MATLAB", "ANSYS"],
    },
    "Architecture": {
        "skills": ["BIM", "Revit", "Urban Planning", "Building Codes", "Sustainable Design", "Client Presentation"],
        "companies": ["Hafeez Contractor", "CP Kukreja", "Gensler", "AECOM", "HOK", "SOM"],
        "certifications": ["Revit Architecture", "Green Building Certification", "BIM Professional"],
        "interview": ["Resume Screening", "Portfolio Review", "Design Critique", "Technical Drawing Discussion", "Client Scenario"],
        "future_demand": "Urban expansion, sustainable design, real estate redevelopment, and BIM adoption continue to drive architecture demand.",
        "market_insights": [
            "Portfolio quality, drawings, BIM fluency, and client communication decide most shortlists.",
            "Sustainability and building-code literacy improve senior opportunities.",
        ],
        "programming_languages": [],
        "frameworks": ["Revit", "AutoCAD", "SketchUp", "BIM"],
    },
    "Education": {
        "skills": ["Curriculum Development", "Classroom Management", "Assessment", "Pedagogy", "Student Counseling"],
        "companies": ["Schools", "Universities", "Byju's", "Unacademy", "Coursera Partners", "Public Education Departments"],
        "certifications": ["BEd", "TESOL", "Google Certified Educator", "Subject Teaching Certificate"],
        "interview": ["Resume Screening", "Teaching Demo", "Subject Knowledge Round", "Classroom Scenario", "Panel Interview"],
        "future_demand": "Education reforms, online learning, skill-based programs, and STEM education are increasing demand.",
        "market_insights": [
            "Lesson quality, student outcomes, assessment design, and communication are key signals.",
            "Digital teaching ability and subject depth improve long-term growth.",
        ],
        "programming_languages": [],
        "frameworks": ["LMS", "Assessment Rubrics", "Digital Content Tools"],
    },
    "Business": {
        "skills": ["Operations", "Stakeholder Management", "Sales", "CRM", "Process Improvement", "Negotiation"],
        "companies": ["Deloitte", "Accenture", "Tata Group", "Reliance Retail", "Amazon", "Flipkart"],
        "certifications": ["Google Project Management", "Six Sigma", "Business Analytics", "CRM Certification"],
        "interview": ["Resume Screening", "Business Case", "Role Scenario", "Manager Interview", "HR Interview"],
        "future_demand": "Business expansion, process improvement, customer growth, and operating efficiency continue to drive demand.",
        "market_insights": [
            "Employers value measurable business outcomes, coordination, and ownership.",
            "Process metrics, CRM proof, and stakeholder stories strengthen business profiles.",
        ],
        "programming_languages": [],
        "frameworks": ["CRM", "Excel", "Power BI", "Project Management Tools"],
    },
    "Creative": {
        "skills": ["Visual Design", "Storytelling", "Portfolio Development", "Brand Systems", "Client Communication"],
        "companies": ["WPP", "Dentsu", "Ogilvy", "Netflix", "Disney", "Canva"],
        "certifications": ["Adobe Certified Professional", "Google UX Design", "Figma Design", "Content Strategy"],
        "interview": ["Resume Screening", "Portfolio Review", "Creative Task", "Design Critique", "Client Scenario"],
        "future_demand": "Digital content, brand experience, product design, and media growth continue to support creative demand.",
        "market_insights": [
            "Portfolio originality, process clarity, and execution quality drive hiring decisions.",
            "Candidates with measurable campaign or product outcomes stand out.",
        ],
        "programming_languages": [],
        "frameworks": ["Figma", "Adobe Creative Cloud", "Canva"],
    },
    "Hospitality": {
        "skills": ["Guest Relations", "Hotel Operations", "Food Safety", "Service Recovery", "Event Planning"],
        "companies": ["Taj Hotels", "Oberoi Hotels", "Marriott", "Hilton", "Accor", "Emirates"],
        "certifications": ["Food Safety", "Hospitality Management", "Revenue Management", "Event Management"],
        "interview": ["Resume Screening", "Service Scenario", "Operations Interview", "Guest Handling Roleplay", "HR Interview"],
        "future_demand": "Tourism recovery, premium guest experience, events, and travel growth continue to drive hospitality demand.",
        "market_insights": [
            "Service quality, complaint handling, and operational discipline decide hiring strength.",
            "Food safety, revenue management, and guest-experience metrics improve growth.",
        ],
        "programming_languages": [],
        "frameworks": ["PMS Tools", "Revenue Management", "Food Safety SOPs"],
    },
    "Agriculture": {
        "skills": ["Crop Management", "Soil Science", "Agri Business", "Food Technology", "Sustainability"],
        "companies": ["ICAR", "IFFCO", "Amul", "ITC Agri", "Syngenta", "Cargill"],
        "certifications": ["Agri Business", "Food Safety", "Supply Chain Analytics", "Soil Health"],
        "interview": ["Resume Screening", "Field Knowledge Round", "Crop/Soil Case", "Operations Discussion", "HR Interview"],
        "future_demand": "Food security, agri supply chains, precision farming, and sustainability needs continue to drive demand.",
        "market_insights": [
            "Field exposure, crop knowledge, and market-linkage understanding matter strongly.",
            "Food technology and sustainability skills improve growth options.",
        ],
        "programming_languages": [],
        "frameworks": ["GIS Basics", "Food Safety Standards", "Supply Chain Tools"],
    },
    "Government": {
        "skills": ["Public Administration", "Policy Analysis", "Current Affairs", "Ethics", "Public Communication"],
        "companies": ["Government Departments", "Public Sector Units", "Municipal Bodies", "UN Agencies", "Think Tanks"],
        "certifications": ["Public Policy", "Governance", "Project Management", "Data for Public Policy"],
        "interview": ["Application Screening", "Written/Role Assessment", "Current Affairs Discussion", "Ethics Scenario", "Panel Interview"],
        "future_demand": "Public service delivery, regulation, infrastructure programs, and social-sector implementation sustain demand.",
        "market_insights": [
            "Policy clarity, public communication, ethics, and execution experience improve fit.",
            "Domain knowledge and documentation discipline are strong differentiators.",
        ],
        "programming_languages": [],
        "frameworks": ["Policy Frameworks", "Program Evaluation", "Public Finance"],
    },
    "Science": {
        "skills": ["Research Methods", "Laboratory Techniques", "Statistics", "Academic Writing", "Data Analysis"],
        "companies": ["CSIR", "ICMR", "ISRO", "Universities", "Biocon", "Research Labs"],
        "certifications": ["Research Methods", "Laboratory Safety", "Biostatistics", "Good Clinical Practice"],
        "interview": ["Resume Screening", "Research Discussion", "Methods Round", "Literature Critique", "Panel Interview"],
        "future_demand": "R&D investment, clinical studies, sustainability research, and applied science programs continue to drive demand.",
        "market_insights": [
            "Publication quality, methods rigor, and lab or field proof strengthen research profiles.",
            "Grant writing, statistics, and reproducibility improve senior progression.",
        ],
        "programming_languages": [],
        "frameworks": ["Research Design", "Statistics Tools", "Lab Protocols"],
    },
}


ADDITIONAL_COUNTRY_DATA = {
    "United Kingdom": {
        "currency": "GBP",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "High",
        "cost_of_living": "High",
        "language_requirements": ["English professional fluency"],
        "top_hiring_companies": ["BBC", "NHS", "Barclays", "Deloitte UK", "Google UK", "Rolls-Royce"],
        "interview_process": ["Recruiter screen", "Competency interview", "Role task or case", "Panel interview"],
        "future_demand": "Strong demand across AI, healthcare, finance, public services, education, and creative technology.",
        "certifications": ["Role-specific UK certificate", "Google Project Management", "AWS Cloud Practitioner", "CIPD for HR"],
        "programming_languages": ["Python", "SQL", "JavaScript", "R"],
        "frameworks": ["React", "Django", "Power BI", "Figma"],
        "country_skills": ["English Communication", "UK Work Culture", "Portfolio Evidence"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "45-60", "mid": "65-90", "senior": "95-140"},
            "Data": {"demand": "High", "entry": "38-52", "mid": "58-78", "senior": "85-120"},
            "Software": {"demand": "High", "entry": "40-55", "mid": "60-85", "senior": "90-135"},
            "Product": {"demand": "High", "entry": "48-65", "mid": "75-105", "senior": "115-170"},
            "Design": {"demand": "Medium", "entry": "35-48", "mid": "55-75", "senior": "82-115"},
            **DEFAULT_CATEGORY_MARKETS,
        },
    },
    "Singapore": {
        "currency": "SGD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "Very High",
        "remote_jobs": "Medium",
        "cost_of_living": "Very High",
        "language_requirements": ["English professional fluency"],
        "top_hiring_companies": ["Grab", "DBS", "Shopee", "GovTech", "Sea Group", "Accenture"],
        "interview_process": ["Recruiter screen", "Technical or case round", "Business round", "Leadership interview"],
        "future_demand": "Very strong demand in finance, AI, cybersecurity, logistics, healthcare, and regional business roles.",
        "certifications": ["AWS Solutions Architect", "Google Data Analytics", "CFA Level 1", "Project Management"],
        "programming_languages": ["Python", "SQL", "Java", "JavaScript"],
        "frameworks": ["React", "Spring Boot", "Power BI", "Docker"],
        "country_skills": ["Regional Business Context", "English Communication", "Cross-cultural Collaboration"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "70-95", "mid": "105-150", "senior": "165-240"},
            "Data": {"demand": "High", "entry": "60-82", "mid": "90-125", "senior": "135-190"},
            "Software": {"demand": "High", "entry": "65-90", "mid": "95-140", "senior": "150-220"},
            "Product": {"demand": "High", "entry": "80-110", "mid": "125-175", "senior": "190-280"},
            "Design": {"demand": "Medium", "entry": "55-75", "mid": "82-115", "senior": "125-175"},
            **DEFAULT_CATEGORY_MARKETS,
        },
    },
    "UAE": {
        "currency": "AED",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "Very High",
        "remote_jobs": "Medium",
        "cost_of_living": "High",
        "language_requirements": ["English professional fluency", "Arabic helpful for public-facing roles"],
        "top_hiring_companies": ["Emirates", "Etisalat", "Careem", "ADNOC", "PwC Middle East", "Dubai Government"],
        "interview_process": ["Recruiter screen", "Manager interview", "Case or portfolio round", "HR and offer discussion"],
        "future_demand": "High demand in finance, tourism, construction, AI, cybersecurity, healthcare, and government digital services.",
        "certifications": ["PMP", "AWS Cloud Practitioner", "CFA Level 1", "Google Ads"],
        "programming_languages": ["Python", "SQL", "JavaScript", "Java"],
        "frameworks": ["Power BI", "React", "Django", "Figma"],
        "country_skills": ["Business Communication", "Gulf Market Awareness", "Client Management"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "150-220", "mid": "240-360", "senior": "400-650"},
            "Data": {"demand": "High", "entry": "120-180", "mid": "200-300", "senior": "330-520"},
            "Software": {"demand": "High", "entry": "120-190", "mid": "210-320", "senior": "350-560"},
            "Product": {"demand": "High", "entry": "160-240", "mid": "270-420", "senior": "460-720"},
            "Design": {"demand": "Medium", "entry": "100-150", "mid": "170-260", "senior": "280-430"},
            **DEFAULT_CATEGORY_MARKETS,
        },
    },
    "Japan": {
        "currency": "JPY",
        "salary_suffix": "m",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "Medium",
        "cost_of_living": "High in Tokyo, medium elsewhere",
        "language_requirements": ["Japanese N3-N2 preferred", "English for global teams"],
        "top_hiring_companies": ["Rakuten", "Sony", "Toyota", "LINE Yahoo", "Mercari", "SoftBank"],
        "interview_process": ["Recruiter screen", "Technical or role round", "Culture fit", "Final manager interview"],
        "future_demand": "Strong future demand in robotics, software, automotive, healthcare, data, and bilingual business roles.",
        "certifications": ["JLPT N3/N2", "AWS Cloud Practitioner", "Data Analytics certificate"],
        "programming_languages": ["Python", "Java", "SQL", "JavaScript"],
        "frameworks": ["React", "Spring Boot", "Django", "TensorFlow"],
        "country_skills": ["Japanese Language", "Process Discipline", "Documentation"],
        "categories": {
            "AI": {"demand": "High", "entry": "5-7", "mid": "8-12", "senior": "13-20"},
            "Data": {"demand": "High", "entry": "4-6", "mid": "7-10", "senior": "11-16"},
            "Software": {"demand": "High", "entry": "4-7", "mid": "7-11", "senior": "12-18"},
            "Product": {"demand": "Medium", "entry": "6-8", "mid": "9-14", "senior": "15-22"},
            "Design": {"demand": "Medium", "entry": "4-6", "mid": "7-10", "senior": "11-15"},
            **DEFAULT_CATEGORY_MARKETS,
        },
    },
    "France": {
        "currency": "EUR",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "Medium",
        "cost_of_living": "High in Paris, medium elsewhere",
        "language_requirements": ["French B1-B2 preferred", "English for international teams"],
        "top_hiring_companies": ["Dassault Systemes", "Capgemini", "L'Oreal", "BNP Paribas", "Airbus", "Mistral AI"],
        "interview_process": ["Recruiter screen", "Role interview", "Case or technical task", "Team fit interview"],
        "future_demand": "High demand in AI, aerospace, luxury, finance, healthcare, public tech, and design.",
        "certifications": ["French B1", "AWS Cloud Practitioner", "Google Data Analytics", "Role-specific certificate"],
        "programming_languages": ["Python", "SQL", "Java", "JavaScript"],
        "frameworks": ["React", "Django", "Docker", "Power BI"],
        "country_skills": ["French Language", "EU Work Culture", "Portfolio Evidence"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "42-55", "mid": "60-82", "senior": "88-125"},
            "Data": {"demand": "High", "entry": "38-50", "mid": "55-75", "senior": "80-110"},
            "Software": {"demand": "High", "entry": "38-52", "mid": "58-80", "senior": "85-120"},
            "Product": {"demand": "Medium", "entry": "45-60", "mid": "68-95", "senior": "105-145"},
            "Design": {"demand": "Medium", "entry": "34-46", "mid": "50-68", "senior": "75-100"},
            **DEFAULT_CATEGORY_MARKETS,
        },
    },
    "Netherlands": {
        "currency": "EUR",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "High",
        "cost_of_living": "High in Amsterdam, medium-high elsewhere",
        "language_requirements": ["English professional fluency", "Dutch helpful for public-facing roles"],
        "top_hiring_companies": ["ASML", "Booking.com", "Philips", "Adyen", "ING", "TomTom"],
        "interview_process": ["Recruiter screen", "Role task", "Team interview", "Culture interview"],
        "future_demand": "High demand in semiconductors, AI, data, logistics, finance, design, and sustainability careers.",
        "certifications": ["AWS Solutions Architect", "Scrum.org PSM", "Dutch A2 helpful", "Google Data Analytics"],
        "programming_languages": ["Python", "SQL", "Java", "TypeScript"],
        "frameworks": ["React", "Django", "Docker", "Kubernetes"],
        "country_skills": ["English Communication", "EU Collaboration", "Portfolio Evidence"],
        "categories": {
            "AI": {"demand": "Very High", "entry": "50-65", "mid": "72-95", "senior": "105-145"},
            "Data": {"demand": "High", "entry": "45-58", "mid": "65-85", "senior": "92-125"},
            "Software": {"demand": "High", "entry": "48-62", "mid": "68-90", "senior": "98-140"},
            "Product": {"demand": "High", "entry": "58-75", "mid": "85-115", "senior": "125-175"},
            "Design": {"demand": "Medium", "entry": "42-55", "mid": "60-78", "senior": "85-115"},
            **DEFAULT_CATEGORY_MARKETS,
        },
    },
}


COUNTRY_MARKET_DATA.update(ADDITIONAL_COUNTRY_DATA)


REGIONAL_COUNTRY_GROUPS = {
    "North America": ["Mexico", "Jamaica", "Dominican Republic", "Trinidad and Tobago"],
    "Latin America": [
        "Brazil",
        "Argentina",
        "Chile",
        "Colombia",
        "Peru",
        "Uruguay",
        "Costa Rica",
        "Panama",
        "Ecuador",
        "Bolivia",
        "Paraguay",
        "Guatemala",
        "El Salvador",
    ],
    "Europe": [
        "Czech Republic",
        "Italy",
        "Hungary",
        "Romania",
        "Greece",
        "Luxembourg",
        "Iceland",
        "Estonia",
        "Latvia",
        "Lithuania",
        "Slovakia",
        "Slovenia",
        "Croatia",
        "Bulgaria",
        "Serbia",
        "Turkey",
        "Malta",
        "Cyprus",
        "Ukraine",
        "Georgia",
        "Armenia",
        "Russia",
    ],
    "Middle East": ["Saudi Arabia", "Qatar", "Kuwait", "Bahrain", "Oman", "Israel", "Jordan", "Lebanon"],
    "Africa": [
        "South Africa",
        "Egypt",
        "Nigeria",
        "Kenya",
        "Morocco",
        "Ghana",
        "Rwanda",
        "Ethiopia",
        "Tanzania",
        "Uganda",
        "Senegal",
        "Tunisia",
        "Algeria",
        "Botswana",
        "Namibia",
        "Mauritius",
    ],
    "Asia": [
        "China",
        "Hong Kong",
        "Taiwan",
        "Malaysia",
        "Thailand",
        "Indonesia",
        "Vietnam",
        "Philippines",
        "Sri Lanka",
        "Nepal",
        "Myanmar",
        "Cambodia",
        "Laos",
        "Mongolia",
        "Kazakhstan",
        "Uzbekistan",
    ],
    "Oceania": ["Fiji", "Papua New Guinea", "Samoa"],
}


REGIONAL_MARKET_TEMPLATES = {
    "North America": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "High",
        "cost_of_living": "Medium to High",
        "language_requirements": ["English helpful", "Spanish helpful in Mexico"],
        "top_hiring_companies": ["multinational employers", "banks", "technology firms", "healthcare networks", "manufacturing groups"],
        "interview_process": ["Recruiter screen", "Role interview", "Practical task or case", "Final manager interview"],
        "future_demand": "Demand is strongest in digital transformation, healthcare, finance, manufacturing, logistics, and professional services.",
        "certifications": ["Role-specific professional certificate", "Project Management", "Digital tools certification"],
        "programming_languages": ["Python", "SQL", "JavaScript"],
        "frameworks": ["Power BI", "Cloud tools", "Role-specific platforms"],
        "country_skills": ["English Communication", "Portfolio Evidence", "Local Market Awareness"],
        "major_industries": ["Technology", "Healthcare", "Finance", "Manufacturing", "Logistics"],
    },
    "Latin America": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "Medium to High",
        "remote_jobs": "High",
        "cost_of_living": "Medium",
        "language_requirements": ["Spanish or Portuguese usually required", "English improves remote roles"],
        "top_hiring_companies": ["Mercado Libre", "Nubank", "regional banks", "consulting firms", "healthcare groups"],
        "interview_process": ["Recruiter screen", "Role interview", "Portfolio or case review", "Final interview"],
        "future_demand": "Nearshore work, fintech, healthcare, digital commerce, education, and infrastructure are expanding opportunities.",
        "certifications": ["Role-specific professional certificate", "Google Career Certificate", "Project Management"],
        "programming_languages": ["Python", "SQL", "JavaScript"],
        "frameworks": ["Power BI", "CRM tools", "Role-specific platforms"],
        "country_skills": ["Local Language", "English Communication", "Remote Collaboration"],
        "major_industries": ["Fintech", "E-commerce", "Healthcare", "Education", "Infrastructure"],
    },
    "Europe": {
        "currency": "EUR",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "High",
        "cost_of_living": "Medium to High",
        "language_requirements": ["English professional fluency", "Local language improves non-technical roles"],
        "top_hiring_companies": ["EU employers", "banks", "manufacturers", "consulting firms", "public institutions"],
        "interview_process": ["Recruiter screen", "Role task", "Team interview", "Culture interview"],
        "future_demand": "Demand is strong in healthcare, engineering, public services, sustainability, finance, AI, and regulated industries.",
        "certifications": ["Role-specific EU credential", "Language certificate", "Project Management"],
        "programming_languages": ["Python", "SQL", "Java", "JavaScript"],
        "frameworks": ["Power BI", "Cloud tools", "Role-specific platforms"],
        "country_skills": ["EU Work Culture", "Documentation", "Local Language"],
        "major_industries": ["Engineering", "Healthcare", "Finance", "Public Sector", "Sustainability"],
    },
    "Middle East": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "Very High",
        "remote_jobs": "Medium",
        "cost_of_living": "Medium to High",
        "language_requirements": ["English professional fluency", "Arabic helpful for public-facing roles"],
        "top_hiring_companies": ["airlines", "energy companies", "construction firms", "banks", "government entities"],
        "interview_process": ["Recruiter screen", "Manager interview", "Case or portfolio round", "HR discussion"],
        "future_demand": "Tourism, aviation, energy, construction, healthcare, finance, digital government, and AI investment drive growth.",
        "certifications": ["PMP", "Role-specific license", "Professional safety or compliance credential"],
        "programming_languages": ["Python", "SQL", "JavaScript"],
        "frameworks": ["Power BI", "CRM tools", "Role-specific platforms"],
        "country_skills": ["Client Communication", "Gulf Market Awareness", "Compliance"],
        "major_industries": ["Energy", "Aviation", "Construction", "Hospitality", "Healthcare"],
    },
    "Africa": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "High",
        "remote_jobs": "Medium",
        "cost_of_living": "Low to Medium",
        "language_requirements": ["English or French depending on country", "Local language helpful"],
        "top_hiring_companies": ["banks", "telecom companies", "NGOs", "healthcare groups", "government agencies"],
        "interview_process": ["Resume screen", "Role interview", "Scenario or case round", "Final interview"],
        "future_demand": "Healthcare, education, public administration, telecom, fintech, agriculture, and infrastructure remain important growth areas.",
        "certifications": ["Role-specific credential", "Project Management", "Digital skills certificate"],
        "programming_languages": ["Python", "SQL", "JavaScript"],
        "frameworks": ["Power BI", "Mobile tools", "Role-specific platforms"],
        "country_skills": ["Local Context", "Communication", "Practical Field Experience"],
        "major_industries": ["Telecom", "Healthcare", "Finance", "Agriculture", "Public Sector"],
    },
    "Asia": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "Very High",
        "remote_jobs": "Medium",
        "cost_of_living": "Low to High by city",
        "language_requirements": ["English helpful", "Local language often required for public-facing roles"],
        "top_hiring_companies": ["technology firms", "manufacturers", "banks", "healthcare groups", "education providers"],
        "interview_process": ["Resume screen", "Role assessment", "Manager interview", "HR interview"],
        "future_demand": "Manufacturing, digital services, healthcare, finance, education, logistics, and AI adoption are expanding career opportunities.",
        "certifications": ["Role-specific professional certificate", "Digital tools certification", "Project Management"],
        "programming_languages": ["Python", "SQL", "JavaScript", "Java"],
        "frameworks": ["Power BI", "Cloud tools", "Role-specific platforms"],
        "country_skills": ["Local Language", "Documentation", "Practical Portfolio"],
        "major_industries": ["Technology", "Manufacturing", "Finance", "Healthcare", "Education"],
    },
    "Oceania": {
        "currency": "USD",
        "salary_suffix": "k",
        "visa_difficulty": "Medium",
        "market_growth": "Medium",
        "remote_jobs": "Medium",
        "cost_of_living": "Medium",
        "language_requirements": ["English professional fluency"],
        "top_hiring_companies": ["hospitality employers", "public services", "education providers", "healthcare groups"],
        "interview_process": ["Resume screen", "Role interview", "Practical discussion", "Final interview"],
        "future_demand": "Hospitality, healthcare, education, tourism, public services, and remote professional work create opportunities.",
        "certifications": ["Role-specific credential", "Hospitality or safety certificate", "Project Management"],
        "programming_languages": ["Python", "SQL"],
        "frameworks": ["Office tools", "Role-specific platforms"],
        "country_skills": ["English Communication", "Service Orientation", "Local Market Awareness"],
        "major_industries": ["Tourism", "Healthcare", "Education", "Public Services", "Hospitality"],
    },
}


COUNTRY_CURRENCY_OVERRIDES = {
    "Mexico": "MXN",
    "Brazil": "BRL",
    "Argentina": "ARS",
    "Chile": "CLP",
    "Colombia": "COP",
    "Peru": "PEN",
    "Uruguay": "UYU",
    "Costa Rica": "CRC",
    "Panama": "PAB",
    "Jamaica": "JMD",
    "Dominican Republic": "DOP",
    "Trinidad and Tobago": "TTD",
    "Ecuador": "USD",
    "Bolivia": "BOB",
    "Paraguay": "PYG",
    "Guatemala": "GTQ",
    "El Salvador": "USD",
    "Czech Republic": "CZK",
    "Italy": "EUR",
    "Hungary": "HUF",
    "Romania": "RON",
    "Greece": "EUR",
    "Luxembourg": "EUR",
    "Iceland": "ISK",
    "Estonia": "EUR",
    "Latvia": "EUR",
    "Lithuania": "EUR",
    "Slovakia": "EUR",
    "Slovenia": "EUR",
    "Croatia": "EUR",
    "Bulgaria": "BGN",
    "Serbia": "RSD",
    "Turkey": "TRY",
    "Malta": "EUR",
    "Cyprus": "EUR",
    "Ukraine": "UAH",
    "Georgia": "GEL",
    "Armenia": "AMD",
    "Russia": "RUB",
    "Saudi Arabia": "SAR",
    "Qatar": "QAR",
    "Kuwait": "KWD",
    "Bahrain": "BHD",
    "Oman": "OMR",
    "Israel": "ILS",
    "Jordan": "JOD",
    "Lebanon": "LBP",
    "South Africa": "ZAR",
    "Egypt": "EGP",
    "Nigeria": "NGN",
    "Kenya": "KES",
    "Morocco": "MAD",
    "Ghana": "GHS",
    "Rwanda": "RWF",
    "Ethiopia": "ETB",
    "Tanzania": "TZS",
    "Uganda": "UGX",
    "Senegal": "XOF",
    "Tunisia": "TND",
    "Algeria": "DZD",
    "Botswana": "BWP",
    "Namibia": "NAD",
    "Mauritius": "MUR",
    "China": "CNY",
    "Hong Kong": "HKD",
    "Taiwan": "TWD",
    "Malaysia": "MYR",
    "Thailand": "THB",
    "Indonesia": "IDR",
    "Vietnam": "VND",
    "Philippines": "PHP",
    "Pakistan": "PKR",
    "Bangladesh": "BDT",
    "Sri Lanka": "LKR",
    "Nepal": "NPR",
    "Myanmar": "MMK",
    "Cambodia": "KHR",
    "Laos": "LAK",
    "Mongolia": "MNT",
    "Kazakhstan": "KZT",
    "Uzbekistan": "UZS",
    "Fiji": "FJD",
    "Papua New Guinea": "PGK",
    "Samoa": "WST",
}


REGIONAL_CATEGORY_MARKETS = {
    "North America": DEFAULT_CATEGORY_MARKETS,
    "Latin America": {
        "Finance": {"demand": "High", "entry": "18-30", "mid": "35-58", "senior": "65-105"},
        "Marketing": {"demand": "High", "entry": "16-26", "mid": "30-48", "senior": "55-90"},
        "Law": {"demand": "Medium", "entry": "18-32", "mid": "38-65", "senior": "75-120"},
        "Healthcare": {"demand": "High", "entry": "16-28", "mid": "32-55", "senior": "60-100"},
        "Education": {"demand": "Medium", "entry": "14-24", "mid": "26-42", "senior": "48-75"},
        "Engineering": {"demand": "High", "entry": "18-32", "mid": "38-62", "senior": "70-110"},
        "Government": {"demand": "Medium", "entry": "14-24", "mid": "28-48", "senior": "55-90"},
        "General": {"demand": "Medium", "entry": "15-25", "mid": "30-50", "senior": "58-95"},
    },
    "Europe": DEFAULT_CATEGORY_MARKETS,
    "Middle East": DEFAULT_CATEGORY_MARKETS,
    "Africa": {
        "Finance": {"demand": "High", "entry": "12-22", "mid": "25-42", "senior": "50-85"},
        "Marketing": {"demand": "Medium", "entry": "10-18", "mid": "22-36", "senior": "42-70"},
        "Law": {"demand": "Medium", "entry": "12-22", "mid": "25-45", "senior": "52-90"},
        "Healthcare": {"demand": "High", "entry": "10-20", "mid": "24-42", "senior": "48-82"},
        "Education": {"demand": "High", "entry": "9-16", "mid": "18-32", "senior": "36-60"},
        "Engineering": {"demand": "High", "entry": "12-24", "mid": "28-48", "senior": "55-95"},
        "Government": {"demand": "Medium", "entry": "10-18", "mid": "22-38", "senior": "45-75"},
        "General": {"demand": "Medium", "entry": "10-18", "mid": "22-38", "senior": "45-75"},
    },
    "Asia": {
        "Finance": {"demand": "High", "entry": "12-25", "mid": "28-55", "senior": "65-120"},
        "Marketing": {"demand": "High", "entry": "10-22", "mid": "25-48", "senior": "55-100"},
        "Law": {"demand": "Medium", "entry": "12-26", "mid": "30-60", "senior": "70-130"},
        "Healthcare": {"demand": "High", "entry": "10-22", "mid": "26-50", "senior": "58-110"},
        "Education": {"demand": "Medium", "entry": "8-18", "mid": "20-38", "senior": "45-80"},
        "Engineering": {"demand": "High", "entry": "12-25", "mid": "30-60", "senior": "70-130"},
        "Government": {"demand": "Medium", "entry": "8-18", "mid": "20-40", "senior": "48-90"},
        "General": {"demand": "Medium", "entry": "10-20", "mid": "24-45", "senior": "52-95"},
    },
    "Oceania": DEFAULT_CATEGORY_MARKETS,
}


def register_global_country_data() -> None:
    for region, countries in REGIONAL_COUNTRY_GROUPS.items():
        template = REGIONAL_MARKET_TEMPLATES[region]
        for country in countries:
            if country in COUNTRY_MARKET_DATA:
                continue
            country_data = dict(template)
            country_data["currency"] = COUNTRY_CURRENCY_OVERRIDES.get(country, template["currency"])
            country_data["categories"] = dict(REGIONAL_CATEGORY_MARKETS.get(region, DEFAULT_CATEGORY_MARKETS))
            COUNTRY_MARKET_DATA[country] = country_data


register_global_country_data()
COUNTRY_CATEGORY_DEFAULTS = {
    "India": {
        "Finance": {"demand": "High", "entry": "4-8", "mid": "10-18", "senior": "22-45"},
        "Marketing": {"demand": "High", "entry": "3-6", "mid": "8-16", "senior": "18-35"},
        "Law": {"demand": "Medium", "entry": "4-8", "mid": "10-22", "senior": "25-60"},
        "Healthcare": {"demand": "High", "entry": "3-7", "mid": "8-18", "senior": "20-45"},
        "Education": {"demand": "Medium", "entry": "2-5", "mid": "6-12", "senior": "15-30"},
        "Engineering": {"demand": "High", "entry": "4-8", "mid": "10-20", "senior": "24-45"},
        "Government": {"demand": "Medium", "entry": "4-8", "mid": "9-16", "senior": "18-35"},
        "General": {"demand": "Medium", "entry": "3-6", "mid": "8-15", "senior": "18-32"},
    },
    "Japan": {
        "Finance": {"demand": "High", "entry": "4-6", "mid": "7-11", "senior": "12-18"},
        "Marketing": {"demand": "Medium", "entry": "3-5", "mid": "6-9", "senior": "10-15"},
        "Law": {"demand": "Medium", "entry": "4-7", "mid": "8-13", "senior": "14-22"},
        "Healthcare": {"demand": "High", "entry": "4-6", "mid": "7-11", "senior": "12-18"},
        "Education": {"demand": "Medium", "entry": "3-5", "mid": "5-8", "senior": "9-13"},
        "Engineering": {"demand": "High", "entry": "4-6", "mid": "7-11", "senior": "12-18"},
        "Government": {"demand": "Medium", "entry": "3-5", "mid": "6-9", "senior": "10-14"},
        "General": {"demand": "Medium", "entry": "3-5", "mid": "6-9", "senior": "10-15"},
    },
    "UAE": {
        "Finance": {"demand": "High", "entry": "90-150", "mid": "180-300", "senior": "350-600"},
        "Marketing": {"demand": "High", "entry": "70-120", "mid": "150-240", "senior": "280-450"},
        "Law": {"demand": "Medium", "entry": "100-180", "mid": "220-380", "senior": "450-750"},
        "Healthcare": {"demand": "High", "entry": "80-140", "mid": "170-280", "senior": "320-520"},
        "Education": {"demand": "Medium", "entry": "60-110", "mid": "120-200", "senior": "230-360"},
        "Engineering": {"demand": "High", "entry": "90-150", "mid": "180-300", "senior": "350-580"},
        "Government": {"demand": "Medium", "entry": "80-140", "mid": "160-260", "senior": "300-480"},
        "General": {"demand": "Medium", "entry": "70-120", "mid": "140-230", "senior": "260-420"},
    },
}
for _country_data in COUNTRY_MARKET_DATA.values():
    _country_data.setdefault("cost_of_living", "Medium")
    _country_data.setdefault("language_requirements", ["English helpful for global roles"])
for _country_name, _country_data in COUNTRY_MARKET_DATA.items():
    _defaults = COUNTRY_CATEGORY_DEFAULTS.get(_country_name, DEFAULT_CATEGORY_MARKETS)
    _country_data["categories"] = {**_defaults, **_country_data.get("categories", {})}
    if _country_name in COUNTRY_CATEGORY_DEFAULTS:
        _country_data["categories"].update(COUNTRY_CATEGORY_DEFAULTS[_country_name])

SUPPORTED_COUNTRIES = sorted(COUNTRY_MARKET_DATA)


@dataclass
class CountryCareerIntelligence:
    country: str
    career: str
    flag: str
    currency: str
    demand_level: str
    entry_salary: str
    mid_level_salary: str
    senior_salary: str
    average_salary: str
    remote_jobs: str
    remote_work_availability: str
    top_hiring_companies: list[str]
    major_hiring_industries: list[str]
    most_required_skills: list[str]
    most_valuable_certifications: list[str]
    most_valuable_programming_languages: list[str]
    most_valuable_frameworks: list[str]
    visa_difficulty: str
    visa_overview: str
    market_growth: str
    hiring_trend: str
    degree_requirements: list[str]
    career_progression: list[str]
    future_outlook: str
    interview_process: list[str]
    future_demand: str
    cost_of_living: str
    language_requirements: list[str]
    interview_style: str
    career_growth: str
    insights: list[str]


def get_country_career_intelligence(
    career_name: str,
    country: str,
    career_definition: dict[str, Any],
) -> CountryCareerIntelligence:
    selected_country = country if country in COUNTRY_MARKET_DATA else "India"
    country_data = COUNTRY_MARKET_DATA[selected_country]
    domain = str(career_definition.get("domain", "General") or "General")
    category = categorize_career(career_name, career_definition)
    market_profile = profession_market_profile(category, domain)
    market = country_data["categories"].get(
        category,
        country_data["categories"].get(domain, country_data["categories"].get("General", country_data["categories"].get("Software"))),
    )
    required_skills = career_definition.get("required_skills", [])
    most_required_skills = dedupe_list(required_skills[:5] + market_profile["skills"])[:7]
    is_technology = domain == "Technology" or (not domain and category in {"AI", "Data", "Cybersecurity", "Cloud", "Software"})
    top_companies = dedupe_list(
        (career_definition.get("top_hiring_companies") or career_definition.get("hiring_companies") or [])
        + market_profile["companies"]
    )[:8]
    certifications = (
        career_definition.get("certifications")
        or career_definition.get("preferred_certifications")
        or career_definition.get("recommended_certifications")
        or market_profile["certifications"]
    )
    certifications = dedupe_list(list(certifications) + market_profile["certifications"])[:8]
    interview_process = career_definition.get("interview_pattern") or market_profile["interview"]
    interview_process = dedupe_list(interview_process)[:6]
    future_demand = profession_future_demand(career_name, category, domain, market_profile)
    frameworks = career_definition.get("frameworks") or market_profile["frameworks"]

    intelligence = CountryCareerIntelligence(
        country=selected_country,
        career=career_name,
        flag=country_flag(selected_country),
        currency=country_data["currency"],
        demand_level=market["demand"],
        entry_salary=format_salary(country_data, market["entry"]),
        mid_level_salary=format_salary(country_data, market["mid"]),
        senior_salary=format_salary(country_data, market["senior"]),
        average_salary=format_salary(country_data, market["mid"]),
        remote_jobs=country_data["remote_jobs"],
        remote_work_availability=country_data["remote_jobs"],
        top_hiring_companies=top_companies,
        major_hiring_industries=major_hiring_industries(country_data, domain, category),
        most_required_skills=most_required_skills,
        most_valuable_certifications=certifications,
        most_valuable_programming_languages=market_profile["programming_languages"] if is_technology else [],
        most_valuable_frameworks=frameworks if is_technology else market_profile["frameworks"],
        visa_difficulty=country_data["visa_difficulty"],
        visa_overview=visa_overview(selected_country, country_data["visa_difficulty"], domain),
        market_growth=country_data["market_growth"],
        hiring_trend=hiring_trend(market["demand"], country_data["market_growth"]),
        degree_requirements=list(career_definition.get("degree_requirements", []))[:6],
        career_progression=list(career_definition.get("career_path", []))[:6],
        future_outlook=future_demand,
        interview_process=interview_process,
        future_demand=future_demand,
        cost_of_living=country_data.get("cost_of_living", "Medium"),
        language_requirements=country_data.get("language_requirements", ["English helpful for global roles"]),
        interview_style=", ".join(interview_process[:2]),
        career_growth=country_data.get("market_growth", "Medium"),
        insights=[],
    )
    intelligence.insights = build_country_insights(intelligence, category, market_profile)
    return intelligence


def categorize_career(career_name: str, career_definition: dict[str, Any] | None = None) -> str:
    normalized = career_name.casefold()
    priority_categories = ["Finance", "Marketing", "Law", "Healthcare", "Education", "Engineering", "Government", "Cybersecurity", "Cloud", "AI", "Data"]
    for category in priority_categories:
        if any(keyword in normalized for keyword in CAREER_CATEGORY_KEYWORDS.get(category, [])):
            return category
    for category, keywords in CAREER_CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    if career_definition:
        domain = str(career_definition.get("domain", "") or "")
        if domain:
            return {
                "Technology": "Software",
                "Creative": "Design",
                "Business": "Product",
            }.get(domain, domain)
    try:
        from services.career_knowledge import get_career_knowledge

        domain = get_career_knowledge(career_name).get("domain", "")
        return {
            "Technology": "Software",
            "Creative": "Design",
            "Business": "Product",
        }.get(domain, domain or "General")
    except Exception:
        return "General"


def profession_market_profile(category: str, domain: str) -> dict[str, Any]:
    """Return the isolated market dataset for the selected profession family."""
    if category in PROFESSION_MARKET_PROFILES:
        return PROFESSION_MARKET_PROFILES[category]
    if domain in PROFESSION_MARKET_PROFILES:
        return PROFESSION_MARKET_PROFILES[domain]
    return PROFESSION_MARKET_PROFILES["Business"]


def profession_future_demand(career_name: str, category: str, domain: str, profile: dict[str, Any]) -> str:
    base = str(profile["future_demand"])
    if career_name and career_name.casefold() not in base.casefold():
        return f"For {career_name}, {base[0].lower() + base[1:]}"
    return base


def dedupe_list(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        text = str(value).strip()
        if not text:
            continue
        key = text.casefold()
        if key not in seen:
            seen.add(key)
            result.append(text)
    return result


def format_salary(country_data: dict[str, Any], salary_range: str) -> str:
    if "-" in salary_range:
        low, high = salary_range.split("-", 1)
        suffix = country_data["salary_suffix"]
        return f"{country_data['currency']} {low}{suffix} - {country_data['currency']} {high}{suffix}"
    return f"{country_data['currency']} {salary_range}{country_data['salary_suffix']}"


def salary_midpoint(value: str) -> int:
    import re

    numbers = [int(part) for part in re.findall(r"\d+", value)]
    if len(numbers) >= 2:
        return round(sum(numbers[:2]) / 2)
    return numbers[0] if numbers else 0


def country_flag(country: str) -> str:
    flags = {
        "India": "IN",
        "Germany": "DE",
        "USA": "US",
        "Canada": "CA",
        "Australia": "AU",
        "United Kingdom": "GB",
        "Singapore": "SG",
        "UAE": "AE",
        "Japan": "JP",
        "France": "FR",
        "Netherlands": "NL",
        "Sweden": "SE",
        "Switzerland": "CH",
        "New Zealand": "NZ",
        "South Korea": "KR",
        "Italy": "IT",
        "Spain": "ES",
        "Belgium": "BE",
        "Norway": "NO",
        "Denmark": "DK",
        "Finland": "FI",
        "Ireland": "IE",
        "Austria": "AT",
        "Portugal": "PT",
        "Poland": "PL",
        "Mexico": "MX",
        "Brazil": "BR",
        "Argentina": "AR",
        "Chile": "CL",
        "Colombia": "CO",
        "Peru": "PE",
        "Uruguay": "UY",
        "Costa Rica": "CR",
        "Panama": "PA",
        "Czech Republic": "CZ",
        "Hungary": "HU",
        "Romania": "RO",
        "Greece": "GR",
        "Luxembourg": "LU",
        "Iceland": "IS",
        "Estonia": "EE",
        "Latvia": "LV",
        "Lithuania": "LT",
        "Slovakia": "SK",
        "Slovenia": "SI",
        "Croatia": "HR",
        "Bulgaria": "BG",
        "Serbia": "RS",
        "Turkey": "TR",
        "Saudi Arabia": "SA",
        "Qatar": "QA",
        "Kuwait": "KW",
        "Bahrain": "BH",
        "Oman": "OM",
        "Israel": "IL",
        "South Africa": "ZA",
        "Egypt": "EG",
        "Nigeria": "NG",
        "Kenya": "KE",
        "Morocco": "MA",
        "Ghana": "GH",
        "Rwanda": "RW",
        "Ethiopia": "ET",
        "China": "CN",
        "Hong Kong": "HK",
        "Taiwan": "TW",
        "Malaysia": "MY",
        "Thailand": "TH",
        "Indonesia": "ID",
        "Vietnam": "VN",
        "Philippines": "PH",
        "Pakistan": "PK",
        "Bangladesh": "BD",
        "Sri Lanka": "LK",
        "Nepal": "NP",
        "Fiji": "FJ",
        "Russia": "RU",
    }
    return flag_emoji(flags.get(country, country[:2].upper()))


def flag_emoji(country_code: str) -> str:
    if len(country_code) != 2 or not country_code.isalpha():
        return country_code
    base = 127397
    return "".join(chr(base + ord(char.upper())) for char in country_code)


def visa_overview(country: str, difficulty: str, domain: str) -> str:
    if difficulty == "High":
        return f"{country} usually requires strong employer sponsorship, documentation, and clear role fit for {domain.lower()} careers."
    if difficulty == "Medium":
        return f"{country} has workable visa or permit routes, but local rules, documents, and employer readiness should be checked before applying."
    return f"{country} is generally straightforward for local candidates; international applicants should still verify work-permit rules."


def hiring_trend(demand: str, market_growth: str) -> str:
    if demand == "Very High" or market_growth == "Very High":
        return "Expanding"
    if demand == "High" or market_growth == "High":
        return "Growing"
    if demand == "Medium":
        return "Selective"
    return "Niche"


def major_hiring_industries(country_data: dict[str, Any], domain: str, category: str) -> list[str]:
    base = list(country_data.get("major_industries", []))
    domain_industries = {
        "Technology": ["Software Products", "Cloud Services", "Cybersecurity", "Fintech"],
        "Healthcare": ["Hospitals", "Clinics", "Pharmaceuticals", "Public Health"],
        "Finance": ["Banking", "Audit", "Investment", "Insurance"],
        "Law": ["Law Firms", "Corporate Legal", "Compliance", "Public Sector"],
        "Creative": ["Media", "Design Studios", "Advertising", "Entertainment"],
        "Hospitality": ["Hotels", "Tourism", "Airlines", "Events"],
        "Education": ["Schools", "Universities", "EdTech", "Training Institutes"],
        "Engineering": ["Manufacturing", "Construction", "Energy", "Infrastructure"],
        "Architecture": ["Architecture Firms", "Interior Design Studios", "Construction", "Real Estate"],
        "Government": ["Public Administration", "Policy", "PSUs", "Development Agencies"],
        "Business": ["Consulting", "Retail", "Operations", "Logistics"],
        "Entrepreneurship": ["Startups", "Small Business", "Venture Studios", "Incubators"],
        "Science": ["Research Labs", "Universities", "Biotechnology", "Environmental Research"],
        "Agriculture": ["Agri Business", "Food Technology", "Sustainability", "Supply Chain"],
        "Marketing": ["Digital Agencies", "Consumer Brands", "E-commerce", "Media"],
    }
    category_industries = {
        "AI": ["AI Products", "Research Labs", "Enterprise Automation"],
        "Data": ["Analytics", "Consulting", "Finance", "Healthcare"],
        "Cybersecurity": ["Security Services", "Banking", "Cloud Providers"],
        "Cloud": ["Cloud Providers", "Managed Services", "Enterprise IT"],
        "Marketing": ["Digital Agencies", "Consumer Brands", "E-commerce"],
        "Science": ["Research Labs", "Universities", "R&D Centers"],
    }
    return dedupe_list(base + category_industries.get(category, []) + domain_industries.get(domain, []))[:8]


def build_country_insights(intelligence: CountryCareerIntelligence, category: str, market_profile: dict[str, Any]) -> list[str]:
    insights = [
        f"{intelligence.career} in {intelligence.country} has {intelligence.demand_level.lower()} demand with {intelligence.market_growth.lower()} market growth.",
        f"Remote job availability is {intelligence.remote_jobs.lower()}, so profession-specific proof and communication skills affect opportunity quality.",
        f"Focus on {', '.join(intelligence.most_required_skills[:3])} first to improve local market fit.",
        f"Future demand: {intelligence.future_demand}",
    ]
    insights.extend(market_profile.get("market_insights", [])[:2])
    if intelligence.visa_difficulty == "High":
        insights.append("Visa difficulty is high, so strong portfolio proof and employer sponsorship readiness matter.")
    elif intelligence.visa_difficulty == "Medium":
        insights.append("Visa difficulty is manageable, but local language, documentation, and relevant experience improve outcomes.")
    else:
        insights.append("Visa difficulty is low for local candidates, so skills and portfolio quality become the main differentiators.")
    return insights
