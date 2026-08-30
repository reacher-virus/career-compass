from __future__ import annotations

from dataclasses import dataclass
from typing import Any


DOMAIN_KEYWORDS = {
    "Engineering": [
        "engineering",
        "btech",
        "b.tech",
        "be",
        "mechanical",
        "civil",
        "electrical",
        "electronics",
        "aerospace",
        "chemical",
        "robotics",
        "cad",
        "solidworks",
        "renewable energy",
        "solar energy",
        "wind energy",
        "grid operations",
        "pilot",
        "commercial pilot",
        "flight operations",
        "aviation safety",
        "marine engineer",
        "maritime safety",
    ],
    "Technology": [
        "computer science",
        "information technology",
        "python",
        "java",
        "sql",
        "cloud",
        "software",
        "developer",
        "machine learning",
        "cybersecurity",
    ],
    "Business": [
        "bba",
        "mba",
        "commerce",
        "management",
        "operations",
        "strategy",
        "sales",
        "human resources",
        "hr",
    ],
    "Finance": [
        "bcom",
        "accounting",
        "banking",
        "investment",
        "finance",
        "valuation",
        "tax",
        "audit",
        "financial modeling",
    ],
    "Marketing": [
        "marketing",
        "seo",
        "google ads",
        "content strategy",
        "brand",
        "social media",
        "campaign",
        "copywriting",
    ],
    "Law": [
        "llb",
        "llm",
        "law",
        "legal",
        "compliance",
        "contract",
        "litigation",
        "intellectual property",
        "cyber law",
    ],
    "Healthcare": [
        "mbbs",
        "nursing",
        "pharmacy",
        "pharmacist",
        "pharmaceutical",
        "formulation",
        "drug safety",
        "physiotherapy",
        "public health",
        "clinical",
        "patient",
        "biotechnology",
        "medical",
    ],
    "Science": [
        "bsc",
        "msc",
        "physics",
        "chemistry",
        "mathematics",
        "statistics",
        "biology",
        "research",
        "laboratory",
    ],
    "Education": [
        "teaching",
        "teacher",
        "education",
        "curriculum",
        "lesson plan",
        "pedagogy",
        "training",
    ],
    "Creative": [
        "design",
        "film",
        "media",
        "journalism",
        "photography",
        "animation",
        "ui ux",
        "fashion",
        "portfolio",
    ],
    "Hospitality": ["hotel management", "hospitality", "front office", "food and beverage", "tourism", "guest relations", "chef", "kitchen operations", "food safety", "menu planning"],
    "Architecture": ["architecture", "urban planning", "autocad", "revit", "building design", "model making", "interior designer", "interior design", "space planning", "lighting design"],
    "Agriculture": ["agriculture", "agronomy", "soil", "crop", "farm", "food technology", "sustainability"],
    "Government": ["upsc", "ssc", "government", "public administration", "policy", "civil services", "defence", "police officer", "law enforcement", "public safety", "citizen services"],
    "Entrepreneurship": ["startup", "founder", "business model", "pitch", "fundraising", "freelance", "entrepreneur"],
}


SKILLS_BY_DOMAIN = {
    "Engineering": ["CAD", "SolidWorks", "MATLAB", "AutoCAD", "Thermodynamics", "Circuit Design", "Quality Control"],
    "Technology": ["Python", "Java", "SQL", "Cloud", "Git", "Machine Learning", "Cybersecurity", "React", "Docker"],
    "Business": ["Market Research", "Operations", "Stakeholder Management", "Business Analytics", "Presentation", "Negotiation"],
    "Finance": ["Accounting", "Financial Modeling", "Valuation", "Excel", "Power BI", "Taxation", "Risk Analysis"],
    "Marketing": ["SEO", "Google Ads", "Content Strategy", "Copywriting", "Campaign Analytics", "Brand Strategy"],
    "Law": ["Legal Research", "Contract Drafting", "Compliance", "Litigation", "Case Analysis", "Legal Writing"],
    "Healthcare": ["Patient Care", "Clinical Research", "Medical Terminology", "Public Health", "Pharmacology", "Biostatistics"],
    "Science": ["Research Methods", "Laboratory Techniques", "Statistics", "Academic Writing", "Data Analysis"],
    "Education": ["Lesson Planning", "Curriculum Design", "Assessment", "Classroom Management", "Student Counseling"],
    "Creative": ["Figma", "Canva", "Adobe Photoshop", "Storytelling", "Visual Design", "User Research", "Video Editing"],
    "Hospitality": ["Guest Relations", "Food Safety", "Event Planning", "Hotel Operations", "Customer Service"],
    "Architecture": ["AutoCAD", "Revit", "SketchUp", "Building Codes", "Sustainable Design", "Model Making"],
    "Agriculture": ["Crop Science", "Soil Science", "Agri Business", "Sustainability", "Food Technology"],
    "Government": ["Current Affairs", "Policy Analysis", "Quantitative Aptitude", "Reasoning", "Essay Writing"],
    "Entrepreneurship": ["Business Model Design", "Sales", "Fundraising", "Pitching", "Customer Discovery"],
}


COMMON_SKILL_TERMS = {
    "communication",
    "presentation",
    "documentation",
    "leadership",
    "problem solving",
    "team collaboration",
    "collaboration",
    "stakeholder management",
    "decision making",
    "customer service",
    "market research",
    "data analysis",
    "excel",
    "project management",
    "negotiation",
    "english",
}


BASE_RESOURCES = {
    "books": ["The First 90 Days", "So Good They Can't Ignore You", "Designing Your Life"],
    "youtube_channels": ["CrashCourse", "Harvard Business Review", "TED-Ed"],
    "courses": ["Coursera role specialization", "edX professional certificate", "LinkedIn Learning role path"],
    "communities": ["LinkedIn Groups", "Reddit career communities", "Local professional meetups"],
    "practice_sites": ["Forage", "Internshala", "LinkedIn Jobs", "Role-specific case libraries"],
    "competitions": ["Case competitions", "Hackathons", "Research paper contests", "Portfolio challenges"],
    "professional_organizations": ["Local professional association", "University alumni network"],
    "internships": ["Role-specific internship", "Remote apprenticeship", "Campus placement project"],
}


CAREER_TEMPLATES: dict[str, dict[str, Any]] = {
    "AI Engineer": {
        "domain": "Technology",
        "description": "Builds AI systems, model APIs, evaluation workflows, and production-ready intelligent products.",
        "required_skills": ["Python", "SQL", "Machine Learning", "Deep Learning", "Docker", "FastAPI", "Cloud"],
        "technical_skills": ["Python", "PyTorch", "TensorFlow", "MLOps", "Vector Databases", "Model Evaluation"],
        "soft_skills": ["Problem Solving", "Communication", "Experiment Thinking"],
        "degree_requirements": ["Computer Science", "AI", "Data Science", "Mathematics", "related engineering degree"],
        "preferred_certifications": ["DeepLearning.AI Machine Learning", "AWS Machine Learning Specialty"],
        "target_projects": ["LLM app", "Model deployment API", "Computer vision pipeline"],
        "salary": "High",
        "future_growth": "Very High",
        "ai_impact": "Core AI builder role with strong upside and fast-changing tools.",
    },
    "Data Scientist": {
        "domain": "Technology",
        "description": "Uses statistics, machine learning, and business context to convert data into decisions.",
        "required_skills": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization", "Power BI"],
        "technical_skills": ["Python", "Pandas", "Statistics", "Experiment Design", "Dashboards"],
        "soft_skills": ["Business Communication", "Storytelling", "Critical Thinking"],
        "degree_requirements": ["Statistics", "Computer Science", "Mathematics", "Economics", "Data Science"],
        "preferred_certifications": ["Google Data Analytics", "Microsoft PL-300"],
        "target_projects": ["Customer churn model", "A/B testing report", "Executive dashboard"],
        "salary": "High",
        "future_growth": "High",
        "ai_impact": "AI automates basic analysis; strong data scientists move toward decision systems.",
    },
    "Mechanical Engineer": {
        "domain": "Engineering",
        "description": "Designs, tests, and improves mechanical systems, products, manufacturing workflows, and simulations.",
        "required_skills": ["CAD", "SolidWorks", "MATLAB", "Thermodynamics", "Quality Control", "Project Management"],
        "technical_skills": ["CAD", "FEA", "Manufacturing", "GD&T", "Simulation"],
        "soft_skills": ["Problem Solving", "Documentation", "Team Collaboration"],
        "degree_requirements": ["Mechanical Engineering", "Production Engineering"],
        "preferred_certifications": ["SolidWorks Associate", "Six Sigma Yellow Belt"],
        "target_projects": ["CAD assembly portfolio", "Thermal analysis report", "Manufacturing optimization case"],
        "salary": "Medium",
        "future_growth": "Medium to High",
        "ai_impact": "AI-assisted design and simulation increase demand for tool-fluent engineers.",
    },
    "Civil Engineer": {
        "domain": "Engineering",
        "description": "Plans, designs, and manages infrastructure, construction, and structural projects.",
        "required_skills": ["AutoCAD", "STAAD Pro", "Construction Management", "Surveying", "Project Planning"],
        "technical_skills": ["Structural Analysis", "BOQ", "Estimation", "Revit", "Site Safety"],
        "soft_skills": ["Coordination", "Negotiation", "Documentation"],
        "degree_requirements": ["Civil Engineering", "Construction Management"],
        "preferred_certifications": ["AutoCAD Civil", "Primavera P6"],
        "target_projects": ["Structural design portfolio", "Site planning report", "Cost estimation sheet"],
        "salary": "Medium",
        "future_growth": "Medium",
        "ai_impact": "Digital twins and BIM raise demand for data-aware civil engineers.",
    },
    "Finance Analyst": {
        "domain": "Finance",
        "description": "Analyzes financial performance, builds models, and supports investment or business decisions.",
        "required_skills": ["Excel", "Accounting", "Financial Modeling", "Valuation", "Power BI", "Business Communication"],
        "technical_skills": ["Excel", "Power BI", "Financial Statements", "Forecasting", "SQL"],
        "soft_skills": ["Attention to Detail", "Presentation", "Business Judgment"],
        "degree_requirements": ["BCom", "BBA", "MBA Finance", "Economics"],
        "preferred_certifications": ["CFA Level 1", "FMVA", "NISM"],
        "target_projects": ["Three-statement model", "Equity research report", "Budget variance dashboard"],
        "salary": "Medium to High",
        "future_growth": "High",
        "ai_impact": "AI handles repetitive reporting; analysts with modeling and storytelling win.",
    },
    "Digital Marketer": {
        "domain": "Marketing",
        "description": "Plans and optimizes digital campaigns across search, social, content, email, and analytics.",
        "required_skills": ["SEO", "Google Ads", "Content Strategy", "Campaign Analytics", "Copywriting", "A/B Testing"],
        "technical_skills": ["Google Analytics", "Search Console", "Meta Ads", "Email Automation"],
        "soft_skills": ["Creativity", "Customer Empathy", "Writing"],
        "degree_requirements": ["Marketing", "BBA", "Mass Communication", "any degree with portfolio"],
        "preferred_certifications": ["Google Ads", "HubSpot Content Marketing", "Meta Blueprint"],
        "target_projects": ["SEO audit", "Campaign performance dashboard", "Landing page experiment"],
        "salary": "Medium",
        "future_growth": "High",
        "ai_impact": "AI speeds content creation; strategy, analytics, and brand judgment remain valuable.",
    },
    "HR Manager": {
        "domain": "Business",
        "description": "Manages hiring, employee experience, learning, performance, and people operations.",
        "required_skills": ["Recruitment", "HR Analytics", "Employee Relations", "Communication", "Policy Writing"],
        "technical_skills": ["HRMS", "Excel", "People Analytics", "Interview Design"],
        "soft_skills": ["Empathy", "Conflict Resolution", "Confidentiality"],
        "degree_requirements": ["BBA", "MBA HR", "Psychology", "Human Resources"],
        "preferred_certifications": ["SHRM Foundation", "HRCI Associate Professional"],
        "target_projects": ["Hiring funnel analysis", "Employee engagement plan", "Policy audit"],
        "salary": "Medium",
        "future_growth": "Medium to High",
        "ai_impact": "AI supports screening and analytics; human judgment matters for culture and trust.",
    },
    "Corporate Lawyer": {
        "domain": "Law",
        "description": "Advises companies on contracts, compliance, governance, transactions, and legal risk.",
        "required_skills": ["Legal Research", "Contract Drafting", "Compliance", "Negotiation", "Legal Writing"],
        "technical_skills": ["Companies Act", "Contract Law", "Due Diligence", "IP Basics"],
        "soft_skills": ["Argumentation", "Ethics", "Attention to Detail"],
        "degree_requirements": ["LLB", "LLM", "Corporate Law specialization"],
        "preferred_certifications": ["Contract Drafting", "Corporate Law certificate", "Compliance certification"],
        "target_projects": ["Contract review portfolio", "Compliance memo", "Case brief collection"],
        "salary": "Medium to High",
        "future_growth": "High",
        "ai_impact": "AI accelerates research; judgment, drafting, negotiation, and compliance strategy become stronger differentiators.",
    },
    "Healthcare Administrator": {
        "domain": "Healthcare",
        "description": "Runs healthcare operations, patient workflows, compliance, quality, and service delivery.",
        "required_skills": ["Healthcare Operations", "Patient Care", "Public Health", "Data Analysis", "Compliance"],
        "technical_skills": ["Hospital Operations", "Quality Metrics", "Healthcare IT", "Excel"],
        "soft_skills": ["Empathy", "Coordination", "Decision Making"],
        "degree_requirements": ["Healthcare Management", "Public Health", "Nursing", "Pharmacy", "MBBS"],
        "preferred_certifications": ["Hospital Administration", "Public Health certificate"],
        "target_projects": ["Patient wait-time analysis", "Clinic operations dashboard", "Quality improvement plan"],
        "salary": "Medium",
        "future_growth": "High",
        "ai_impact": "AI improves triage and operations; healthcare leaders need data and compliance literacy.",
    },
    "Research Assistant": {
        "domain": "Science",
        "description": "Supports academic, scientific, or policy research through literature, experiments, data, and writing.",
        "required_skills": ["Research Methods", "Literature Review", "Statistics", "Academic Writing", "Data Analysis"],
        "technical_skills": ["SPSS", "Python", "R", "Experiment Design", "Citation Tools"],
        "soft_skills": ["Curiosity", "Patience", "Scientific Communication"],
        "degree_requirements": ["BSc", "MSc", "BA", "MA", "domain-specific degree"],
        "preferred_certifications": ["Research Methods", "Statistics certificate"],
        "target_projects": ["Literature review", "Reproducible notebook", "Survey report"],
        "salary": "Medium",
        "future_growth": "Medium to High",
        "ai_impact": "AI helps search and summarization; rigorous methods and original thinking stay essential.",
    },
    "UX Designer": {
        "domain": "Creative",
        "description": "Designs user-friendly digital experiences through research, wireframes, prototypes, and usability testing.",
        "required_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Usability Testing", "Design Systems"],
        "technical_skills": ["Figma", "Information Architecture", "Design Systems", "Accessibility"],
        "soft_skills": ["Empathy", "Storytelling", "Collaboration"],
        "degree_requirements": ["Design", "Psychology", "Arts", "Engineering", "any degree with portfolio"],
        "preferred_certifications": ["Google UX Design", "Nielsen Norman UX"],
        "target_projects": ["Mobile app redesign", "Usability study", "Design system case study"],
        "salary": "Medium to High",
        "future_growth": "High",
        "ai_impact": "AI speeds visual exploration; research, product sense, and usability judgment matter more.",
    },
    "Teacher": {
        "domain": "Education",
        "description": "Teaches learners through lesson planning, assessment, mentoring, and curriculum delivery.",
        "required_skills": ["Lesson Planning", "Curriculum Design", "Assessment", "Communication", "Classroom Management"],
        "technical_skills": ["Learning Management Systems", "Digital Content", "Assessment Tools"],
        "soft_skills": ["Patience", "Empathy", "Public Speaking"],
        "degree_requirements": ["BEd", "subject degree", "teaching certification"],
        "preferred_certifications": ["BEd", "TESOL", "Google Certified Educator"],
        "target_projects": ["Lesson plan portfolio", "Student assessment rubric", "Teaching demo video"],
        "salary": "Medium",
        "future_growth": "Medium",
        "ai_impact": "AI supports content and assessment; great teachers use it for personalization.",
    },
    "Hotel Manager": {
        "domain": "Hospitality",
        "description": "Manages guest experience, operations, staff, revenue, events, and service quality.",
        "required_skills": ["Guest Relations", "Hotel Operations", "Event Planning", "Customer Service", "Food Safety"],
        "technical_skills": ["PMS Tools", "Revenue Management", "Inventory", "Service SOPs"],
        "soft_skills": ["Communication", "Leadership", "Conflict Resolution"],
        "degree_requirements": ["Hotel Management", "Hospitality", "Tourism"],
        "preferred_certifications": ["Food Safety", "Hospitality Management certificate"],
        "target_projects": ["Guest experience improvement plan", "Event operations plan", "Revenue dashboard"],
        "salary": "Medium",
        "future_growth": "Medium to High",
        "ai_impact": "AI improves booking, pricing, and service analytics; human service quality remains central.",
    },
    "Architect": {
        "domain": "Architecture",
        "description": "Designs spaces, prepares plans, coordinates construction details, and balances function, beauty, and safety.",
        "required_skills": ["AutoCAD", "Revit", "SketchUp", "Building Codes", "Sustainable Design", "Presentation"],
        "technical_skills": ["BIM", "3D Modeling", "Rendering", "Construction Drawings"],
        "soft_skills": ["Creativity", "Client Communication", "Project Coordination"],
        "degree_requirements": ["BArch", "Architecture"],
        "preferred_certifications": ["Revit Architecture", "Green building certification"],
        "target_projects": ["Residential design portfolio", "Sustainable building concept", "BIM model"],
        "salary": "Medium",
        "future_growth": "Medium to High",
        "ai_impact": "Generative design helps ideation; architects with BIM and sustainability skills stand out.",
    },
    "Agri Business Analyst": {
        "domain": "Agriculture",
        "description": "Connects agriculture, markets, sustainability, and data to improve farm and food business decisions.",
        "required_skills": ["Agri Business", "Crop Science", "Excel", "Market Research", "Sustainability", "Data Analysis"],
        "technical_skills": ["Commodity Analysis", "Supply Chain", "GIS Basics", "Food Technology"],
        "soft_skills": ["Field Communication", "Problem Solving", "Stakeholder Management"],
        "degree_requirements": ["Agriculture", "Agri Business", "Food Technology", "Economics"],
        "preferred_certifications": ["Agri business certificate", "Supply chain analytics"],
        "target_projects": ["Crop pricing analysis", "Farm supply-chain dashboard", "Sustainability report"],
        "salary": "Medium",
        "future_growth": "High",
        "ai_impact": "AI supports precision agriculture and forecasting; field knowledge plus analytics is valuable.",
    },
    "Civil Services Aspirant": {
        "domain": "Government",
        "description": "Prepares for policy, administration, public service, and government examination pathways.",
        "required_skills": ["Current Affairs", "Policy Analysis", "Essay Writing", "Quantitative Aptitude", "Reasoning"],
        "technical_skills": ["Data Interpretation", "Governance", "Public Administration", "Economics"],
        "soft_skills": ["Discipline", "Ethics", "Communication"],
        "degree_requirements": ["Any recognized degree"],
        "preferred_certifications": ["Public policy certificate", "Constitution and governance course"],
        "target_projects": ["Policy brief", "Current affairs notes system", "Mock exam tracker"],
        "salary": "Structured government pay",
        "future_growth": "Stable",
        "ai_impact": "AI helps revision and analysis; exam judgment and writing clarity remain decisive.",
    },
    "Entrepreneur": {
        "domain": "Entrepreneurship",
        "description": "Builds and validates a business, product, or freelance practice through customers, execution, and growth.",
        "required_skills": ["Customer Discovery", "Sales", "Business Model Design", "Pitching", "Financial Planning"],
        "technical_skills": ["No-Code Tools", "Analytics", "Operations", "Basic Automation"],
        "soft_skills": ["Resilience", "Negotiation", "Leadership"],
        "degree_requirements": ["No fixed degree; proof of execution matters"],
        "preferred_certifications": ["Startup school", "Digital business certificate"],
        "target_projects": ["Landing page test", "Customer interview report", "MVP launch"],
        "salary": "Variable",
        "future_growth": "High upside, high uncertainty",
        "ai_impact": "AI lowers build and marketing costs, raising the value of customer insight and execution speed.",
    },
}


