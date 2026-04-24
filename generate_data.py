import pandas as pd
import numpy as np
import random

def generate_highly_realistic_data(num_samples=2000):
    np.random.seed(99)
    random.seed(99)
    
    # Industries and their legit descriptions
    industries = {
        "Technology": ["Cloud Computing", "AI Research", "Cybersecurity", "Blockchain"],
        "Finance": ["Investment Banking", "Risk Management", "Asset Management", "FinTech"],
        "Healthcare": ["Telemedicine", "Clinical Research", "Medical Devices", "Pharmaceuticals"],
        "Education": ["EdTech", "Higher Education", "K-12", "Special Education"],
        "Creative": ["Graphic Design", "Video Production", "Digital Marketing", "Content Creation"]
    }
    
    locations = ["London, UK", "New York, NY", "Austin, TX", "Berlin, DE", "Toronto, CA", "Sydney, AU", "Remote"]
    
    data = []
    for i in range(num_samples):
        # 30% Fraudulent, 70% Legitimate
        is_fraudulent = np.random.choice([0, 1], p=[0.7, 0.3])
        
        industry_name = random.choice(list(industries.keys()))
        sub_industry = random.choice(industries[industry_name])
        
        if is_fraudulent:
            # Types of Scams
            scam_type = random.choice(["Phishing", "Money Mule", "Check Scam", "Personal Info Harvest"])
            
            if scam_type == "Phishing":
                title = f"Remote {random.choice(['Data Entry', 'Virtual Assistant', 'Admin Assistant'])}"
                company_profile = "We are a global logistics company expanding rapidly. We value speed and efficiency."
                description = "Work from the comfort of your home. High hourly pay ($45/hr). No experience needed. Immediate start."
                requirements = "Must be able to follow instructions carefully. Basic computer knowledge. Stable internet."
                benefits = "Flexible hours, Weekly pay via Zelle or CashApp, Home office equipment provided."
            
            elif scam_type == "Money Mule":
                title = f"{random.choice(['Regional', 'Local'])} Payment Processor"
                company_profile = "International trade company helping small businesses with global payments."
                description = "Receive payments from our clients and forward them to our international branches. You keep 10% commission on every transaction."
                requirements = "Personal bank account required. Must be available during business hours to process transfers."
                benefits = "Commission-based pay. Potential to earn $2000+ weekly."
            
            elif scam_type == "Check Scam":
                title = "Mystery Shopper / Quality Control"
                company_profile = "Consumer research group evaluating retail standards across the country."
                description = "Visit local stores, perform specific tasks, and report back. We will send you a check for funds to purchase items."
                requirements = "Reliable transportation. Smartphone for reporting. Honest and detail-oriented."
                benefits = "Keep the products you buy. Reimbursement plus $300 fee per assignment."
            
            else: # Personal Info Harvest
                title = "Junior Software Developer (Remote)"
                company_profile = "Innovative startup focused on next-gen social platforms."
                description = "Looking for passionate developers. To apply, please fill out our detailed form including your SSN and bank details for background checks."
                requirements = "Knowledge of React or Node.js. Willingness to learn."
                benefits = "Stock options, Remote work, Competitive salary."

        else:
            # Legitimate Jobs
            title = f"{random.choice(['Senior', 'Lead', 'Principal'])} {sub_industry} Specialist"
            company_profile = f"A well-established leader in the {industry_name} sector with over 20 years of experience. Committed to excellence and employee growth."
            description = f"We are seeking a {title} to join our {industry_name} division. You will work on {sub_industry} projects, mentor junior staff, and drive innovation."
            requirements = "8+ years of experience in the field. Relevant certifications. Strong analytical and problem-solving skills."
            benefits = "Full health coverage, 401k with matching, Paid Parental Leave, Annual Bonus."

        location = random.choice(locations)
        
        data.append({
            "job_id": i + 1,
            "title": title,
            "location": location,
            "department": random.choice(["Engineering", "Operations", "Finance", "Marketing"]) if random.random() > 0.2 else np.nan,
            "salary_range": f"{random.randint(50, 90)}k-{random.randint(100, 200)}k" if random.random() > 0.3 else np.nan,
            "company_profile": company_profile,
            "description": description,
            "requirements": requirements,
            "benefits": benefits,
            "telecommuting": 1 if "remote" in title.lower() or "remote" in location.lower() else 0,
            "has_company_logo": 1 if not is_fraudulent else np.random.randint(0, 2),
            "has_questions": np.random.randint(0, 2),
            "employment_type": "Full-time" if not is_fraudulent else random.choice(["Part-time", "Contract"]),
            "required_experience": "Mid-Senior level" if not is_fraudulent else "Entry level",
            "required_education": "Bachelor's Degree" if not is_fraudulent else "Unspecified",
            "industry": industry_name,
            "function": "Information Technology" if "Software" in title else "General Management",
            "fraudulent": is_fraudulent
        })
    
    df = pd.DataFrame(data)
    df.to_csv("fake_job_postings.csv", index=False)
    print(f"Generated {num_samples} highly realistic mixed job postings.")

if __name__ == "__main__":
    generate_highly_realistic_data()
