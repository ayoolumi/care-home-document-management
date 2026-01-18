"""
Sample Data Generator for Care Home Document Management System
Creates realistic demo documents for testing and demonstration
"""

import database as db
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample documents for demonstration"""
    
    # Get categories
    categories = db.get_categories()
    category_dict = {cat['name']: cat['id'] for cat in categories}
    
    # Sample documents with realistic care home data
    sample_documents = [
        # Policies & Procedures
        {
            'title': 'Fire Safety Policy and Procedures',
            'description': 'Comprehensive fire safety policy including evacuation procedures, fire drill schedules, and emergency contacts.',
            'category': 'Policies & Procedures',
            'file_name': 'Fire_Safety_Policy_2023.pdf',
            'review_days': 365,
            'expiry_days': 400
        },
        {
            'title': 'Medication Administration Policy',
            'description': 'Guidelines for safe medication storage, administration, and documentation in accordance with NICE guidelines.',
            'category': 'Policies & Procedures',
            'file_name': 'Medication_Policy_v3.pdf',
            'review_days': 180,
            'expiry_days': 365
        },
        {
            'title': 'Safeguarding Adults Policy',
            'description': 'Protection of vulnerable adults policy aligned with Care Act 2014 requirements.',
            'category': 'Policies & Procedures',
            'file_name': 'Safeguarding_Policy_2023.pdf',
            'review_days': 365,
            'expiry_days': 730
        },
        {
            'title': 'Infection Prevention and Control Policy',
            'description': 'IPC protocols including hand hygiene, PPE usage, and outbreak management procedures.',
            'category': 'Policies & Procedures',
            'file_name': 'IPC_Policy_Updated.pdf',
            'review_days': 90,
            'expiry_days': 365
        },
        
        # Health & Safety
        {
            'title': 'Risk Assessment - Kitchen Area',
            'description': 'Comprehensive risk assessment for main kitchen including COSHH and food safety considerations.',
            'category': 'Health & Safety',
            'file_name': 'Kitchen_Risk_Assessment.pdf',
            'review_days': 180,
            'expiry_days': 365
        },
        {
            'title': 'Manual Handling Risk Assessment',
            'description': 'Assessment of manual handling risks for resident care activities with control measures.',
            'category': 'Health & Safety',
            'file_name': 'Manual_Handling_RA_2023.pdf',
            'review_days': 365,
            'expiry_days': 400
        },
        {
            'title': 'COSHH Assessment - Cleaning Products',
            'description': 'Control of Substances Hazardous to Health assessment for all cleaning chemicals.',
            'category': 'Health & Safety',
            'file_name': 'COSHH_Cleaning_Products.pdf',
            'review_days': 365,
            'expiry_days': 730
        },
        
        # Staff Training
        {
            'title': 'MAPA Training Certificate - Team A',
            'description': 'Management of Actual and Potential Aggression certification for care team.',
            'category': 'Staff Training',
            'file_name': 'MAPA_Certificates_TeamA.pdf',
            'review_days': 365,
            'expiry_days': 365
        },
        {
            'title': 'First Aid Training Records Q3 2023',
            'description': 'First aid at work certification records for all trained staff members.',
            'category': 'Staff Training',
            'file_name': 'FirstAid_Q3_2023.pdf',
            'review_days': 1095,
            'expiry_days': 1095
        },
        {
            'title': 'Food Hygiene Level 2 Certificates',
            'description': 'Food hygiene certification for kitchen and care staff involved in food handling.',
            'category': 'Staff Training',
            'file_name': 'Food_Hygiene_Certs.pdf',
            'review_days': 1095,
            'expiry_days': 1095
        },
        
        # Quality Assurance
        {
            'title': 'Internal Audit Report - Q2 2023',
            'description': 'Quarterly internal audit findings and improvement action plan.',
            'category': 'Quality Assurance',
            'file_name': 'Internal_Audit_Q2_2023.pdf',
            'review_days': 90,
            'expiry_days': None
        },
        {
            'title': 'Resident Satisfaction Survey Results',
            'description': 'Annual resident and family satisfaction survey analysis and action points.',
            'category': 'Quality Assurance',
            'file_name': 'Satisfaction_Survey_2023.pdf',
            'review_days': 365,
            'expiry_days': None
        },
        {
            'title': 'Care Inspectorate Action Plan',
            'description': 'Improvement action plan following latest Care Inspectorate visit.',
            'category': 'Quality Assurance',
            'file_name': 'CI_Action_Plan_2023.pdf',
            'review_days': 30,
            'expiry_days': 180
        },
        
        # HR Documents
        {
            'title': 'Staff Handbook 2023',
            'description': 'Employee handbook covering terms, conditions, policies and procedures.',
            'category': 'HR Documents',
            'file_name': 'Staff_Handbook_2023.pdf',
            'review_days': 365,
            'expiry_days': None
        },
        {
            'title': 'PVG Scheme Records',
            'description': 'Protecting Vulnerable Groups scheme membership records for all staff.',
            'category': 'HR Documents',
            'file_name': 'PVG_Records_Master.xlsx',
            'review_days': 365,
            'expiry_days': None
        },
        
        # Meeting Minutes
        {
            'title': 'Staff Meeting Minutes - June 2023',
            'description': 'Monthly all-staff meeting minutes including action items and decisions.',
            'category': 'Meeting Minutes',
            'file_name': 'Staff_Meeting_June2023.docx',
            'review_days': None,
            'expiry_days': None
        },
        {
            'title': 'Management Team Meeting - Q2 Review',
            'description': 'Quarterly management meeting covering performance, staffing, and quality.',
            'category': 'Meeting Minutes',
            'file_name': 'Management_Q2_Review.docx',
            'review_days': None,
            'expiry_days': None
        },
        
        # Regulatory
        {
            'title': 'Care Inspectorate Registration Certificate',
            'description': 'Official registration certificate from Care Inspectorate Scotland.',
            'category': 'Regulatory',
            'file_name': 'CI_Registration_Cert.pdf',
            'review_days': 365,
            'expiry_days': None
        },
        {
            'title': 'SSSC Registration Confirmation',
            'description': 'Scottish Social Services Council registration for the service.',
            'category': 'Regulatory',
            'file_name': 'SSSC_Registration.pdf',
            'review_days': 365,
            'expiry_days': None
        },
        
        # Templates & Forms
        {
            'title': 'Incident Report Form Template',
            'description': 'Blank incident/accident report form for staff use.',
            'category': 'Templates & Forms',
            'file_name': 'Incident_Report_Template.docx',
            'review_days': 365,
            'expiry_days': None
        },
        {
            'title': 'Care Plan Review Template',
            'description': 'Standard template for conducting and documenting care plan reviews.',
            'category': 'Templates & Forms',
            'file_name': 'Care_Plan_Review_Template.docx',
            'review_days': 365,
            'expiry_days': None
        },
    ]
    
    # Add documents with varied dates
    for doc in sample_documents:
        # Random past date for creation (within last 6 months)
        days_ago = random.randint(7, 180)
        
        # Calculate review and expiry dates
        review_date = None
        expiry_date = None
        
        if doc.get('review_days'):
            review_date = (datetime.now() + timedelta(days=random.randint(-30, doc['review_days']))).strftime('%Y-%m-%d')
        
        if doc.get('expiry_days'):
            expiry_date = (datetime.now() + timedelta(days=random.randint(7, doc['expiry_days']))).strftime('%Y-%m-%d')
        
        # Generate dummy file content
        file_content = f"This is a placeholder for: {doc['title']}\n\nGenerated for demonstration purposes.".encode()
        file_type = doc['file_name'].split('.')[-1]
        
        # Add to database
        db.add_document(
            title=doc['title'],
            description=doc['description'],
            category_id=category_dict.get(doc['category']),
            file_name=doc['file_name'],
            file_type=file_type,
            file_size=len(file_content),
            file_data=file_content,
            uploaded_by='System Admin',
            review_date=review_date,
            expiry_date=expiry_date,
            tags=[doc['category'].lower().replace(' ', '-'), 'sample']
        )
    
    print(f"✅ Added {len(sample_documents)} sample documents to the database")


if __name__ == "__main__":
    generate_sample_data()