DOMAIN_PROFILES: dict[str, dict[str, Any]] = {
    "Technology": {
        "required_skills": ["Problem Solving", "Programming", "Git", "System Design", "Cloud Basics", "Testing"],
        "technical_skills": ["Python", "Java", "JavaScript", "Docker", "AWS", "SQL"],
        "tools": ["GitHub", "VS Code", "Docker", "Postman", "Jira"],
        "software": ["Linux", "Cloud Consoles", "CI/CD Tools"],
        "frameworks": ["React", "FastAPI", "Django", "Spring Boot"],
        "certifications": ["AWS Cloud Practitioner", "Google Cloud Digital Leader", "Meta Developer Certificate"],
        "books": ["Clean Code", "Designing Data-Intensive Applications", "System Design Interview"],
        "courses": ["CS50", "freeCodeCamp", "Meta Software Developer"],
        "youtube_channels": ["freeCodeCamp", "Fireship", "ByteByteGo"],
        "communities": ["GitHub", "Stack Overflow", "Dev.to"],
        "professional_organizations": ["ACM", "IEEE Computer Society"],
        "practice_platforms": ["LeetCode", "HackerRank", "Kaggle"],
        "companies": ["Google", "Microsoft", "Amazon", "OpenAI", "NVIDIA", "Meta"],
        "portfolio": ["GitHub repositories", "deployed application", "technical case study"],
        "interview": ["Coding round", "System design", "Project deep dive", "Behavioral interview"],
        "salary_ranges": {"India": ["6-12 LPA", "15-30 LPA", "35-80 LPA"]},
        "remote": "High",
        "freelance": "High",
        "startup": "High",
        "ai_impact": "AI raises productivity but increases expectations for architecture, debugging, and product judgment.",
    },
    "Engineering": {
        "required_skills": ["Engineering Drawing", "CAD", "Quality Control", "Project Planning", "Safety", "Documentation"],
        "technical_skills": ["AutoCAD", "SolidWorks", "MATLAB", "Simulation", "Manufacturing"],
        "tools": ["AutoCAD", "SolidWorks", "ANSYS", "MATLAB", "Primavera"],
        "software": ["CAD suites", "Simulation tools", "Project planning tools"],
        "frameworks": [],
        "certifications": ["Six Sigma", "AutoCAD Professional", "PMP Foundation"],
        "books": ["Engineering Mechanics", "The Goal", "Project Management for Engineering"],
        "courses": ["NPTEL engineering courses", "Coursera CAD specialization", "edX engineering management"],
        "youtube_channels": ["NPTEL", "Learn Engineering", "The Efficient Engineer"],
        "communities": ["IEEE", "ASME", "SAE", "Institution of Engineers"],
        "professional_organizations": ["IEEE", "ASME", "SAE International"],
        "practice_platforms": ["SAE competitions", "CAD challenges", "NPTEL assignments"],
        "companies": ["Larsen & Toubro", "Siemens", "Bosch", "Tata Motors", "Schneider Electric"],
        "portfolio": ["CAD portfolio", "simulation report", "manufacturing case study"],
        "interview": ["Core engineering concepts", "Design task", "Project discussion", "Safety and process round"],
        "salary_ranges": {"India": ["4-8 LPA", "10-20 LPA", "24-45 LPA"]},
        "remote": "Low to Medium",
        "freelance": "Medium",
        "startup": "Medium",
        "ai_impact": "AI-assisted design and simulation reward engineers who combine fundamentals with modern tools.",
    },
    "Healthcare": {
        "required_skills": ["Patient Care", "Healthcare Operations", "Medical Records", "Compliance", "Healthcare Finance", "Quality Improvement"],
        "technical_skills": ["Hospital Management", "Patient Safety", "NABH Standards", "Healthcare Analytics", "Clinical Workflow"],
        "tools": ["EHR Systems", "Hospital Information Systems", "Excel", "Quality Dashboards"],
        "software": ["Hospital management software", "EHR platforms", "Medical records systems"],
        "frameworks": [],
        "certifications": ["NABH", "Lean Healthcare", "Hospital Administration", "Public Health", "Healthcare Leadership"],
        "books": ["The Goal", "Healthcare Operations Management", "Healthcare Strategy"],
        "courses": ["Coursera Healthcare Management", "WHO Learning", "Harvard Public Health", "Johns Hopkins Healthcare"],
        "youtube_channels": ["WHO", "Johns Hopkins Bloomberg School", "Healthcare Triage"],
        "communities": ["Public health forums", "Hospital administration networks", "Healthcare leadership groups"],
        "professional_organizations": ["WHO", "Indian Medical Association", "ACHE", "Public Health Foundation of India"],
        "practice_platforms": ["WHO case studies", "Public health simulations", "Hospital operations case studies"],
        "companies": ["Apollo Hospitals", "Fortis", "Medanta", "Manipal Hospitals", "Max Healthcare", "Narayana Health", "WHO", "UNICEF"],
        "portfolio": ["patient wait-time improvement plan", "hospital operations dashboard", "quality compliance case"],
        "interview": ["Healthcare operations case", "Compliance scenario", "Patient safety discussion", "Leadership round"],
        "salary_ranges": {"India": ["3-7 LPA", "8-18 LPA", "20-45 LPA"]},
        "remote": "Low to Medium",
        "freelance": "Low",
        "startup": "Medium",
        "ai_impact": "AI improves triage, records, and operations, while healthcare judgment and compliance remain essential.",
    },
    "Law": {
        "required_skills": ["Legal Research", "Contract Drafting", "Case Analysis", "Compliance", "Legal Writing", "Negotiation"],
        "technical_skills": ["Contract Law", "Companies Act", "Evidence Law", "Due Diligence", "Legal Research Databases"],
        "tools": ["SCC Online", "Manupatra", "Westlaw", "LexisNexis", "Document review tools"],
        "software": ["Legal research databases", "case management systems", "document management tools"],
        "frameworks": [],
        "certifications": ["Contract Drafting", "Corporate Law", "Compliance", "Intellectual Property Law"],
        "books": ["Learning the Law", "Contract Law", "Legal Writing in Plain English"],
        "courses": ["NLSIU online law courses", "Coursera Legal Tech", "edX Contract Law"],
        "youtube_channels": ["LiveLaw", "Bar and Bench", "LegalEdge"],
        "communities": ["Bar association groups", "Moot court societies", "Legal research forums"],
        "professional_organizations": ["Bar Council", "International Bar Association", "Local bar associations"],
        "practice_platforms": ["Moot court competitions", "case brief libraries", "legal drafting exercises"],
        "companies": ["Khaitan & Co", "Cyril Amarchand Mangaldas", "Trilegal", "AZB", "Shardul Amarchand", "In-house legal teams"],
        "portfolio": ["case briefs", "contract review samples", "compliance memo"],
        "interview": ["Case law discussion", "Drafting test", "Scenario analysis", "Ethics round"],
        "salary_ranges": {"India": ["4-8 LPA", "10-22 LPA", "25-60 LPA"]},
        "remote": "Medium",
        "freelance": "Medium",
        "startup": "Medium",
        "ai_impact": "AI speeds research and first drafts, but legal reasoning, judgment, and advocacy remain central.",
    },
    "Business": {
        "required_skills": ["Business Communication", "Market Research", "Operations", "Stakeholder Management", "Presentation", "Decision Making"],
        "technical_skills": ["Business Analytics", "Process Mapping", "Excel", "CRM", "Project Management"],
        "tools": ["Excel", "PowerPoint", "CRM", "Notion", "Asana"],
        "software": ["CRM platforms", "ERP tools", "project management software"],
        "frameworks": ["SWOT", "OKRs", "Porter's Five Forces", "Lean"],
        "certifications": ["Google Project Management", "Six Sigma Yellow Belt", "Business Analytics Certificate"],
        "books": ["Good Strategy Bad Strategy", "Measure What Matters", "The Lean Startup"],
        "courses": ["Wharton Business Foundations", "Google Project Management", "IIM business courses"],
        "youtube_channels": ["Harvard Business Review", "Y Combinator", "Think School"],
        "communities": ["MBA clubs", "startup communities", "business analyst forums"],
        "professional_organizations": ["PMI", "AIMA", "Local chambers of commerce"],
        "practice_platforms": ["Forage", "case competitions", "business simulation platforms"],
        "companies": ["Deloitte", "PwC", "EY", "KPMG", "Accenture", "Tata Group"],
        "portfolio": ["business case study", "process improvement report", "market research deck"],
        "interview": ["Case interview", "Business scenario", "Stakeholder discussion", "Behavioral round"],
        "salary_ranges": {"India": ["4-9 LPA", "10-22 LPA", "25-55 LPA"]},
        "remote": "Medium",
        "freelance": "Medium",
        "startup": "High",
        "ai_impact": "AI helps analysis and writing; business judgment, communication, and execution still drive outcomes.",
    },
    "Finance": {
        "required_skills": ["Accounting", "Financial Modeling", "Valuation", "Risk Analysis", "Excel", "Financial Reporting"],
        "technical_skills": ["Financial Statements", "Forecasting", "Budgeting", "Taxation", "Power BI"],
        "tools": ["Excel", "Power BI", "Tally", "Bloomberg Terminal", "QuickBooks"],
        "software": ["Accounting software", "ERP finance modules", "financial terminals"],
        "frameworks": ["DCF", "Comparable Company Analysis", "Risk frameworks"],
        "certifications": ["CFA Level 1", "FMVA", "NISM", "ACCA Foundation"],
        "books": ["The Intelligent Investor", "Financial Statement Analysis", "Investment Banking"],
        "courses": ["CFA Institute resources", "Wall Street Prep", "Coursera Finance"],
        "youtube_channels": ["Aswath Damodaran", "Corporate Finance Institute", "Zerodha Varsity"],
        "communities": ["CFA Society", "finance clubs", "investment forums"],
        "professional_organizations": ["CFA Institute", "ICAI", "GARP"],
        "practice_platforms": ["Zerodha Varsity", "Forage finance cases", "stock pitch competitions"],
        "companies": ["JP Morgan", "Goldman Sachs", "HDFC Bank", "ICICI Bank", "Deloitte", "KPMG"],
        "portfolio": ["valuation report", "financial model", "equity research note"],
        "interview": ["Finance technical round", "Case analysis", "Excel/modeling task", "Market discussion"],
        "salary_ranges": {"India": ["4-8 LPA", "10-18 LPA", "22-45 LPA"]},
        "remote": "Medium",
        "freelance": "Medium",
        "startup": "Medium",
        "ai_impact": "AI automates reporting, so modeling, judgment, and business storytelling become more valuable.",
    },
    "Marketing": {
        "required_skills": ["Brand Strategy", "Consumer Research", "Content Strategy", "Campaign Analytics", "Copywriting", "SEO"],
        "technical_skills": ["Google Analytics", "Search Console", "Meta Ads", "Email Automation", "A/B Testing"],
        "tools": ["Google Analytics", "Google Ads", "Meta Ads", "Canva", "HubSpot"],
        "software": ["marketing automation tools", "analytics dashboards", "CRM platforms"],
        "frameworks": ["AIDA", "STP", "4Ps", "Growth funnel"],
        "certifications": ["Google Ads", "HubSpot Content Marketing", "Meta Blueprint"],
        "books": ["Contagious", "Building a StoryBrand", "Influence"],
        "courses": ["Google Digital Garage", "HubSpot Academy", "Coursera Marketing"],
        "youtube_channels": ["HubSpot Marketing", "Neil Patel", "Think with Google"],
        "communities": ["marketing communities", "growth marketing groups", "brand strategy forums"],
        "professional_organizations": ["American Marketing Association", "DMA", "local marketing clubs"],
        "practice_platforms": ["Google Skillshop", "HubSpot Academy", "campaign teardown libraries"],
        "companies": ["Ogilvy", "Dentsu", "WPP", "Nykaa", "Zomato", "HUL"],
        "portfolio": ["campaign case study", "SEO audit", "content calendar", "brand strategy deck"],
        "interview": ["Campaign critique", "Marketing case", "Portfolio review", "Behavioral round"],
        "salary_ranges": {"India": ["3-6 LPA", "8-16 LPA", "18-35 LPA"]},
        "remote": "High",
        "freelance": "High",
        "startup": "High",
        "ai_impact": "AI speeds content and research, while strategy, positioning, and creative judgment differentiate candidates.",
    },
    "Creative": {
        "required_skills": ["Visual Design", "Storytelling", "Portfolio Development", "Client Communication", "Creative Direction"],
        "technical_skills": ["Figma", "Adobe Creative Suite", "Canva", "Video Editing", "Typography"],
        "tools": ["Figma", "Photoshop", "Illustrator", "Premiere Pro", "Canva"],
        "software": ["Adobe Creative Cloud", "Figma", "Canva", "DaVinci Resolve"],
        "frameworks": ["Design Thinking", "Brand Systems", "User-centered design"],
        "certifications": ["Google UX Design", "Adobe Certified Professional", "Nielsen Norman UX"],
        "books": ["Don't Make Me Think", "Steal Like an Artist", "The Design of Everyday Things"],
        "courses": ["Google UX Design", "Domestika", "Coursera Graphic Design"],
        "youtube_channels": ["The Futur", "Flux Academy", "CharliMarieTV"],
        "communities": ["Behance", "Dribbble", "design communities"],
        "professional_organizations": ["AIGA", "Interaction Design Foundation", "local design groups"],
        "practice_platforms": ["Behance challenges", "Dribbble prompts", "design hackathons"],
        "companies": ["Adobe", "Canva", "WPP", "IDEO", "media agencies", "design studios"],
        "portfolio": ["case studies", "visual portfolio", "client/project outcomes"],
        "interview": ["Portfolio review", "Design critique", "Creative task", "Client scenario"],
        "salary_ranges": {"India": ["4-8 LPA", "10-18 LPA", "22-40 LPA"]},
        "remote": "High",
        "freelance": "High",
        "startup": "High",
        "ai_impact": "AI helps ideation and production, but taste, research, originality, and client communication remain decisive.",
    },
    "Education": {
        "required_skills": ["Lesson Planning", "Curriculum Design", "Assessment", "Classroom Management", "Student Counseling"],
        "technical_skills": ["Learning Management Systems", "Assessment Tools", "Educational Psychology", "Content Design"],
        "tools": ["Google Classroom", "Moodle", "Zoom", "Canva", "assessment tools"],
        "software": ["LMS platforms", "virtual classroom tools", "content authoring tools"],
        "frameworks": ["Bloom's Taxonomy", "Backward Design", "Formative Assessment"],
        "certifications": ["BEd", "TESOL", "Google Certified Educator", "Instructional Design"],
        "books": ["Teach Like a Champion", "Make It Stick", "Understanding by Design"],
        "courses": ["Google for Education", "Coursera Teaching", "edX Instructional Design"],
        "youtube_channels": ["Teaching Channel", "Khan Academy", "Edutopia"],
        "communities": ["teacher communities", "subject educator groups", "EdTech forums"],
        "professional_organizations": ["ISTE", "TESOL", "local teacher associations"],
        "practice_platforms": ["lesson plan repositories", "teaching demo reviews", "teacher training workshops"],
        "companies": ["schools", "universities", "Byju's", "Vedantu", "Khan Academy", "edtech companies"],
        "portfolio": ["lesson plans", "teaching demo", "assessment rubric", "student outcome evidence"],
        "interview": ["Teaching demo", "Pedagogy questions", "Classroom scenario", "Subject knowledge round"],
        "salary_ranges": {"India": ["2-5 LPA", "6-12 LPA", "15-30 LPA"]},
        "remote": "Medium",
        "freelance": "Medium",
        "startup": "Medium",
        "ai_impact": "AI supports lesson creation and assessment; teacher empathy and facilitation remain core.",
    },
    "Science": {
        "required_skills": ["Research Methods", "Literature Review", "Data Analysis", "Academic Writing", "Laboratory Techniques"],
        "technical_skills": ["Experiment Design", "Statistics", "Citation Management", "Lab Safety", "Scientific Reporting"],
        "tools": ["Zotero", "SPSS", "R", "lab equipment", "Google Scholar"],
        "software": ["citation tools", "statistical packages", "lab information systems"],
        "frameworks": ["Scientific Method", "Peer Review", "Research Ethics"],
        "certifications": ["Research Methods", "Biostatistics", "Lab Safety"],
        "books": ["The Craft of Research", "How to Read a Paper", "Statistics for Researchers"],
        "courses": ["Coursera Research Methods", "edX Statistics", "NPTEL science courses"],
        "youtube_channels": ["CrashCourse", "MIT OpenCourseWare", "Nature Video"],
        "communities": ["ResearchGate", "academic societies", "journal clubs"],
        "professional_organizations": ["discipline-specific scientific societies", "AAAS", "local research associations"],
        "practice_platforms": ["research poster contests", "paper replication projects", "lab workshops"],
        "companies": ["research labs", "universities", "pharma companies", "policy think tanks"],
        "portfolio": ["literature review", "research poster", "paper summary", "reproducible analysis"],
        "interview": ["Research discussion", "Methods round", "Literature critique", "Ethics scenario"],
        "salary_ranges": {"India": ["3-6 LPA", "7-14 LPA", "16-35 LPA"]},
        "remote": "Medium",
        "freelance": "Low to Medium",
        "startup": "Medium",
        "ai_impact": "AI accelerates literature review and analysis, while research design and validation remain human-led.",
    },
    "Hospitality": {
        "required_skills": ["Guest Relations", "Hotel Operations", "Food Safety", "Event Planning", "Service Quality"],
        "technical_skills": ["PMS Tools", "Revenue Management", "Housekeeping Operations", "F&B Operations"],
        "tools": ["property management systems", "POS systems", "booking platforms", "Excel"],
        "software": ["hotel PMS", "reservation systems", "guest feedback tools"],
        "frameworks": ["Service recovery", "Revenue management", "Guest journey mapping"],
        "certifications": ["Food Safety", "Hospitality Management", "Revenue Management"],
        "books": ["Setting the Table", "Hospitality Management", "The New Gold Standard"],
        "courses": ["Cornell hospitality courses", "Coursera Hospitality", "AHLEI certificates"],
        "youtube_channels": ["Hospitality Academy", "Cornell Hospitality", "service management channels"],
        "communities": ["hotel management groups", "tourism associations", "hospitality networks"],
        "professional_organizations": ["AHLEI", "HAMA", "local hotel associations"],
        "practice_platforms": ["guest service simulations", "event planning cases", "hotel operations case studies"],
        "companies": ["Taj Hotels", "Oberoi", "Marriott", "Hilton", "IHG", "Airbnb"],
        "portfolio": ["guest experience plan", "event operations plan", "service improvement case"],
        "interview": ["Guest scenario", "Operations discussion", "Service recovery case", "Behavioral round"],
        "salary_ranges": {"India": ["3-6 LPA", "7-14 LPA", "16-32 LPA"]},
        "remote": "Low",
        "freelance": "Medium",
        "startup": "Medium",
        "ai_impact": "AI helps booking and service analytics, but hospitality remains people and operations intensive.",
    },
    "Architecture": {
        "required_skills": ["Architectural Design", "AutoCAD", "Revit", "Building Codes", "Sustainable Design"],
        "technical_skills": ["BIM", "Construction Drawings", "Rendering", "Site Planning"],
        "tools": ["AutoCAD", "Revit", "SketchUp", "Lumion", "Rhino"],
        "software": ["BIM software", "rendering tools", "CAD platforms"],
        "frameworks": ["Design thinking", "green building principles", "building code compliance"],
        "certifications": ["Revit Architecture", "Green Building", "LEED basics"],
        "books": ["A Pattern Language", "Form Space and Order", "101 Things I Learned in Architecture School"],
        "courses": ["Autodesk learning", "Coursera architecture", "green building courses"],
        "youtube_channels": ["30X40 Design Workshop", "Show It Better", "Architecture Hunter"],
        "communities": ["architecture forums", "design studios", "urban planning groups"],
        "professional_organizations": ["Council of Architecture", "RIBA", "AIA"],
        "practice_platforms": ["architecture competitions", "design charrettes", "portfolio reviews"],
        "companies": ["architecture studios", "AECOM", "Gensler", "HOK", "L&T Construction"],
        "portfolio": ["design portfolio", "BIM model", "site analysis", "sustainable design concept"],
        "interview": ["Portfolio review", "design critique", "technical drawing discussion", "client scenario"],
        "salary_ranges": {"India": ["3-7 LPA", "8-18 LPA", "20-45 LPA"]},
        "remote": "Medium",
        "freelance": "High",
        "startup": "Medium",
        "ai_impact": "AI and generative design speed concepts; code knowledge, context, and client fit remain crucial.",
    },
    "Agriculture": {
        "required_skills": ["Crop Science", "Soil Science", "Agri Business", "Sustainability", "Supply Chain"],
        "technical_skills": ["Precision Agriculture", "Food Technology", "Irrigation", "Commodity Analysis"],
        "tools": ["GIS tools", "soil testing kits", "farm management software", "Excel"],
        "software": ["farm management platforms", "GIS systems", "supply-chain tools"],
        "frameworks": ["sustainable agriculture", "value chain analysis", "food safety standards"],
        "certifications": ["Agri Business", "Food Safety", "Supply Chain Analytics"],
        "books": ["Agribusiness Management", "Soil Science", "Sustainable Agriculture"],
        "courses": ["NPTEL agriculture", "FAO learning", "Coursera sustainability"],
        "youtube_channels": ["FAO", "ICAR", "agriculture extension channels"],
        "communities": ["farmer producer networks", "agritech communities", "sustainability groups"],
        "professional_organizations": ["ICAR", "FAO", "agriculture universities"],
        "practice_platforms": ["field projects", "agritech case studies", "sustainability competitions"],
        "companies": ["UPL", "ITC Agri", "Mahindra Agri", "Ninjacart", "DeHaat"],
        "portfolio": ["crop advisory report", "supply-chain analysis", "sustainability project"],
        "interview": ["field case", "market linkage discussion", "technical agriculture round", "operations round"],
        "salary_ranges": {"India": ["3-6 LPA", "7-15 LPA", "18-35 LPA"]},
        "remote": "Low to Medium",
        "freelance": "Medium",
        "startup": "High",
        "ai_impact": "AI improves forecasting and precision agriculture; field knowledge and trust remain essential.",
    },
    "Government": {
        "required_skills": ["Current Affairs", "Policy Analysis", "Essay Writing", "Reasoning", "Ethics"],
        "technical_skills": ["Governance", "Economics", "Data Interpretation", "Constitution", "Public Administration"],
        "tools": ["newspapers", "government reports", "answer writing notebooks", "mock test platforms"],
        "software": ["exam prep platforms", "document readers", "note-taking tools"],
        "frameworks": ["policy cycle", "constitutional governance", "public administration frameworks"],
        "certifications": ["Public Policy", "Governance", "Constitution studies"],
        "books": ["Indian Polity", "Indian Economy", "Ethics Integrity and Aptitude"],
        "courses": ["public policy courses", "UPSC foundation", "governance courses"],
        "youtube_channels": ["PRS India", "Rajya Sabha TV", "study channels"],
        "communities": ["civil services study groups", "public policy forums", "debate societies"],
        "professional_organizations": ["government bodies", "policy think tanks", "civil service associations"],
        "practice_platforms": ["mock tests", "answer writing platforms", "essay competitions"],
        "companies": ["government departments", "PSUs", "policy think tanks", "international development organizations"],
        "portfolio": ["policy brief", "essay samples", "mock test tracker", "public project analysis"],
        "interview": ["personality test", "current affairs discussion", "ethics scenario", "policy analysis"],
        "salary_ranges": {"India": ["structured pay", "structured pay", "structured pay"]},
        "remote": "Low",
        "freelance": "Low",
        "startup": "Low",
        "ai_impact": "AI helps revision and information synthesis; judgment, writing, and ethics remain decisive.",
    },
    "Entrepreneurship": {
        "required_skills": ["Customer Discovery", "Sales", "Business Model Design", "Financial Planning", "Pitching"],
        "technical_skills": ["Market Validation", "Unit Economics", "Growth Strategy", "Operations"],
        "tools": ["Notion", "Canva", "CRM", "payment tools", "analytics tools"],
        "software": ["no-code tools", "CRM platforms", "analytics dashboards"],
        "frameworks": ["Lean Startup", "Business Model Canvas", "Jobs To Be Done"],
        "certifications": ["Startup school", "Digital business", "Product management"],
        "books": ["The Lean Startup", "Zero to One", "The Mom Test"],
        "courses": ["Y Combinator Startup School", "IIM entrepreneurship", "Coursera entrepreneurship"],
        "youtube_channels": ["Y Combinator", "Lenny's Podcast", "Harvard i-lab"],
        "communities": ["startup communities", "founder groups", "local incubators"],
        "professional_organizations": ["incubators", "accelerators", "startup networks"],
        "practice_platforms": ["pitch competitions", "startup weekends", "customer interview sprints"],
        "companies": ["own venture", "startup studios", "incubators", "freelance marketplaces"],
        "portfolio": ["MVP", "customer interviews", "pitch deck", "revenue experiment"],
        "interview": ["investor pitch", "customer insight discussion", "business model review", "execution story"],
        "salary_ranges": {"India": ["variable", "variable", "variable"]},
        "remote": "High",
        "freelance": "High",
        "startup": "Very High",
        "ai_impact": "AI lowers execution costs, so customer insight, speed, and distribution become stronger advantages.",
    },
}


PROFESSION_SEEDS: dict[str, list[str]] = {
    "Technology": [
        "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Mobile App Developer",
        "DevOps Engineer", "Cloud Engineer", "Cybersecurity Analyst", "Cybersecurity Engineer", "Data Engineer",
        "Database Administrator", "Site Reliability Engineer", "QA Engineer", "Automation Tester", "UI Developer",
        "Game Developer", "Blockchain Developer", "AR VR Developer", "Computer Vision Engineer", "NLP Engineer",
        "AI Product Manager", "Technical Program Manager", "Solutions Architect", "IT Support Specialist", "Network Engineer",
    ],
    "Engineering": [
        "Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Electronics Engineer", "Chemical Engineer",
        "Aerospace Engineer", "Automobile Engineer", "Robotics Engineer", "Industrial Engineer", "Manufacturing Engineer",
        "Production Engineer", "Quality Engineer", "Instrumentation Engineer", "Mechatronics Engineer", "Marine Engineer",
        "Petroleum Engineer", "Environmental Engineer", "Structural Engineer", "Construction Manager", "HVAC Engineer",
    ],
    "Business": [
        "Business Analyst", "Product Manager", "Operations Manager", "Supply Chain Manager", "Management Consultant",
        "Project Manager", "Sales Manager", "Account Manager", "Customer Success Manager", "Retail Manager",
        "Business Development Executive", "Strategy Analyst", "Operations Analyst", "Procurement Manager", "Logistics Manager",
        "HR Manager", "Recruiter", "Talent Acquisition Specialist", "Learning and Development Manager", "Training Manager",
    ],
    "Finance": [
        "Finance Analyst", "Accountant", "Investment Banker", "Equity Research Analyst", "Credit Analyst",
        "Risk Analyst", "Tax Consultant", "Auditor", "Financial Planner", "Wealth Manager",
        "Bank Manager", "Insurance Advisor", "Actuary", "Treasury Analyst", "Portfolio Manager",
        "Compliance Analyst", "Loan Officer", "Cost Accountant", "Forensic Accountant", "Payroll Specialist",
    ],
    "Marketing": [
        "Digital Marketer", "SEO Specialist", "Content Marketer", "Brand Manager", "Social Media Manager",
        "Performance Marketer", "Email Marketing Specialist", "Marketing Analyst", "Copywriter", "Public Relations Specialist",
        "Growth Marketer", "Market Research Analyst", "Influencer Marketing Manager", "Community Manager", "CRM Marketing Manager",
    ],
    "Law": [
        "Corporate Lawyer", "Criminal Lawyer", "Civil Lawyer", "Cyber Lawyer", "Legal Advisor",
        "Legal Researcher", "Judge", "Intellectual Property Lawyer", "Tax Lawyer", "Family Lawyer",
        "Human Rights Lawyer", "Compliance Officer", "Contract Manager", "Paralegal", "Legal Journalist",
    ],
    "Healthcare": [
        "Doctor", "Nurse", "Healthcare Administrator", "Hospital Manager", "Pharmacist",
        "Dentist", "Public Health Specialist", "Physiotherapist", "Radiologist", "Medical Laboratory Technologist",
        "Clinical Research Associate", "Nutritionist", "Mental Health Counselor", "Occupational Therapist", "Healthcare Quality Manager",
    ],
    "Science": [
        "Research Assistant", "Biologist", "Chemist", "Physicist", "Mathematician",
        "Statistician", "Biotechnologist", "Environmental Scientist", "Food Scientist", "Lab Technician",
        "Data Researcher", "Clinical Researcher", "Geologist", "Astronomer", "Research Scientist",
    ],
    "Creative": [
        "UX Designer", "Graphic Designer", "Animator", "Film Director", "Video Editor",
        "Photographer", "Journalist", "Content Creator", "Fashion Designer", "Game Designer",
        "Art Director", "Illustrator", "Motion Graphics Designer", "Creative Writer", "Media Planner",
    ],
    "Education": [
        "Teacher", "Professor", "Instructional Designer", "Academic Counselor", "School Principal",
        "Curriculum Developer", "Special Education Teacher", "Corporate Trainer", "Language Trainer", "Online Tutor",
        "Education Consultant", "Research Scholar", "Librarian", "Education Administrator", "Exam Coordinator",
    ],
    "Hospitality": [
        "Hotel Manager", "Restaurant Manager", "Event Manager", "Travel Consultant", "Chef",
        "Front Office Manager", "Food and Beverage Manager", "Housekeeping Manager", "Tourism Manager", "Airline Cabin Crew",
    ],
    "Architecture": [
        "Architect", "Urban Planner", "Interior Designer", "Landscape Architect", "BIM Specialist",
        "Architectural Visualizer", "Construction Planner", "Sustainable Design Consultant", "Real Estate Developer", "Quantity Surveyor",
    ],
    "Agriculture": [
        "Agri Business Analyst", "Agronomist", "Food Technologist", "Dairy Technologist", "Horticulturist",
        "Soil Scientist", "Farm Manager", "Agricultural Officer", "Fisheries Officer", "Sustainability Analyst",
    ],
    "Government": [
        "Civil Services Aspirant", "Policy Analyst", "Public Administrator", "Defense Officer", "Police Officer",
        "Public Sector Banker", "Railway Officer", "Municipal Officer", "Development Officer", "Diplomat",
    ],
    "Entrepreneurship": [
        "Entrepreneur", "Freelancer", "Startup Founder", "Small Business Owner", "Independent Consultant",
        "Creator Entrepreneur", "E-commerce Seller", "Agency Owner", "Social Entrepreneur", "Franchise Owner",
    ],
}


ROLE_FAMILIES: dict[str, list[str]] = {
    "Technology": [
        "Software Engineer", "Backend Engineer", "Frontend Engineer", "Full Stack Engineer", "Mobile Engineer",
        "Android Developer", "iOS Developer", "Flutter Developer", "React Developer", "Python Developer",
        "Java Developer", "Node.js Developer", "Platform Engineer", "DevOps Engineer", "Site Reliability Engineer",
        "Cloud Engineer", "Cloud Architect", "Data Engineer", "Machine Learning Engineer", "AI Engineer",
        "NLP Engineer", "Computer Vision Engineer", "MLOps Engineer", "Data Scientist", "Data Analyst",
        "Business Intelligence Analyst", "Analytics Engineer", "Cybersecurity Analyst", "Security Engineer",
        "SOC Analyst", "Penetration Tester", "Security Architect", "QA Engineer", "Automation Test Engineer",
        "Manual Tester", "Release Engineer", "Embedded Systems Engineer", "Firmware Engineer", "IoT Engineer",
        "Blockchain Developer", "Smart Contract Developer", "Game Developer", "Unity Developer", "Unreal Developer",
        "UI UX Designer", "Product Designer", "UX Researcher", "Technical Program Manager", "Solutions Architect",
    ],
    "Finance": [
        "Accountant", "Financial Analyst", "Finance Analyst", "Chartered Accountant", "Audit Associate",
        "Internal Auditor", "Tax Consultant", "Finance Manager", "Finance Controller", "Treasury Analyst",
        "Corporate Finance Manager", "Risk Analyst", "Investment Analyst", "Portfolio Manager", "Equity Research Analyst",
        "Credit Analyst", "FP&A Analyst", "Financial Planning Analyst", "Cost Accountant", "Forensic Accountant",
        "Payroll Specialist", "Banking Analyst", "Insurance Analyst", "Wealth Manager", "Fund Manager",
        "Compliance Analyst", "Loan Officer", "Branch Manager", "Accounts Payable Specialist", "Accounts Receivable Specialist",
    ],
    "Business": [
        "Business Analyst", "Operations Executive", "Operations Manager", "Product Manager", "Program Manager",
        "Project Manager", "Strategy Consultant", "Management Consultant", "Business Development Manager",
        "Sales Executive", "Sales Manager", "Account Manager", "Customer Success Manager", "Retail Manager",
        "Procurement Manager", "Logistics Manager", "Supply Chain Analyst", "Supply Chain Manager", "Process Analyst",
        "Business Operations Manager", "Vendor Manager", "Partnerships Manager", "Chief of Staff", "General Manager",
    ],
    "Marketing": [
        "Marketing Executive", "Digital Marketing Executive", "SEO Specialist", "SEM Specialist", "Content Strategist",
        "Social Media Manager", "Performance Marketing Manager", "Brand Manager", "Growth Manager", "Marketing Manager",
        "Content Marketing Manager", "Email Marketing Specialist", "CRM Marketing Manager", "Public Relations Specialist",
        "Market Research Analyst", "Marketing Analyst", "Influencer Marketing Manager", "Community Manager",
        "Copywriter", "Creative Strategist",
    ],
    "Business HR": [
        "HR Executive", "Recruiter", "Technical Recruiter", "Talent Acquisition Specialist", "HR Business Partner",
        "HR Manager", "Learning and Development Manager", "Compensation and Benefits Manager", "Employee Relations Manager",
        "People Operations Manager", "HR Generalist", "Training Manager", "Organizational Development Specialist",
    ],
    "Healthcare": [
        "Nurse", "Medical Officer", "Resident Doctor", "Specialist Doctor", "Consultant Doctor", "Surgeon",
        "Radiologist", "Pharmacist", "Physiotherapist", "Hospital Administrator", "Medical Director", "Dentist",
        "Public Health Specialist", "Clinical Research Associate", "Medical Laboratory Technologist", "Nutritionist",
        "Mental Health Counselor", "Occupational Therapist", "Healthcare Quality Manager", "Healthcare Operations Manager",
        "Medical Records Manager", "Clinical Coordinator", "Biostatistician", "Healthcare Data Analyst",
    ],
    "Education": [
        "Teacher", "Senior Teacher", "Lecturer", "Assistant Professor", "Associate Professor", "Professor",
        "Academic Coordinator", "Principal", "Dean", "Instructional Designer", "Curriculum Developer",
        "Education Consultant", "School Counselor", "Special Education Teacher", "Corporate Trainer", "Online Tutor",
        "Language Trainer", "Research Scholar", "Librarian", "Exam Coordinator",
    ],
    "Law": [
        "Legal Associate", "Senior Associate", "Legal Counsel", "Corporate Lawyer", "Legal Manager", "Partner",
        "Criminal Lawyer", "Civil Lawyer", "Cyber Lawyer", "Legal Advisor", "Legal Researcher", "Judge",
        "Intellectual Property Lawyer", "Tax Lawyer", "Family Lawyer", "Human Rights Lawyer", "Compliance Officer",
        "Contract Manager", "Paralegal", "Legal Journalist",
    ],
    "Engineering": [
        "Civil Engineer", "Mechanical Engineer", "Electrical Engineer", "Electronics Engineer", "Chemical Engineer",
        "Aerospace Engineer", "Industrial Engineer", "Automotive Engineer", "Manufacturing Engineer", "Production Engineer",
        "Quality Engineer", "Instrumentation Engineer", "Robotics Engineer", "Mechatronics Engineer", "Marine Engineer",
        "Petroleum Engineer", "Environmental Engineer", "Structural Engineer", "Construction Manager", "HVAC Engineer",
        "Process Engineer", "Plant Engineer", "Maintenance Engineer", "Design Engineer", "Safety Engineer",
    ],
    "Hospitality": [
        "Hotel Manager", "Restaurant Manager", "Event Manager", "Travel Consultant", "Chef", "Front Office Manager",
        "Food and Beverage Manager", "Housekeeping Manager", "Tourism Manager", "Airline Cabin Crew", "Resort Manager",
        "Guest Relations Manager", "Catering Manager", "Revenue Manager", "Hospitality Operations Manager",
    ],
    "Creative": [
        "Journalist", "Editor", "News Anchor", "Film Director", "Video Editor", "Photographer", "Graphic Designer",
        "Animator", "Motion Graphics Designer", "Game Designer", "Fashion Designer", "Interior Designer", "Art Director",
        "Creative Director", "Illustrator", "Content Creator", "Media Planner", "Screenwriter", "Producer", "Sound Designer",
    ],
    "Architecture": [
        "Architect", "Urban Planner", "Interior Designer", "Landscape Architect", "BIM Specialist",
        "Architectural Visualizer", "Construction Planner", "Sustainable Design Consultant", "Real Estate Developer",
        "Quantity Surveyor", "Site Architect", "Project Architect",
    ],
    "Agriculture": [
        "Agronomist", "Agri Business Analyst", "Food Technologist", "Dairy Technologist", "Horticulturist",
        "Soil Scientist", "Farm Manager", "Agricultural Officer", "Fisheries Officer", "Sustainability Analyst",
        "Agricultural Economist", "Seed Technologist", "Agri Supply Chain Manager",
    ],
    "Government": [
        "Civil Services Officer", "Policy Analyst", "Public Administrator", "Defense Officer", "Police Officer",
        "Public Sector Banker", "Railway Officer", "Municipal Officer", "Development Officer", "Diplomat",
        "Public Relations Officer", "Tax Officer", "Customs Officer", "Administrative Officer",
    ],
    "Science": [
        "Research Assistant", "Research Scientist", "Biologist", "Chemist", "Physicist", "Mathematician", "Statistician",
        "Biotechnologist", "Environmental Scientist", "Food Scientist", "Lab Technician", "Clinical Researcher",
        "Geologist", "Astronomer", "Psychologist", "Social Worker", "Research Analyst", "Policy Researcher",
    ],
    "Entrepreneurship": [
        "Entrepreneur", "Freelancer", "Startup Founder", "Small Business Owner", "Independent Consultant",
        "Creator Entrepreneur", "E-commerce Seller", "Agency Owner", "Social Entrepreneur", "Franchise Owner",
    ],
    "Aviation": [
        "Pilot", "Commercial Pilot", "Air Traffic Controller", "Aircraft Maintenance Engineer", "Avionics Technician",
        "Flight Dispatcher", "Airport Operations Manager", "Ground Staff Supervisor", "Aviation Safety Officer",
        "Cabin Crew Trainer", "Aviation Security Officer", "Airline Operations Analyst", "Flight Operations Manager",
        "Aviation Quality Manager", "Airport Planner", "Cargo Operations Manager", "Ramp Manager", "Crew Scheduler",
    ],
    "Marine": [
        "Marine Engineer", "Deck Officer", "Ship Captain", "Port Operations Manager", "Naval Architect",
        "Marine Surveyor", "Shipping Operations Executive", "Logistics Coordinator", "Dredging Engineer",
        "Marine Safety Officer", "Offshore Operations Manager", "Marine Superintendent", "Port Planner",
        "Ship Broker", "Maritime Lawyer", "Fleet Manager",
    ],
    "Energy": [
        "Energy Analyst", "Renewable Energy Engineer", "Solar Project Engineer", "Wind Energy Engineer",
        "Power Plant Engineer", "Grid Operations Engineer", "Energy Trader", "Battery Systems Engineer",
        "Sustainability Consultant", "Energy Auditor", "Electrical Grid Planner", "Hydrogen Energy Specialist",
        "Oil and Gas Engineer", "Drilling Engineer", "Reservoir Engineer", "Energy Policy Analyst",
    ],
    "Mining": [
        "Mining Engineer", "Mine Planner", "Geotechnical Engineer", "Exploration Geologist", "Mine Safety Officer",
        "Mineral Processing Engineer", "Drilling Supervisor", "Quarry Manager", "Metallurgist", "Survey Engineer",
        "Mining Operations Manager", "Environmental Compliance Officer",
    ],
    "Telecommunications": [
        "Telecom Engineer", "RF Engineer", "Network Planning Engineer", "5G Engineer", "Fiber Optic Technician",
        "NOC Engineer", "Telecom Project Manager", "Satellite Communications Engineer", "Microwave Engineer",
        "OSS BSS Analyst", "Telecom Sales Engineer", "Network Optimization Engineer",
    ],
    "Pharmaceuticals": [
        "Pharmaceutical Scientist", "Clinical Research Associate", "Regulatory Affairs Specialist", "Quality Assurance Pharmacist",
        "Quality Control Analyst", "Drug Safety Associate", "Medical Writer", "Pharmacovigilance Specialist",
        "Formulation Scientist", "Production Chemist", "Validation Engineer", "Regulatory Affairs Manager",
        "Clinical Trial Manager", "Medical Science Liaison",
    ],
    "Veterinary": [
        "Veterinarian", "Veterinary Surgeon", "Animal Nutritionist", "Veterinary Pharmacist", "Livestock Officer",
        "Animal Health Inspector", "Wildlife Veterinarian", "Veterinary Pathologist", "Dairy Farm Consultant",
        "Pet Care Manager",
    ],
    "Sports": [
        "Sports Coach", "Fitness Trainer", "Sports Analyst", "Sports Physiotherapist", "Athletic Trainer",
        "Sports Psychologist", "Sports Event Manager", "Sports Marketing Manager", "Club Manager",
        "Talent Scout", "Strength and Conditioning Coach", "Esports Manager",
    ],
    "International Relations": [
        "International Relations Analyst", "Diplomat", "Foreign Policy Analyst", "Political Risk Analyst",
        "Trade Policy Analyst", "Development Consultant", "Humanitarian Program Manager", "UN Program Officer",
        "International Partnerships Manager", "Geopolitical Analyst",
    ],
    "Aerospace": [
        "Aerospace Engineer", "Flight Test Engineer", "Propulsion Engineer", "Aircraft Design Engineer",
        "Satellite Systems Engineer", "Space Mission Analyst", "Avionics Engineer", "Aerospace Quality Engineer",
        "Aerodynamics Engineer", "Orbital Mechanics Analyst", "Launch Operations Engineer", "Aerospace Program Manager",
    ],
    "Defence": [
        "Defence Analyst", "Defence Engineer", "Weapons Systems Engineer", "Military Operations Analyst",
        "Cyber Defence Analyst", "Defence Procurement Specialist", "Radar Systems Engineer", "Naval Systems Engineer",
        "Aerospace Defence Engineer", "Defence Research Scientist", "Security Intelligence Analyst", "Defence Project Manager",
    ],
    "Biotechnology": [
        "Biotechnology Researcher", "Molecular Biologist", "Genomics Analyst", "Bioinformatics Scientist",
        "Bioprocess Engineer", "Cell Culture Scientist", "Clinical Data Scientist", "Biomedical Research Associate",
        "Genetic Counselor", "Biotech Quality Analyst", "Regulatory Biotech Specialist", "Biomanufacturing Specialist",
    ],
    "Logistics": [
        "Logistics Coordinator", "Warehouse Manager", "Transportation Manager", "Distribution Manager",
        "Fleet Manager", "Logistics Analyst", "Last Mile Operations Manager", "Freight Forwarding Executive",
        "Import Export Executive", "Inventory Controller", "Cold Chain Manager", "Logistics Technology Analyst",
    ],
    "Supply Chain": [
        "Supply Chain Analyst", "Supply Chain Manager", "Demand Planner", "Procurement Analyst",
        "Sourcing Manager", "Materials Planner", "Inventory Planner", "Vendor Development Manager",
        "Supply Chain Consultant", "Global Trade Specialist", "Category Manager", "Supply Chain Risk Analyst",
    ],
    "Manufacturing": [
        "Manufacturing Engineer", "Production Supervisor", "Plant Manager", "Lean Manufacturing Specialist",
        "Quality Control Engineer", "Quality Assurance Manager", "Industrial Automation Engineer", "CNC Programmer",
        "Process Improvement Engineer", "Maintenance Planner", "Factory Operations Manager", "Manufacturing Excellence Manager",
    ],
    "Renewable Energy": [
        "Solar Energy Engineer", "Wind Energy Engineer", "Renewable Energy Analyst", "Battery Storage Engineer",
        "Green Hydrogen Engineer", "Energy Storage Consultant", "Solar Plant Manager", "Wind Farm Operations Manager",
        "Renewable Project Developer", "Carbon Markets Analyst", "Sustainability Engineer", "Clean Energy Policy Analyst",
    ],
    "Construction": [
        "Construction Project Manager", "Site Engineer", "Construction Supervisor", "Planning Engineer",
        "Contracts Manager", "MEP Engineer", "Safety Manager", "Estimation Engineer",
        "Building Services Engineer", "Construction Quality Manager", "Infrastructure Project Manager", "Real Estate Project Manager",
    ],
    "Cybersecurity": [
        "Cybersecurity Analyst", "Security Engineer", "SOC Analyst", "Penetration Tester",
        "Threat Intelligence Analyst", "Application Security Engineer", "Cloud Security Engineer", "Identity Access Manager",
        "Incident Response Analyst", "Digital Forensics Analyst", "Security Consultant", "GRC Analyst",
    ],
    "Cloud Computing": [
        "Cloud Engineer", "Cloud Architect", "AWS Engineer", "Azure Engineer", "Google Cloud Engineer",
        "Cloud DevOps Engineer", "Cloud Network Engineer", "Cloud Security Engineer", "Kubernetes Engineer",
        "Cloud Migration Consultant", "FinOps Analyst", "Cloud Operations Manager",
    ],
    "Artificial Intelligence": [
        "AI Engineer", "Machine Learning Engineer", "NLP Engineer", "Computer Vision Engineer",
        "Generative AI Engineer", "LLM Engineer", "AI Product Manager", "AI Research Scientist",
        "MLOps Engineer", "Prompt Engineer", "AI Ethics Specialist", "AI Solutions Architect",
    ],
    "Robotics": [
        "Robotics Engineer", "Automation Engineer", "Controls Engineer", "Robot Programmer",
        "Autonomous Systems Engineer", "ROS Developer", "Mechatronics Engineer", "Industrial Robotics Engineer",
        "Drone Systems Engineer", "Robotics Researcher", "Human Robot Interaction Designer", "Robotics Technician",
    ],
    "Research": [
        "Research Scientist", "Research Associate", "Research Analyst", "Policy Researcher",
        "Market Researcher", "Academic Researcher", "Laboratory Researcher", "Field Research Coordinator",
        "Data Researcher", "Clinical Researcher", "Research Program Manager", "Grant Proposal Specialist",
    ],
    "Public Administration": [
        "Public Administrator", "Policy Analyst", "Urban Governance Specialist", "Municipal Commissioner",
        "Public Finance Analyst", "Development Officer", "Government Program Manager", "Administrative Officer",
        "Public Policy Consultant", "Regulatory Affairs Officer", "Social Impact Manager", "Civic Innovation Manager",
    ],
    "Fashion": [
        "Fashion Designer", "Textile Designer", "Fashion Merchandiser", "Fashion Buyer",
        "Apparel Production Manager", "Fashion Stylist", "Luxury Brand Manager", "Pattern Maker",
        "Garment Technologist", "Fashion Marketing Manager", "Visual Merchandiser", "Sustainable Fashion Consultant",
    ],
    "Tourism": [
        "Tourism Manager", "Travel Consultant", "Tour Operations Manager", "Destination Marketing Manager",
        "Tour Guide", "Travel Product Manager", "MICE Manager", "Heritage Tourism Consultant",
        "Adventure Tourism Manager", "Travel Technology Specialist", "Visa Consultant", "Travel Experience Designer",
    ],
    "Media": [
        "Journalist", "News Producer", "Broadcast Producer", "Media Planner", "Digital Editor",
        "Content Producer", "Podcast Producer", "Copy Editor", "Public Relations Manager",
        "Communications Specialist", "Social Media Producer", "Media Research Analyst",
    ],
    "Entertainment": [
        "Film Producer", "Line Producer", "Screenwriter", "Casting Director", "Music Producer",
        "Sound Engineer", "Video Producer", "OTT Content Manager", "Talent Manager",
        "Event Producer", "Entertainment Lawyer", "Post Production Supervisor",
    ],
    "Interior Design": [
        "Interior Designer", "Interior Architect", "Space Planner", "Furniture Designer",
        "Lighting Designer", "Retail Space Designer", "Exhibition Designer", "Set Designer",
        "Kitchen Designer", "Residential Interior Consultant", "Commercial Interior Designer", "Design Project Manager",
    ],
    "Environmental Science": [
        "Environmental Scientist", "Environmental Consultant", "Climate Analyst", "ESG Analyst",
        "Sustainability Consultant", "Waste Management Specialist", "Water Resource Specialist", "Air Quality Analyst",
        "Environmental Compliance Officer", "Conservation Scientist", "Carbon Accounting Analyst", "Environmental Impact Assessor",
    ],
    "Food Technology": [
        "Food Technologist", "Food Safety Officer", "Food Quality Analyst", "Product Development Scientist",
        "Food Microbiologist", "Dairy Technologist", "Nutrition Scientist", "Food Processing Engineer",
        "Sensory Analyst", "Beverage Technologist", "Food Regulatory Specialist", "Packaging Technologist",
    ],
    "Banking": [
        "Banking Analyst", "Relationship Manager", "Credit Manager", "Branch Manager",
        "Loan Officer", "Treasury Dealer", "Retail Banking Manager", "Corporate Banking Manager",
        "Risk Manager", "KYC Analyst", "Trade Finance Specialist", "Investment Banking Analyst",
    ],
    "Insurance": [
        "Insurance Analyst", "Actuarial Analyst", "Claims Manager", "Underwriter",
        "Insurance Sales Manager", "Risk Surveyor", "Reinsurance Analyst", "Policy Servicing Manager",
        "Insurance Operations Manager", "Health Insurance Specialist", "Motor Claims Specialist", "Insurance Product Manager",
    ],
    "Retail": [
        "Retail Manager", "Store Manager", "Category Manager", "Merchandising Manager",
        "E-commerce Manager", "Retail Operations Manager", "Visual Merchandiser", "Customer Experience Manager",
        "Inventory Manager", "Retail Buyer", "Omnichannel Manager", "Retail Analytics Manager",
    ],
    "Real Estate": [
        "Real Estate Analyst", "Property Manager", "Real Estate Developer", "Leasing Manager",
        "Facilities Manager", "Real Estate Consultant", "Valuation Analyst", "Land Acquisition Manager",
        "Asset Manager", "Brokerage Manager", "Property Sales Manager", "Real Estate Portfolio Manager",
    ],
}


SENIORITY_PREFIXES = [
    "",
    "Junior",
    "Associate",
    "Senior",
    "Lead",
    "Principal",
    "Staff",
]


EXECUTIVE_ROLES = {
    "Technology": ["Engineering Manager", "Director of Engineering", "VP Engineering", "Chief Technology Officer", "Chief Information Officer"],
    "Finance": ["Audit Manager", "Finance Manager", "Finance Controller", "Finance Director", "Chief Financial Officer"],
    "Business": ["Operations Director", "Business Unit Head", "VP Operations", "Chief Operating Officer"],
    "Marketing": ["Senior Marketing Manager", "Head of Marketing", "Marketing Director", "Chief Marketing Officer"],
    "Business HR": ["Head of HR", "HR Director", "VP People", "Chief Human Resources Officer"],
    "Healthcare": ["Hospital Manager", "Medical Director", "Healthcare Operations Director", "Chief Medical Officer"],
    "Education": ["Academic Coordinator", "Principal", "Dean", "Director of Education"],
    "Law": ["Legal Manager", "Partner", "General Counsel", "Chief Legal Officer"],
    "Engineering": ["Engineering Manager", "Plant Head", "Director of Engineering", "VP Engineering"],
}


@dataclass(frozen=True)
class CareerRecommendation:
    career: str
    domain: str
    fit_score: int
    explanation: str
    matched_signals: list[str]


def career_skill_terms() -> list[str]:
    terms: set[str] = set()
    for values in SKILLS_BY_DOMAIN.values():
        terms.update(values)
    for profile in DOMAIN_PROFILES.values():
        terms.update(profile.get("required_skills", []))
        terms.update(profile.get("technical_skills", []))
        terms.update(profile.get("tools", []))
        terms.update(profile.get("software", []))
    for career in CAREER_TEMPLATES.values():
        terms.update(career.get("required_skills", []))
        terms.update(career.get("technical_skills", []))
        terms.update(career.get("soft_skills", []))
    return sorted(terms, key=lambda value: (-len(value), value.casefold()))


def get_career_catalog() -> dict[str, dict[str, Any]]:
    catalog = {}
    for domain, names in PROFESSION_SEEDS.items():
        for name in names:
            catalog[name] = generate_profession_profile(name, domain)
    for domain, names in ROLE_FAMILIES.items():
        profile_domain = canonical_domain(domain)
        for name in expanded_role_names(domain, names):
            catalog.setdefault(name, generate_profession_profile(name, profile_domain))
    for name, career in CAREER_TEMPLATES.items():
        base = generate_profession_profile(name, career.get("domain", infer_domain_from_text(name)))
        catalog[name] = enrich_career(name, {**base, **career})
    return catalog


def canonical_domain(domain: str) -> str:
    """Map sub-industries to the reusable domain profiles already used by the app."""
    return {
        "Business HR": "Business",
        "Aviation": "Engineering",
        "Marine": "Engineering",
        "Energy": "Engineering",
        "Mining": "Engineering",
        "Telecommunications": "Technology",
        "Pharmaceuticals": "Healthcare",
        "Veterinary": "Healthcare",
        "Sports": "Business",
        "International Relations": "Government",
        "Aerospace": "Engineering",
        "Defence": "Government",
        "Biotechnology": "Healthcare",
        "Logistics": "Business",
        "Supply Chain": "Business",
        "Manufacturing": "Engineering",
        "Renewable Energy": "Engineering",
        "Construction": "Engineering",
        "Cybersecurity": "Technology",
        "Cloud Computing": "Technology",
        "Artificial Intelligence": "Technology",
        "Robotics": "Engineering",
        "Research": "Science",
        "Public Administration": "Government",
        "Fashion": "Creative",
        "Tourism": "Hospitality",
        "Media": "Creative",
        "Entertainment": "Creative",
        "Interior Design": "Architecture",
        "Environmental Science": "Science",
        "Food Technology": "Agriculture",
        "Banking": "Finance",
        "Insurance": "Finance",
        "Retail": "Business",
        "Real Estate": "Architecture",
    }.get(domain, domain)


def expanded_role_names(domain: str, base_roles: list[str]) -> list[str]:
    """Create seniority and leadership variants while preserving existing exact role names."""
    roles: list[str] = []
    prefixes = seniority_prefixes_for_domain(domain)
    for base_role in base_roles:
        roles.append(base_role)
        for prefix in prefixes:
            if not prefix:
                continue
            if base_role.casefold().startswith(prefix.casefold() + " "):
                continue
            if prefix == "Head of":
                roles.append(f"Head of {strip_seniority(base_role)}")
            elif prefix in {"Manager", "Senior Manager", "Director"} and any(term in base_role for term in ["Manager", "Director", "Head"]):
                continue
            else:
                roles.append(f"{prefix} {strip_seniority(base_role)}")
    roles.extend(EXECUTIVE_ROLES.get(domain, []))
    return dedupe(roles)


def seniority_prefixes_for_domain(domain: str) -> list[str]:
    """Use realistic seniority labels for each industry family."""
    if domain in {"Technology", "Engineering"}:
        return SENIORITY_PREFIXES
    if domain in {"Finance", "Law", "Education", "Healthcare", "Marketing", "Business", "Business HR"}:
        return ["", "Junior", "Associate", "Senior"]
    return ["", "Junior", "Associate", "Senior", "Lead"]


def strip_seniority(role: str) -> str:
    """Remove common seniority words before generating clean progression variants."""
    cleaned = role
    for prefix in ["Junior ", "Associate ", "Senior ", "Lead ", "Principal ", "Staff ", "Head of "]:
        if cleaned.casefold().startswith(prefix.casefold()):
            cleaned = cleaned[len(prefix):]
    return cleaned.strip()


def get_career_knowledge(career_name: str, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = get_career_catalog()
    if career_name in catalog:
        return catalog[career_name]

    fallback = fallback or {}
    domain = infer_domain_from_text(career_name + " " + " ".join(fallback.get("required_skills", [])))
    generated = {
        "domain": domain,
        "description": fallback.get("description") or f"A professional path focused on {career_name} outcomes.",
        "required_skills": fallback.get("required_skills", SKILLS_BY_DOMAIN.get(domain, [])[:6]),
        "technical_skills": fallback.get("technical_skills", SKILLS_BY_DOMAIN.get(domain, [])[:5]),
        "soft_skills": fallback.get("soft_skills", ["Communication", "Problem Solving", "Professional Judgment"]),
        "tools": fallback.get("tools", DOMAIN_PROFILES.get(domain, {}).get("tools", SKILLS_BY_DOMAIN.get(domain, [])[:4])),
        "degree_requirements": fallback.get("degree_requirements", ["Relevant degree or portfolio proof"]),
        "preferred_certifications": fallback.get("recommended_certifications", fallback.get("preferred_certifications", [])),
        "target_projects": fallback.get("target_projects", [f"{career_name} portfolio project"]),
        "salary": fallback.get("salary", "Market dependent"),
        "future_growth": fallback.get("future_growth", "Medium to High"),
        "ai_impact": fallback.get("ai_impact", "AI changes routine work; role-specific judgment and proof remain important."),
    }
    return enrich_career(career_name, generated)


def enrich_career(name: str, career: dict[str, Any]) -> dict[str, Any]:
    domain = career.get("domain", infer_domain_from_text(name))
    domain_profile = DOMAIN_PROFILES.get(domain, {})
    resources = career.get("learning_resources", {})
    domain_resources = {
        "books": domain_profile.get("books", []),
        "youtube_channels": domain_profile.get("youtube_channels", []),
        "courses": domain_profile.get("courses", []),
        "communities": domain_profile.get("communities", []),
        "practice_sites": domain_profile.get("practice_platforms", []),
        "professional_organizations": domain_profile.get("professional_organizations", []),
        "internships": career.get("internship_recommendations", [f"{name} internship", f"{domain} apprenticeship"]),
    }
    return {
        "name": name,
        "domain": domain,
        "description": career.get("description", ""),
        "required_skills": career.get("required_skills", []),
        "technical_skills": career.get("technical_skills") or domain_profile.get("technical_skills", SKILLS_BY_DOMAIN.get(domain, []))[:6],
        "soft_skills": career.get("soft_skills", []),
        "tools": career.get("tools") or domain_profile.get("tools") or SKILLS_BY_DOMAIN.get(domain, [])[:4],
        "software": career.get("software", domain_profile.get("software", [])),
        "frameworks": career.get("frameworks", domain_profile.get("frameworks", [])),
        "degree_requirements": career.get("degree_requirements", []),
        "preferred_certifications": career.get("preferred_certifications", career.get("recommended_certifications", [])),
        "recommended_certifications": career.get("preferred_certifications", career.get("recommended_certifications", [])),
        "certifications": career.get("certifications") or career.get("preferred_certifications") or domain_profile.get("certifications") or [f"{name} professional certificate"],
        "experience_level": career.get("experience_level", "Entry to mid-level with portfolio proof"),
        "portfolio_requirements": career.get("portfolio_requirements", career.get("target_projects", [])),
        "target_projects": career.get("target_projects", []),
        "interview_pattern": career.get(
            "interview_pattern",
            domain_profile.get("interview", ["Resume screen", "Role knowledge round", "Portfolio or case discussion", "Behavioral interview"]),
        ),
        "hiring_companies": career.get("hiring_companies", career.get("top_hiring_companies", domain_profile.get("companies", hiring_companies_for_domain(domain)))),
        "top_hiring_companies": career.get("top_hiring_companies", career.get("hiring_companies", domain_profile.get("companies", hiring_companies_for_domain(domain)))),
        "salary": career.get("salary", "Market dependent"),
        "salary_ranges": career.get("salary_ranges", domain_profile.get("salary_ranges", {})),
        "future_growth": career.get("future_growth", "Medium to High"),
        "ai_impact": career.get("ai_impact", domain_profile.get("ai_impact", "AI changes routine work; judgment and proof become more valuable.")),
        "AI_impact": career.get("AI_impact", career.get("ai_impact", domain_profile.get("ai_impact", ""))),
        "remote_opportunities": career.get("remote_opportunities", domain_profile.get("remote", remote_level_for_domain(domain))),
        "freelance_opportunities": career.get("freelance_opportunities", domain_profile.get("freelance", freelance_level_for_domain(domain))),
        "startup_opportunities": career.get("startup_opportunities", domain_profile.get("startup", startup_level_for_domain(domain))),
        "most_demanded_countries": career.get("most_demanded_countries", ["India", "USA", "Germany", "Canada", "Australia"]),
        "most_demanded_cities": career.get("most_demanded_cities", demanded_cities_for_domain(domain)),
        "career_path": career.get("career_path", career_path_for(name, domain)),
        "roadmap": career.get("roadmap", roadmap_for(name, domain, career.get("required_skills", []))),
        "ats_keywords": career.get("ats_keywords", ats_keywords_for(name, domain, career.get("required_skills", []))),
        "resume_keywords": career.get("resume_keywords", resume_keywords_for(name, domain, career.get("required_skills", []))),
        "transition_paths": career.get("transition_paths", transition_paths_for(name, domain)),
        "industry_insights": career.get("industry_insights", industry_insights_for(name, domain)),
        "daily_responsibilities": career.get("daily_responsibilities", daily_responsibilities_for(name, domain)),
        "kpis": career.get("kpis", kpis_for(domain)),
        "licensing_requirements": career.get("licensing_requirements", licensing_requirements_for(name, domain)),
        "work_environment": career.get("work_environment", work_environment_for(domain)),
        "expected_growth": career.get("expected_growth", career.get("future_growth", "Medium to High")),
        "internship_recommendations": career.get("internship_recommendations", [f"{name} internship", f"{domain} trainee role"]),
        "country_specific_information": career.get("country_specific_information", {}),
        "learning_resources": {**BASE_RESOURCES, **domain_resources, **resources},
    }


def generate_profession_profile(name: str, domain: str) -> dict[str, Any]:
    """Create a profession-aware career profile from reusable domain data."""
    domain = role_domain_override(name, domain)
    profile = DOMAIN_PROFILES.get(domain, DOMAIN_PROFILES["Business"])
    required = role_specific_skills(name, domain, profile)
    description = f"{name} is a {domain.lower()} profession focused on {', '.join(required[:3]).lower()} and measurable career outcomes."
    return {
        "domain": domain,
        "description": description,
        "required_skills": required,
        "technical_skills": role_specific_technical_skills(name, domain, profile),
        "soft_skills": role_specific_soft_skills(domain),
        "tools": profile.get("tools", []),
        "software": profile.get("software", []),
        "frameworks": profile.get("frameworks", []),
        "degree_requirements": degree_requirements_for(name, domain),
        "preferred_certifications": profile.get("certifications", []) or [f"{name} professional certificate"],
        "certifications": profile.get("certifications", []) or [f"{name} professional certificate"],
        "target_projects": portfolio_for(name, domain, profile),
        "portfolio_requirements": portfolio_for(name, domain, profile),
        "hiring_companies": profile.get("companies", []),
        "top_hiring_companies": profile.get("companies", []),
        "salary": salary_level_for_domain(domain),
        "salary_ranges": profile.get("salary_ranges", {}),
        "future_growth": growth_for_domain(domain),
        "remote_opportunities": profile.get("remote", remote_level_for_domain(domain)),
        "freelance_opportunities": profile.get("freelance", freelance_level_for_domain(domain)),
        "startup_opportunities": profile.get("startup", startup_level_for_domain(domain)),
        "ai_impact": profile.get("ai_impact", ""),
        "interview_pattern": profile.get("interview", []),
        "career_path": career_path_for(name, domain),
        "roadmap": roadmap_for(name, domain, required),
        "ats_keywords": ats_keywords_for(name, domain, required),
        "resume_keywords": resume_keywords_for(name, domain, required),
        "transition_paths": transition_paths_for(name, domain),
        "industry_insights": industry_insights_for(name, domain),
        "daily_responsibilities": daily_responsibilities_for(name, domain),
        "kpis": kpis_for(domain),
        "licensing_requirements": licensing_requirements_for(name, domain),
        "work_environment": work_environment_for(domain),
        "expected_growth": growth_for_domain(domain),
        "most_demanded_cities": demanded_cities_for_domain(domain),
        "most_demanded_countries": ["India", "USA", "Germany", "Canada", "Australia"],
        "internship_recommendations": [f"{name} internship", f"{domain} trainee role", f"{name} shadowing project"],
        "learning_resources": {
            "books": profile.get("books", []),
            "courses": profile.get("courses", []),
            "youtube_channels": profile.get("youtube_channels", []),
            "communities": profile.get("communities", []),
            "practice_sites": profile.get("practice_platforms", []),
            "professional_organizations": profile.get("professional_organizations", []),
        },
    }


def role_specific_skills(name: str, domain: str, profile: dict[str, Any]) -> list[str]:
    """Blend domain skills with role-name signals without leaking unrelated technologies."""
    skills = list(profile.get("required_skills", []))
    lowered = name.casefold()
    additions = {
        "nurse": ["Patient Care", "Clinical Documentation", "Medication Safety"],
        "doctor": ["Diagnosis", "Patient Care", "Clinical Decision Making"],
        "pharmacist": ["Pharmacology", "Medication Counseling", "Drug Safety"],
        "lawyer": ["Legal Research", "Advocacy", "Legal Drafting"],
        "judge": ["Judicial Reasoning", "Evidence Evaluation", "Legal Ethics"],
        "teacher": ["Lesson Planning", "Assessment", "Classroom Management"],
        "professor": ["Research", "Teaching", "Academic Publishing"],
        "accountant": ["Accounting", "Taxation", "Financial Reporting"],
        "bank": ["Banking Operations", "Risk Analysis", "Customer Advisory"],
        "designer": ["Visual Design", "Portfolio Development", "Client Communication"],
        "architect": ["Architectural Design", "Building Codes", "BIM"],
        "engineer": ["Engineering Fundamentals", "Project Documentation", "Quality Control"],
        "manager": ["Team Leadership", "Operations", "Stakeholder Management"],
    }
    for keyword, values in additions.items():
        if keyword in lowered:
            skills = values + skills
    return dedupe(skills)[:8]


def role_domain_override(name: str, domain: str) -> str:
    lowered = name.casefold()
    if "physiotherapist" in lowered or "physiotherapy" in lowered:
        return "Healthcare"
    if any(term in lowered for term in ["audit", "accountant", "tax", "finance controller", "chartered accountant"]):
        return "Finance"
    if any(term in lowered for term in ["journalist", "reporter", "editor"]):
        return "Creative"
    if any(term in lowered for term in ["pilot", "aviation", "flight"]):
        return "Engineering"
    return domain


def role_specific_technical_skills(name: str, domain: str, profile: dict[str, Any]) -> list[str]:
    """Return domain-relevant technical skills for the selected role."""
    skills = list(profile.get("technical_skills", []))
    lowered = name.casefold()
    if domain == "Technology":
        if "frontend" in lowered:
            skills = ["HTML", "CSS", "JavaScript", "React", "TypeScript"] + skills
        elif "backend" in lowered:
            skills = ["Python", "Java", "APIs", "Databases", "Docker"] + skills
        elif "data" in lowered:
            skills = ["SQL", "Python", "Data Modeling", "Pipelines", "Warehousing"] + skills
    if domain == "Engineering" and "civil" in lowered:
        skills = ["AutoCAD", "STAAD Pro", "Estimation", "Site Planning"] + skills
    if domain == "Healthcare" and "administrator" in lowered:
        skills = ["Hospital Operations", "Healthcare Finance", "Medical Records", "Compliance"] + skills
    return dedupe(skills)[:8]


def role_specific_soft_skills(domain: str) -> list[str]:
    """Provide soft skills tailored to each profession family."""
    return {
        "Healthcare": ["Empathy", "Coordination", "Decision Making", "Ethics"],
        "Law": ["Argumentation", "Ethics", "Attention to Detail", "Negotiation"],
        "Education": ["Patience", "Public Speaking", "Mentoring", "Feedback"],
        "Creative": ["Creativity", "Storytelling", "Collaboration", "Client Communication"],
        "Finance": ["Attention to Detail", "Business Judgment", "Presentation", "Integrity"],
        "Government": ["Ethics", "Discipline", "Public Communication", "Judgment"],
    }.get(domain, ["Communication", "Problem Solving", "Team Collaboration", "Professional Judgment"])


def degree_requirements_for(name: str, domain: str) -> list[str]:
    """Return typical degree requirements without pretending they are mandatory for every market."""
    return {
        "Technology": ["Computer Science", "Information Technology", "Engineering", "portfolio-backed degree"],
        "Engineering": [f"{name.replace(' Engineer', '')} Engineering", "relevant engineering degree"],
        "Healthcare": ["MBBS", "Nursing", "Pharmacy", "Public Health", "Healthcare Management"],
        "Law": ["LLB", "LLM", "Bar eligibility where required"],
        "Finance": ["BCom", "BBA", "MBA Finance", "Economics"],
        "Marketing": ["Marketing", "BBA", "Mass Communication", "portfolio-backed degree"],
        "Education": ["BEd", "subject degree", "teaching certification"],
        "Architecture": ["BArch", "Architecture"],
        "Agriculture": ["Agriculture", "Food Technology", "Agri Business"],
    }.get(domain, ["Relevant degree or portfolio proof"])


def portfolio_for(name: str, domain: str, profile: dict[str, Any]) -> list[str]:
    """Generate profession-specific proof artifacts for dashboard cards."""
    base = list(profile.get("portfolio", []))
    if base:
        return base[:4]
    return [f"{name} case study", f"{domain} portfolio artifact", "measurable outcome report"]


def ats_keywords_for(name: str, domain: str, required: list[str]) -> list[str]:
    """Return ATS terms scoped to the role domain."""
    domain_terms = {
        "Healthcare": ["clinical documentation", "patient safety", "care plan", "hospital protocols"],
        "Finance": ["financial reporting", "audit", "taxation", "compliance", "variance analysis"],
        "Law": ["legal research", "contract drafting", "case analysis", "compliance"],
        "Education": ["lesson planning", "assessment", "curriculum", "student outcomes"],
        "Marketing": ["campaign performance", "brand strategy", "SEO", "content planning"],
        "Creative": ["portfolio", "visual design", "client brief", "creative direction"],
        "Architecture": ["BIM", "Revit", "building codes", "design development"],
        "Hospitality": ["guest experience", "service recovery", "hotel operations", "food safety"],
        "Agriculture": ["crop advisory", "soil science", "field operations", "sustainability"],
        "Government": ["public administration", "policy implementation", "citizen services", "governance"],
        "Science": ["research methods", "laboratory protocols", "publication", "data analysis"],
        "Business": ["stakeholder management", "operations", "process improvement", "CRM"],
        "Engineering": ["project documentation", "quality control", "safety", "technical drawings"],
        "Technology": ["software architecture", "testing", "deployment", "version control"],
    }
    return dedupe([name, domain, *required[:6], *domain_terms.get(domain, [])])[:12]


def resume_keywords_for(name: str, domain: str, required: list[str]) -> list[str]:
    """Return resume terms recruiters expect for a specific career."""
    return dedupe([*ats_keywords_for(name, domain, required), "measurable outcomes", "cross-functional collaboration"])[:14]


def transition_paths_for(name: str, domain: str) -> list[str]:
    paths = {
        "Healthcare": ["Clinical specialization", "Healthcare operations", "Quality and compliance leadership"],
        "Finance": ["Audit and reporting", "FP&A / controllership", "Finance leadership"],
        "Law": ["Practice specialization", "In-house counsel", "Compliance leadership"],
        "Education": ["Senior teaching", "Academic coordination", "Institution leadership"],
        "Marketing": ["Performance marketing", "Brand management", "Growth leadership"],
        "Creative": ["Specialist portfolio track", "Art direction", "Creative leadership"],
        "Architecture": ["Project architect", "Design manager", "Principal architect"],
        "Hospitality": ["Department operations", "Revenue/service management", "General management"],
        "Agriculture": ["Field advisory", "Agri operations", "Sustainability programs"],
        "Government": ["Program administration", "Policy leadership", "Department management"],
        "Science": ["Research associate", "Senior scientist", "Principal investigator"],
        "Business": ["Operations specialist", "Manager", "Business unit leadership"],
        "Engineering": ["Senior engineer", "Project manager", "Engineering leadership"],
        "Technology": ["Senior contributor", "Technical lead", "Engineering leadership"],
    }
    return paths.get(domain, [name, f"Senior {name}", f"{domain} leadership"])


def industry_insights_for(name: str, domain: str) -> list[str]:
    insights = {
        "Healthcare": "Demand is driven by patient volumes, hospital expansion, specialization, and care quality.",
        "Finance": "Demand is shaped by compliance, reporting quality, risk control, and business expansion.",
        "Law": "Demand depends on regulation, contracts, disputes, privacy, and sector specialization.",
        "Education": "Education reforms, online learning, and outcome-focused teaching increase demand.",
        "Marketing": "Digital channels, brand differentiation, and retention analytics shape hiring.",
        "Creative": "Portfolio quality, originality, and measurable client outcomes drive opportunities.",
        "Architecture": "Urban growth, BIM adoption, sustainability, and construction quality drive demand.",
        "Hospitality": "Tourism, premium service, events, and guest experience sustain demand.",
        "Agriculture": "Food security, supply chains, sustainability, and precision farming shape demand.",
        "Government": "Public services, infrastructure, regulation, and social programs sustain demand.",
        "Science": "Research funding, clinical studies, sustainability, and applied R&D shape demand.",
        "Business": "Efficiency, customer growth, and operational excellence drive hiring.",
        "Engineering": "Infrastructure, manufacturing, energy systems, and safety standards drive demand.",
        "Technology": "Digital products, cybersecurity, automation, and cloud modernization drive demand.",
    }
    return [insights.get(domain, f"{name} demand depends on role-specific expertise and measurable outcomes.")]


def daily_responsibilities_for(name: str, domain: str) -> list[str]:
    responsibilities = {
        "Healthcare": ["Assess cases or patients", "Document outcomes", "Coordinate with clinical teams", "Follow safety protocols"],
        "Finance": ["Review reports", "Analyze variances", "Maintain controls", "Prepare stakeholder summaries"],
        "Law": ["Research law", "Draft documents", "Review cases", "Advise stakeholders"],
        "Education": ["Plan lessons", "Teach learners", "Assess progress", "Support student development"],
        "Marketing": ["Plan campaigns", "Track performance", "Create content briefs", "Optimize channels"],
        "Creative": ["Interpret briefs", "Create concepts", "Iterate designs", "Present work"],
        "Architecture": ["Develop drawings", "Coordinate models", "Review codes", "Present design options"],
        "Hospitality": ["Manage service delivery", "Resolve guest issues", "Coordinate teams", "Track operations"],
        "Agriculture": ["Inspect field conditions", "Advise stakeholders", "Track crop or supply metrics", "Document findings"],
        "Government": ["Process public work", "Coordinate programs", "Review compliance", "Report outcomes"],
        "Science": ["Run research tasks", "Analyze results", "Document methods", "Review literature"],
        "Business": ["Coordinate stakeholders", "Track metrics", "Improve processes", "Prepare reports"],
        "Engineering": ["Review technical work", "Coordinate execution", "Maintain safety", "Document progress"],
        "Technology": ["Design solutions", "Build or review systems", "Test changes", "Document decisions"],
    }
    return responsibilities.get(domain, [f"Execute {name} responsibilities", "Coordinate stakeholders", "Track measurable outcomes"])


def kpis_for(domain: str) -> list[str]:
    return {
        "Healthcare": ["patient safety", "documentation accuracy", "care turnaround", "protocol compliance"],
        "Finance": ["report accuracy", "deadline adherence", "control quality", "variance resolution"],
        "Law": ["case quality", "drafting accuracy", "turnaround time", "compliance outcomes"],
        "Education": ["student progress", "assessment quality", "class engagement", "curriculum completion"],
        "Marketing": ["conversion rate", "CAC", "engagement", "campaign ROI"],
        "Creative": ["portfolio quality", "revision cycles", "brand consistency", "client satisfaction"],
        "Architecture": ["drawing quality", "code compliance", "coordination accuracy", "design milestones"],
        "Hospitality": ["guest satisfaction", "service recovery", "occupancy/revenue", "SOP compliance"],
        "Agriculture": ["yield improvement", "field coverage", "supply reliability", "sustainability metrics"],
        "Government": ["service delivery time", "policy compliance", "citizen satisfaction", "program outcomes"],
        "Science": ["research quality", "method accuracy", "publication output", "reproducibility"],
        "Business": ["process efficiency", "stakeholder satisfaction", "cost savings", "delivery timelines"],
        "Engineering": ["quality defects", "safety compliance", "schedule adherence", "technical accuracy"],
        "Technology": ["system reliability", "defect rate", "delivery velocity", "code quality"],
    }.get(domain, ["quality", "timeliness", "stakeholder satisfaction", "measurable outcomes"])


def licensing_requirements_for(name: str, domain: str) -> list[str]:
    lowered = name.casefold()
    if domain == "Healthcare":
        if "doctor" in lowered or "medical" in lowered:
            return ["Valid medical registration where required"]
        if "nurse" in lowered:
            return ["Nursing council registration where required"]
        if "pharmac" in lowered:
            return ["Pharmacy council registration where required"]
        return ["Role-specific healthcare license where required"]
    if domain == "Law":
        return ["Bar council or jurisdiction eligibility where required"]
    if domain == "Architecture":
        return ["Architecture council registration where required"]
    if "pilot" in lowered:
        return ["Valid pilot license and medical fitness certification"]
    if domain == "Education":
        return ["Teaching certification where required"]
    return ["No universal license; verify local regulations for this role"]


def work_environment_for(domain: str) -> str:
    return {
        "Healthcare": "Hospitals, clinics, labs, pharmacies, or healthcare operations teams.",
        "Finance": "Corporate finance teams, audit firms, banks, consultancies, or shared-service centers.",
        "Law": "Law firms, courts, in-house legal teams, compliance teams, or public institutions.",
        "Education": "Schools, universities, edtech teams, training centers, or research institutions.",
        "Marketing": "Agencies, startups, consumer brands, SaaS teams, or media teams.",
        "Creative": "Studios, agencies, product teams, media companies, or freelance environments.",
        "Architecture": "Architecture studios, construction sites, planning firms, or real-estate teams.",
        "Hospitality": "Hotels, restaurants, resorts, travel operations, or event venues.",
        "Agriculture": "Field sites, agri-businesses, food companies, farms, or sustainability programs.",
        "Government": "Public offices, field departments, policy teams, or public-sector agencies.",
        "Science": "Labs, universities, R&D centers, field sites, or clinical research teams.",
        "Business": "Corporate offices, operations floors, client sites, or hybrid business teams.",
        "Engineering": "Plants, project sites, design offices, labs, or infrastructure teams.",
        "Technology": "Product teams, engineering organizations, cloud environments, or remote teams.",
    }.get(domain, "Role-specific professional environment.")


def roadmap_for(name: str, domain: str, required: list[str]) -> list[str]:
    focus = required[:3] or SKILLS_BY_DOMAIN.get(domain, [])[:3] or [name]
    return [
        f"Month 1: strengthen {focus[0]} fundamentals for {name}.",
        f"Month 2: complete a {domain.lower()} proof artifact using {focus[min(1, len(focus)-1)]}.",
        f"Month 3: document outcomes with role-specific resume keywords.",
        f"Month 4: prepare interviews around {focus[min(2, len(focus)-1)]}.",
    ]


def career_path_for(name: str, domain: str) -> list[str]:
    """Generate a simple career progression ladder."""
    key = name.casefold()
    if domain == "Finance":
        if "audit" in key or "auditor" in key:
            return ["Audit Associate", "Senior Audit Associate", "Audit Manager", "Senior Financial Analyst", "Corporate Finance Manager", "Finance Manager", "Finance Controller", "Finance Director", "Chief Financial Officer"]
        if "tax" in key:
            return ["Tax Associate", "Tax Consultant", "Tax Manager", "Finance Manager", "Finance Director", "Chief Financial Officer"]
        if "treasury" in key:
            return ["Treasury Analyst", "Senior Treasury Analyst", "Treasury Manager", "Finance Controller", "Finance Director", "Chief Financial Officer"]
        if "investment" in key or "portfolio" in key:
            return ["Investment Analyst", "Senior Investment Analyst", "Portfolio Manager", "Investment Director", "Chief Investment Officer"]
        return ["Finance Analyst", "Senior Financial Analyst", "FP&A Manager", "Finance Manager", "Finance Controller", "Finance Director", "Chief Financial Officer"]
    if domain == "Technology" and "software" in key:
        return ["Junior Software Engineer", "Software Engineer", "Senior Software Engineer", "Lead Software Engineer", "Engineering Manager", "Director of Engineering", "VP Engineering", "Chief Technology Officer"]
    if domain == "Technology" and ("backend" in key or "frontend" in key or "full stack" in key):
        specialty = "Backend Engineer" if "backend" in key else "Frontend Engineer" if "frontend" in key else "Full Stack Engineer"
        return [f"Junior {specialty}", specialty, f"Senior {specialty}", f"Lead {specialty}", "Engineering Manager", "Director of Engineering", "Chief Technology Officer"]
    if domain == "Technology" and ("security" in key or "cyber" in key or "soc" in key):
        return ["SOC Analyst", "Cybersecurity Analyst", "Security Engineer", "Senior Security Engineer", "Security Architect", "Head of Security", "Chief Information Security Officer"]
    if domain == "Technology" and ("cloud" in key or "devops" in key or "site reliability" in key):
        return ["Cloud Engineer", "Senior Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer", "Cloud Architect", "Platform Engineering Manager", "Head of Cloud"]
    if domain == "Technology" and ("data" in key or "machine learning" in key or "ai " in key or key == "ai engineer"):
        return ["Data Analyst", "Data Scientist", "Machine Learning Engineer", "AI Engineer", "Senior AI Engineer", "AI Architect", "Head of AI"]
    if domain == "Healthcare":
        if "nurse" in key:
            return ["Staff Nurse", "Senior Nurse", "Charge Nurse", "Nursing Supervisor", "Nurse Manager", "Director of Nursing"]
        if "pharmac" in key:
            return ["Pharmacist", "Clinical Pharmacist", "Senior Pharmacist", "Pharmacy Manager", "Head of Pharmacy"]
        if "doctor" in key or "medical officer" in key or "surgeon" in key or "dentist" in key:
            return ["Medical Officer", "Resident Doctor", "Specialist Doctor", "Consultant Doctor", "Medical Director"]
        return ["Healthcare Associate", name, f"Senior {name}", "Healthcare Manager", "Healthcare Operations Director"]
    if domain == "Law":
        return ["Legal Intern", "Legal Associate", "Senior Legal Associate", "Legal Counsel", "Legal Manager", "Partner", "General Counsel"]
    if domain == "Architecture":
        return ["Junior Architect", "Architect", "Project Architect", "Senior Architect", "Design Manager", "Principal Architect"]
    if domain == "Engineering":
        if "civil" in key or "construction" in key or "structural" in key:
            return ["Site Engineer", "Civil Engineer", "Structural Engineer", "Construction Manager", "Project Manager", "Infrastructure Director"]
        if "mechanical" in key or "manufacturing" in key or "production" in key:
            return ["Graduate Engineer Trainee", "Mechanical Engineer", "Manufacturing Engineer", "Production Manager", "Plant Head", "Director of Engineering"]
        if "electrical" in key or "power" in key:
            return ["Electrical Engineer", "Senior Electrical Engineer", "Power Systems Engineer", "Project Manager", "Engineering Manager"]
        return ["Graduate Engineer Trainee", name, f"Senior {name}", f"Lead {domain} Specialist", "Engineering Manager"]
    if domain == "Education":
        return ["Teacher", "Senior Teacher", "Academic Coordinator", "Principal", "Dean"]
    if domain == "Marketing":
        return ["Marketing Executive", "Marketing Manager", "Senior Marketing Manager", "Head of Marketing", "Chief Marketing Officer"]
    if domain == "Business":
        if "hr" in key or "recruit" in key or "talent" in key:
            return ["HR Executive", "Recruiter", "HR Business Partner", "HR Manager", "Head of HR", "Chief Human Resources Officer"]
        if "supply chain" in key or "logistics" in key:
            return ["Logistics Coordinator", "Supply Chain Analyst", "Supply Chain Manager", "Operations Manager", "Director of Supply Chain"]
        if "sales" in key:
            return ["Sales Executive", "Account Manager", "Sales Manager", "Regional Sales Manager", "Sales Director"]
        return ["Business Analyst", "Senior Business Analyst", "Product Manager", "Program Manager", "Business Unit Head"]
    if domain == "Creative":
        return ["Junior Designer", name, f"Senior {name}", "Art Director", "Creative Director"]
    if domain == "Hospitality":
        return ["Trainee", name, f"Senior {name}", "Operations Manager", "General Manager"]
    if domain == "Agriculture":
        return ["Field Officer", name, f"Senior {name}", "Agri Operations Manager", "Agriculture Program Director"]
    if domain == "Government":
        return ["Officer Trainee", name, f"Senior {name}", "Department Manager", "Director"]
    if domain == "Science":
        return ["Research Assistant", "Research Associate", "Research Scientist", "Senior Research Scientist", "Principal Scientist"]
    return [f"Entry-level {name}", name, f"Senior {name}", f"Lead {domain} Specialist"]


def salary_level_for_domain(domain: str) -> str:
    """Return a directional salary level for the career catalog."""
    return {
        "Technology": "High",
        "Finance": "Medium to High",
        "Healthcare": "Medium to High",
        "Law": "Medium to High",
        "Engineering": "Medium to High",
        "Creative": "Medium",
        "Education": "Medium",
        "Government": "Structured government pay",
        "Entrepreneurship": "Variable",
    }.get(domain, "Medium")


def growth_for_domain(domain: str) -> str:
    """Return directional market growth for a domain."""
    return {
        "Technology": "Very High",
        "Healthcare": "High",
        "Finance": "High",
        "Marketing": "High",
        "Agriculture": "High",
        "Entrepreneurship": "High upside, high uncertainty",
        "Government": "Stable",
    }.get(domain, "Medium to High")


def detect_candidate_domain(
    text: str,
    skills: list[str] | None = None,
    degree: str = "",
    branch: str = "",
) -> tuple[str, float, dict[str, int]]:
    search_space = " ".join([text, degree, branch, " ".join(skills or [])]).casefold()
    scores: dict[str, int] = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(2 if " " in keyword and keyword in search_space else 1 for keyword in keywords if keyword.casefold() in search_space)
        skill_score = sum(1 for skill in SKILLS_BY_DOMAIN.get(domain, []) if skill.casefold() in search_space)
        if score or skill_score:
            scores[domain] = score + skill_score

    if not scores:
        return "General", 0.0, {}
    domain, score = max(scores.items(), key=lambda item: item[1])
    total = sum(scores.values())
    confidence = min(0.98, max(0.35, score / max(total, 1)))
    return domain, round(confidence, 2), scores


def infer_domain_from_text(text: str) -> str:
    domain, confidence, _ = detect_candidate_domain(text)
    return domain if confidence >= 0.35 else "General"


def categorize_skills_for_domain(skills: list[str], domain: str) -> dict[str, list[str]]:
    domain_skills = set(SKILLS_BY_DOMAIN.get(domain, []))
    technical = []
    professional = []
    soft = []
    tools = []
    for skill in skills:
        if skill in domain_skills:
            technical.append(skill)
        elif skill.casefold() in {"communication", "leadership", "problem solving", "negotiation", "empathy", "presentation"}:
            soft.append(skill)
        elif any(token in skill.casefold() for token in ["excel", "power bi", "figma", "autocad", "revit", "git", "ads"]):
            tools.append(skill)
        else:
            professional.append(skill)
    return {
        f"{domain} Core Skills": sorted(set(technical), key=str.casefold),
        "Professional Skills": sorted(set(professional), key=str.casefold),
        "Tools": sorted(set(tools), key=str.casefold),
        "Soft Skills": sorted(set(soft), key=str.casefold),
    }


def discover_careers(interest_text: str, profile: Any | None = None, limit: int = 4) -> list[CareerRecommendation]:
    signals = " ".join(
        [
            interest_text,
            getattr(profile, "degree", "") if profile else "",
            getattr(profile, "branch", "") if profile else "",
            " ".join(getattr(profile, "skills", []) if profile else []),
            " ".join(getattr(profile, "projects", []) if profile else []),
        ]
    ).casefold()
    catalog = get_career_catalog()
    recommendations = []
    for name, career in catalog.items():
        keywords = [career["domain"], name, career["description"], *career["required_skills"], *career["technical_skills"], *career["degree_requirements"]]
        matched = [item for item in keywords if item and item.casefold() in signals]
        related = related_interest_matches(signals, name, career)
        score = min(100, 35 + len(matched) * 12 + len(related) * 10)
        if matched or related:
            recommendations.append(
                CareerRecommendation(
                    career=name,
                    domain=career["domain"],
                    fit_score=score,
                    explanation=build_discovery_explanation(name, career, matched + related),
                    matched_signals=sorted(set(matched + related), key=str.casefold)[:6],
                )
            )
    if not recommendations:
        domain = infer_domain_from_text(signals)
        for name, career in catalog.items():
            if career["domain"] == domain:
                recommendations.append(
                    CareerRecommendation(
                        career=name,
                        domain=career["domain"],
                        fit_score=58,
                        explanation=f"This path belongs to {domain} and can be explored with your current interest signals.",
                        matched_signals=[domain],
                    )
                )
    return sorted(recommendations, key=lambda item: item.fit_score, reverse=True)[:limit]


def career_search_suggestions(query: str, careers: dict[str, dict[str, Any]], limit: int = 50) -> list[str]:
    """Return ranked career names for autocomplete-style filtering."""
    normalized = query.strip().casefold()
    if not normalized:
        return sorted(careers.keys())[:limit]
    scored = []
    for name, career in careers.items():
        name_key = name.casefold()
        domain = str(career.get("domain", "")).casefold()
        path = " ".join(career.get("career_path", [])).casefold()
        score = 0
        if name_key == normalized:
            score += 120
        if name_key.startswith(normalized):
            score += 90
        if normalized in name_key:
            score += 65
        if any(part.startswith(normalized) for part in name_key.split()):
            score += 50
        if normalized in domain:
            score += 25
        if normalized in path:
            score += 20
        if score:
            if any(term in normalized for term in ["senior", "lead", "manager", "director", "head", "chief", "cfo", "cto", "cmo"]):
                score += seniority_rank(name) * 3
            elif any(name_key.startswith(prefix + " ") for prefix in ["junior", "associate", "senior", "lead", "principal", "staff", "director", "head of"]):
                score -= 8
            scored.append((score, name))
    return [name for _, name in sorted(scored, key=lambda item: (-item[0], item[1].casefold()))[:limit]]


def recommend_careers_for_profile(
    profile: Any,
    resume: Any | None,
    careers: dict[str, dict[str, Any]],
    limit: int = 5,
) -> list[CareerRecommendation]:
    """Rank careers using experience, designation, education, skills, and certifications."""
    designation = infer_current_designation(profile, resume)
    years = infer_years_experience(profile, resume)
    current_domain = getattr(resume, "detected_domain", "") if resume else ""
    goal_name = str(getattr(profile, "career_goal", "") or "")
    goal_domain = str(careers.get(goal_name, {}).get("domain", "")) if goal_name else ""
    primary_domain = current_domain if current_domain and current_domain != "General" else goal_domain
    education = " ".join([getattr(profile, "degree", ""), getattr(profile, "branch", "")]).casefold()
    skills = [skill.casefold() for skill in getattr(profile, "skills", [])]
    domain_scores = estimate_profile_domain_relevance(profile, resume, careers)
    designation_domain = domain_from_designation(designation, skills)
    if designation_domain:
        primary_domain = designation_domain
        current_domain = designation_domain
        if not goal_domain:
            goal_domain = designation_domain
    if not primary_domain and domain_scores:
        primary_domain = max(domain_scores.items(), key=lambda item: item[1])[0]
    current_path = career_path_for(designation, current_domain or primary_domain) if designation and (current_domain or primary_domain) else []
    explicit_switch = bool(goal_domain and primary_domain and goal_domain != primary_domain)
    allowed_domains = selected_recommendation_domains(domain_scores, goal_domain, primary_domain)
    if explicit_switch and goal_domain and domain_scores.get(goal_domain, 0) >= 28:
        allowed_domains.add(goal_domain)
    certifications = [cert.casefold() for cert in getattr(profile, "certifications", [])]
    detected_domain = getattr(resume, "detected_domain", "") if resume else ""
    scored = []
    for name, career in careers.items():
        degrees = " ".join(career.get("degree_requirements", [])).casefold()
        cert_targets = [cert.casefold() for cert in career.get("preferred_certifications", career.get("certifications", []))]
        career_domain = career.get("domain", "")
        if "physiotherapist" in name.casefold():
            career_domain = "Healthcare"
        if allowed_domains and career_domain not in allowed_domains:
            continue

        experience_score = experience_alignment_score(name, years)
        designation_score = text_similarity_score(designation, name + " " + " ".join(career.get("career_path", [])))
        education_score = text_similarity_score(education + " " + detected_domain, degrees + " " + career_domain)
        layered_skills = layered_skill_score(skills, {**career, "domain": career_domain})
        skill_score = layered_skills["score"]
        cert_score = overlap_score(certifications, cert_targets)
        domain_score = domain_scores.get(str(career_domain), 0)
        total = round(
            skill_score * 0.48
            + min(domain_score, 100) * 0.18
            + designation_score * 0.14
            + education_score * 0.10
            + experience_score * 0.06
            + cert_score * 0.04
        )
        if years >= 3 and seniority_rank(name) <= 2:
            total -= 20
        if years >= 6 and seniority_rank(name) <= 3:
            total -= 15
        if years >= 3 and seniority_rank(name) == 4:
            total += 12
        if years >= 4 and career_domain == "Finance" and any(term in name.casefold() for term in ["manager", "controller", "director"]):
            total += 8
        path_names = [path_item.casefold() for path_item in current_path]
        if name.casefold() in path_names:
            current_index = path_names.index(designation.casefold()) if designation.casefold() in path_names else -1
            role_index = path_names.index(name.casefold())
            if current_index >= 0 and role_index <= current_index:
                total -= 10
            else:
                total += 34
                if current_index >= 0 and role_index == current_index + 1:
                    total += 30
        if primary_domain:
            if career_domain == primary_domain or (explicit_switch and career_domain == goal_domain):
                total += 8
            else:
                total -= 65
        if detected_domain and career_domain == detected_domain:
            total += 6
        if goal_name:
            goal_key = goal_name.casefold()
            name_key = name.casefold()
            if name_key == goal_key:
                total += 12
            elif goal_key in name_key or name_key in goal_key:
                total += 7
            total += role_family_alignment_score(goal_key, name_key)
        if designation:
            designation_key = strip_seniority(designation).casefold()
            if designation_key and designation_key in name.casefold():
                total += 16
            if "ux" in designation_key and not any(term in name.casefold() for term in ["ux", "ui ux", "product designer"]):
                total -= 24
            if "devops" in designation_key and career_domain != "Technology":
                total -= 30
        total = min(total, int(layered_skills["cap"]))
        total = max(0, total - recommendation_tie_penalty(goal_name, designation, name))
        if total >= 100:
            total = 98
        if not layered_skills["missing_mandatory"] and len(layered_skills["matched_domain"]) >= max(4, len(layered_skills["domain_skills"]) - 1):
            total = min(total + 2, 99)
        if primary_domain and career_domain != primary_domain and total < 35:
            continue
        if total > 25:
            reasons = []
            if designation_score:
                reasons.append("current designation")
            if education_score:
                reasons.append("education/domain")
            if layered_skills["matched_domain"] or layered_skills["matched_mandatory"]:
                reasons.append("domain skills")
            if years:
                reasons.append(f"{years}+ years experience")
            matched_required = [skill for skill in career.get("required_skills", []) if skill.casefold() in skills]
            missing_required = [skill for skill in career.get("required_skills", []) if skill.casefold() not in skills]
            explanation_parts = []
            if years:
                explanation_parts.append(f"{years} years of relevant experience")
            if designation:
                explanation_parts.append(f"current designation: {designation}")
            if education_score:
                explanation_parts.append("education/domain fit")
            if layered_skills["matched_mandatory"]:
                explanation_parts.append("mandatory skills: " + ", ".join(layered_skills["matched_mandatory"][:3]))
            if layered_skills["matched_domain"]:
                explanation_parts.append("domain strengths: " + ", ".join(layered_skills["matched_domain"][:4]))
            if layered_skills["matched_common"]:
                explanation_parts.append("common skills: " + ", ".join(layered_skills["matched_common"][:2]))
            if layered_skills["missing_mandatory"]:
                explanation_parts.append("mandatory gaps cap score: " + ", ".join(layered_skills["missing_mandatory"][:3]))
            elif missing_required:
                explanation_parts.append("missing: " + ", ".join(missing_required[:3]))
            scored.append(
                CareerRecommendation(
                    career=name,
                    domain=str(career_domain),
                    fit_score=max(0, min(total, 100)),
                    explanation="Recommended because " + "; ".join(explanation_parts or reasons or ["profile signals"]) + ".",
                    matched_signals=reasons,
                )
            )
    current_index = path_names.index(designation.casefold()) if designation and designation.casefold() in path_names else -1

    goal_key_for_sort = goal_name.casefold()

    def goal_alignment_rank(name: str) -> int:
        name_key = name.casefold()
        if goal_key_for_sort and name_key == goal_key_for_sort:
            return 4
        if goal_key_for_sort and (goal_key_for_sort in name_key or strip_seniority(goal_key_for_sort) in strip_seniority(name_key)):
            return 3
        if goal_key_for_sort and role_family_alignment_score(goal_key_for_sort, name_key) > 0:
            return 2
        if designation and strip_seniority(designation).casefold() in name_key:
            return 1
        return 0

    def recommendation_sort_key(item: CareerRecommendation) -> tuple[int, int, int, int, str]:
        name_key = item.career.casefold()
        goal_rank = goal_alignment_rank(item.career)
        if current_index >= 0 and name_key in path_names:
            role_index = path_names.index(name_key)
            if role_index > current_index:
                return (1, goal_rank, item.fit_score, -role_index, item.career.casefold())
        return (0, goal_rank, item.fit_score, -seniority_rank(item.career), item.career.casefold())

    return sorted(scored, key=recommendation_sort_key, reverse=True)[:limit]


def infer_current_designation(profile: Any, resume: Any | None) -> str:
    """Infer current designation from structured experience, resume text, or profile projects."""
    if resume and getattr(resume, "current_designation", ""):
        return str(resume.current_designation)
    if resume and getattr(resume, "structured_experience", None):
        for experience in resume.structured_experience:
            if experience.get("role"):
                return str(experience["role"])
    if resume and getattr(resume, "experience", None):
        return str(resume.experience[0])
    if resume and getattr(resume, "text", ""):
        text = getattr(resume, "text", "")
        known_roles = sorted(get_career_catalog().keys(), key=len, reverse=True)
        for role in known_roles:
            if len(role) > 4 and role.casefold() in text.casefold():
                return role
    return " ".join(getattr(profile, "internships", [])[:1] or getattr(profile, "projects", [])[:1])


def domain_from_designation(designation: str, skills: list[str]) -> str:
    signal = f"{designation} {' '.join(skills)}".casefold()
    if any(term in signal for term in ["devops", "site reliability", "cloud engineer", "kubernetes", "terraform", "ci/cd"]):
        return "Technology"
    if any(term in signal for term in ["software", "developer", "backend", "frontend", "full stack", "data scientist", "machine learning", "ai engineer"]):
        return "Technology"
    if any(term in signal for term in ["audit", "accountant", "accounting", "taxation", "financial reporting", "chartered accountant", "finance analyst"]):
        return "Finance"
    if any(term in signal for term in ["pilot", "aviation", "flight operations"]):
        return "Engineering"
    if any(term in signal for term in ["physiotherapist", "rehabilitation", "patient assessment", "exercise therapy"]):
        return "Healthcare"
    if any(term in signal for term in ["journalist", "reporting", "editing", "media research", "storytelling"]):
        return "Creative"
    if any(term in signal for term in ["administrative officer", "public administration", "policy"]):
        return "Government"
    if any(term in signal for term in ["sales executive", "account executive", "business development"]):
        return "Business"
    return ""


def role_family_alignment_score(goal_key: str, name_key: str) -> int:
    families = [
        (["pilot", "aviation", "flight"], ["pilot", "aviation", "flight", "airline"], -45),
        (["journalist", "journalism", "media"], ["journalist", "journalism", "editor", "reporter", "media", "news"], -42),
        (["physiotherapist", "physiotherapy"], ["physiotherapist", "physiotherapy", "rehabilitation", "clinical"], -38),
        (["interior designer", "interior design"], ["interior", "designer", "space", "architecture"], -35),
        (["audit", "chartered accountant"], ["audit", "accountant", "finance", "controller", "tax", "financial"], -35),
        (["sales executive", "sales"], ["sales", "account", "business development", "customer"], -32),
        (["hotel manager", "hospitality"], ["hotel", "hospitality", "guest", "restaurant", "tourism"], -34),
        (["pharmaceutical scientist", "pharmaceutical"], ["pharmaceutical", "pharmacist", "drug", "clinical", "bioprocess", "quality assurance"], -34),
    ]
    for goal_terms, allowed_terms, penalty in families:
        if any(term in goal_key for term in goal_terms):
            if any(term in name_key for term in allowed_terms):
                return 26
            return penalty
    return 0


def recommendation_tie_penalty(goal_name: str, designation: str, career_name: str) -> int:
    goal_key = strip_seniority(goal_name).casefold()
    designation_key = strip_seniority(designation).casefold()
    career_key = strip_seniority(career_name).casefold()
    raw_career_key = career_name.casefold()
    if goal_key and career_key == goal_key:
        if raw_career_key == goal_key:
            return 0
        if raw_career_key.startswith("junior "):
            return 4
        if raw_career_key.startswith("associate "):
            return 3
        if raw_career_key.startswith("senior "):
            return 2
        if raw_career_key.startswith("lead "):
            return 5
        return 1
    if designation_key and career_key == designation_key:
        return 1
    if goal_key and (goal_key in career_key or career_key in goal_key):
        return min(3, max(1, seniority_rank(career_name) - 1))
    if goal_key and role_family_alignment_score(goal_key, career_key) > 0:
        return min(5, seniority_rank(career_name))
    return min(7, seniority_rank(career_name) + 3)


def infer_years_experience(profile: Any, resume: Any | None) -> int:
    """Estimate years of experience from resume text and profile experience count."""
    import re

    text = " ".join(getattr(resume, "experience", []) if resume else [])
    if resume:
        text += " " + getattr(resume, "text", "")
    explicit = re.search(r"\b(\d{1,2})\+?\s*(?:years|yrs)\b", text, flags=re.IGNORECASE)
    if explicit:
        return int(explicit.group(1))
    years = [int(year) for year in re.findall(r"\b(20\d{2}|19\d{2})\b", text)]
    if len(years) >= 2:
        return max(0, min(35, max(years) - min(years)))
    return min(2, len(getattr(profile, "internships", [])))


def experience_alignment_score(role_name: str, years: int) -> int:
    """Score seniority fit so experienced users are not pushed toward entry roles."""
    rank = seniority_rank(role_name)
    if years >= 10:
        target = 5
    elif years >= 6:
        target = 4
    elif years >= 3:
        target = 3
    elif years >= 1:
        target = 2
    else:
        target = 1
    return max(0, 100 - abs(rank - target) * 22)


def seniority_rank(role_name: str) -> int:
    """Return an approximate seniority level from 1 entry-level to 6 executive."""
    value = role_name.casefold()
    if any(term in value for term in ["chief", "cfo", "cto", "cmo", "coo", "vp ", "vice president"]):
        return 6
    if any(term in value for term in ["director", "head of", "dean", "partner", "principal"]):
        return 5
    if any(term in value for term in ["manager", "controller", "lead", "staff", "consultant doctor", "principal"]):
        return 4
    if any(term in value for term in ["senior", "specialist", "consultant", "associate professor"]):
        return 3
    if any(term in value for term in ["associate", "executive", "officer", "analyst", "engineer", "teacher"]):
        return 2
    return 1


def text_similarity_score(source: str, target: str) -> int:
    """Small token-overlap scorer for role, education, and industry signals."""
    source_tokens = {token for token in source.casefold().replace("&", " ").split() if len(token) > 2}
    target_tokens = {token for token in target.casefold().replace("&", " ").split() if len(token) > 2}
    if not source_tokens or not target_tokens:
        return 0
    overlap = len(source_tokens & target_tokens)
    return min(100, round(overlap / max(1, len(source_tokens)) * 100))


def estimate_profile_domain_relevance(
    profile: Any,
    resume: Any | None,
    careers: dict[str, dict[str, Any]],
) -> dict[str, int]:
    """Score career domains before individual career ranking."""
    designation = infer_current_designation(profile, resume)
    skills = [str(skill).casefold() for skill in getattr(profile, "skills", [])]
    projects = " ".join(str(item) for item in getattr(profile, "projects", []))
    certifications = " ".join(str(item) for item in getattr(profile, "certifications", []))
    experience = " ".join(str(item) for item in getattr(profile, "internships", []))
    resume_text = getattr(resume, "text", "") if resume else ""
    education = " ".join([getattr(profile, "degree", ""), getattr(profile, "branch", "")])
    signal_text = " ".join([designation, education, projects, certifications, experience, resume_text]).casefold()
    scores: dict[str, int] = {}
    detected_domain = getattr(resume, "detected_domain", "") if resume else ""
    if detected_domain and detected_domain != "General":
        scores[detected_domain] = scores.get(detected_domain, 0) + 18
    designation_domain = domain_from_designation(designation, skills)
    if designation_domain:
        scores[designation_domain] = scores.get(designation_domain, 0) + 34
    goal_name = str(getattr(profile, "career_goal", "") or "")
    goal_domain = str(careers.get(goal_name, {}).get("domain", "")) if goal_name else ""
    if goal_domain:
        scores[goal_domain] = scores.get(goal_domain, 0) + 10
    for domain, keywords in DOMAIN_KEYWORDS.items():
        keyword_hits = sum(1 for keyword in keywords if keyword.casefold() in signal_text)
        skill_hits = sum(1 for skill in skills if skill in {item.casefold() for item in SKILLS_BY_DOMAIN.get(domain, [])})
        if keyword_hits or skill_hits:
            scores[domain] = scores.get(domain, 0) + keyword_hits * 6 + skill_hits * 9
    for career in careers.values():
        domain = str(career.get("domain", ""))
        if not domain:
            continue
        required = {str(skill).casefold() for skill in career.get("required_skills", [])}
        overlap = len(required & set(skills))
        if overlap >= 2:
            scores[domain] = scores.get(domain, 0) + min(overlap * 2, 8)
    return {domain: min(score, 100) for domain, score in scores.items() if score > 0}


def selected_recommendation_domains(domain_scores: dict[str, int], goal_domain: str, primary_domain: str) -> set[str]:
    if not domain_scores:
        return {domain for domain in [primary_domain, goal_domain] if domain}
    top_score = max(domain_scores.values())
    selected = {domain for domain, score in domain_scores.items() if score >= max(18, top_score * 0.72)}
    if primary_domain and domain_scores.get(primary_domain, 0) >= 12:
        selected.add(primary_domain)
    if goal_domain:
        goal_score = domain_scores.get(goal_domain, 0)
        primary_score = domain_scores.get(primary_domain, 0) if primary_domain else 0
        if goal_domain == primary_domain or goal_score >= max(22, primary_score * 0.82):
            selected.add(goal_domain)
    return selected


def classify_career_skills(career: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    required = [str(skill).casefold() for skill in career.get("required_skills", []) if str(skill).strip()]
    domain = str(career.get("domain", ""))
    domain_terms = {str(skill).casefold() for skill in SKILLS_BY_DOMAIN.get(domain, [])}
    technical_terms = {str(skill).casefold() for skill in career.get("technical_skills", [])}
    mandatory = []
    domain_skills = []
    common_skills = []
    for skill in required:
        if skill in COMMON_SKILL_TERMS:
            common_skills.append(skill)
        elif skill in domain_terms or skill in technical_terms:
            domain_skills.append(skill)
        else:
            domain_skills.append(skill)
    for skill in domain_skills[:3]:
        if skill not in mandatory:
            mandatory.append(skill)
    return common_skills, domain_skills, mandatory


def layered_skill_score(user_skills: list[str], career: dict[str, Any]) -> dict[str, Any]:
    user_set = {str(skill).casefold() for skill in user_skills}
    common_skills, domain_skills, mandatory_skills = classify_career_skills(career)
    matched_common = [skill for skill in common_skills if skill in user_set]
    matched_domain = [skill for skill in domain_skills if skill in user_set]
    matched_mandatory = [skill for skill in mandatory_skills if skill in user_set]
    missing_mandatory = [skill for skill in mandatory_skills if skill not in user_set]

    common_score = min(3, len(matched_common) * 1.0)
    domain_score = min(45, len(matched_domain) * 10)
    mandatory_score = min(30, len(matched_mandatory) * (30 / max(1, len(mandatory_skills))))
    score = round(common_score + domain_score + mandatory_score)

    if not mandatory_skills:
        cap = 86
    elif not matched_mandatory:
        cap = 58
    elif missing_mandatory:
        cap = 74 if len(missing_mandatory) >= 2 else 84
    else:
        cap = 98
    return {
        "score": min(score, cap),
        "cap": cap,
        "matched_common": matched_common,
        "matched_domain": matched_domain,
        "matched_mandatory": matched_mandatory,
        "missing_mandatory": missing_mandatory,
        "common_skills": common_skills,
        "domain_skills": domain_skills,
        "mandatory_skills": mandatory_skills,
    }


def overlap_score(source: list[str], target: list[str]) -> int:
    """Score list overlap for skills and certifications."""
    if not source or not target:
        return 0
    source_set = set(source)
    matched = sum(1 for item in target if item in source_set)
    return min(100, round(matched / max(1, len(target)) * 100))


def related_interest_matches(signals: str, name: str, career: dict[str, Any]) -> list[str]:
    matches = []
    combo_rules = [
        (["biology", "coding"], ["Bioinformatics", "Healthcare Administrator", "Data Scientist", "AI Engineer"]),
        (["business", "technology"], ["Product Manager", "Business Analyst", "AI Product Manager", "Data Scientist"]),
        (["law", "technology"], ["Corporate Lawyer", "Cybersecurity Engineer"]),
        (["creative", "technology"], ["UX Designer", "Digital Marketer"]),
        (["commerce", "analytics"], ["Finance Analyst", "Business Analyst"]),
        (["teaching", "technology"], ["Teacher", "Instructional Designer"]),
    ]
    for interests, careers in combo_rules:
        if all(term in signals for term in interests) and name in careers:
            matches.extend(interests)
    if career["domain"].casefold() in signals:
        matches.append(career["domain"])
    return matches


def build_discovery_explanation(name: str, career: dict[str, Any], signals: list[str]) -> str:
    signal_text = ", ".join(sorted(set(signals), key=str.casefold)[:4]) or career["domain"]
    return f"{name} fits because your profile or interests mention {signal_text}, and the role values {', '.join(career['required_skills'][:3])}."


def build_transition_plan(current_background: str, target_career: str, profile: Any | None = None) -> dict[str, Any]:
    target = get_career_knowledge(target_career)
    current_domain = infer_domain_from_text(current_background)
    skills = set(getattr(profile, "skills", []) if profile else [])
    required = target["required_skills"]
    missing = [skill for skill in required if skill.casefold() not in {item.casefold() for item in skills}]
    same_domain = current_domain == target["domain"]
    difficulty = "Moderate" if same_domain else "Hard" if len(missing) >= 5 else "Medium"
    timeline = "3-6 months" if difficulty == "Moderate" else "6-12 months" if difficulty == "Medium" else "9-18 months"
    probability = max(25, min(88, 78 - len(missing) * 6 + (10 if same_domain else 0) + min(getattr(profile, "weekly_study_hours", 0), 15)))
    roadmap = []
    for index, skill in enumerate(missing[:5], start=1):
        roadmap.append(f"Phase {index}: learn {skill}, complete one proof artifact, and add a resume bullet.")
    if not roadmap:
        roadmap.append("Phase 1: convert existing experience into a target-role portfolio case study.")
    return {
        "from_domain": current_domain,
        "to_domain": target["domain"],
        "difficulty": difficulty,
        "timeline": timeline,
        "required_skills": missing[:8],
        "required_certifications": target["preferred_certifications"][:4],
        "expected_salary": target["salary"],
        "success_probability": round(probability),
        "roadmap": roadmap,
        "why": f"Transition difficulty is based on domain distance, missing role skills, and weekly study hours.",
    }


def learning_recommendations(career_name: str, profile: Any | None = None, missing_skills: list[str] | None = None) -> dict[str, list[str]]:
    career = get_career_knowledge(career_name)
    missing = missing_skills or []
    resources = dict(career["learning_resources"])
    projects = career["target_projects"] or career["portfolio_requirements"]
    resources["projects"] = projects[:4]
    resources["courses"] = [
        f"Focused course on {skill}" for skill in (missing[:3] or career["required_skills"][:3])
    ] + resources.get("courses", [])[:2]
    resources["official_documentation"] = [f"Official docs or standards for {skill}" for skill in career["technical_skills"][:3]]
    return {key: dedupe(values)[:5] for key, values in resources.items()}


def interview_preparation(career_name: str, profile: Any | None = None) -> dict[str, Any]:
    career = get_career_knowledge(career_name)
    projects = getattr(profile, "projects", []) if profile else []
    skills = career["required_skills"][:5]
    return {
        "difficulty_level": "Medium" if projects else "Medium-Hard",
        "hr_questions": [
            f"Why do you want to become a {career_name}?",
            "Tell me about a challenge you handled and what changed because of your action.",
            "Why should we choose you for this role?",
        ],
        "technical_questions": [f"Explain {skill} with a practical example." for skill in skills],
        "case_study_questions": [
            f"Design a small {career_name} solution for a real user or business problem.",
            f"Review a failed {career['domain']} project and recommend improvements.",
        ],
        "behavioral_questions": [
            "Describe a time you worked with feedback.",
            "Describe how you prioritize when deadlines conflict.",
        ],
        "portfolio_review": career["portfolio_requirements"][:4],
        "mock_interview_tips": [
            "Use the STAR format for experience answers.",
            "Keep one strong project story ready with problem, action, and result.",
            "Prepare country-specific salary and company examples.",
        ],
        "checklist": [
            "Resume customized for target role",
            "Two proof projects or case studies",
            "Role keywords visible",
            "Clear answer for career fit and transition story",
        ],
    }


def hiring_companies_for_domain(domain: str) -> list[str]:
    return {
        "Technology": ["Google", "Microsoft", "Amazon", "Infosys", "TCS", "Accenture"],
        "Engineering": ["Larsen & Toubro", "Siemens", "Bosch", "Tata Motors", "Schneider Electric"],
        "Business": ["Deloitte", "PwC", "EY", "KPMG", "Accenture"],
        "Finance": ["JP Morgan", "Goldman Sachs", "HDFC Bank", "ICICI Bank", "Deloitte"],
        "Marketing": ["Ogilvy", "Dentsu", "WPP", "Nykaa", "Zomato"],
        "Law": ["Khaitan & Co", "Cyril Amarchand", "Trilegal", "AZB", "In-house legal teams"],
        "Healthcare": ["Apollo", "Fortis", "Max Healthcare", "Medtronic", "Public health organizations"],
        "Creative": ["Adobe", "Canva", "WPP", "Figma ecosystem studios", "Media agencies"],
    }.get(domain, ["Role-specific employers", "Startups", "Consulting firms", "Government bodies"])


def demanded_cities_for_domain(domain: str) -> list[str]:
    return {
        "Technology": ["Bengaluru", "Hyderabad", "Pune", "Berlin", "Toronto", "Singapore"],
        "Finance": ["Mumbai", "Delhi NCR", "New York", "London", "Singapore", "Dubai"],
        "Law": ["Delhi NCR", "Mumbai", "Bengaluru", "London", "Singapore"],
        "Healthcare": ["Delhi NCR", "Mumbai", "Bengaluru", "Toronto", "Melbourne"],
        "Creative": ["Mumbai", "Bengaluru", "Delhi NCR", "London", "Amsterdam"],
    }.get(domain, ["Delhi NCR", "Mumbai", "Bengaluru", "Toronto", "Dubai"])


def remote_level_for_domain(domain: str) -> str:
    return "High" if domain in {"Technology", "Creative", "Marketing", "Finance"} else "Medium"


def freelance_level_for_domain(domain: str) -> str:
    return "High" if domain in {"Creative", "Marketing", "Technology", "Entrepreneurship"} else "Medium"


def startup_level_for_domain(domain: str) -> str:
    return "High" if domain in {"Technology", "Business", "Finance", "Healthcare", "Entrepreneurship"} else "Medium"


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item and item.casefold() not in seen:
            seen.add(item.casefold())
            result.append(item)
    return result
