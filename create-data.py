### Libraries
import csv
import random
import string

### Create Data
def generate_policy_id(policy_name):
    initials = ''.join(word[0].upper() for word in policy_name.split() if word[0].isalpha())
    number = ''.join(random.choices(string.digits, k=6))
    return f"CDP-{initials}-{number}"

def generate_max_lifetime_benefit():
    return random.choice([1000000, 2000000, 3000000, 5000000, 10000000])

def generate_renewal_terms():
    return random.choice(["Annual", "Bi-annual", "5-year"])

def generate_copayment():
    return random.choice([10, 15, 20, 25, 30, 40, 50])

def generate_coinsurance_rate():
    return random.choice([10, 15, 20, 25, 30])

def generate_deductible():
    return random.choice([500, 1000, 1500, 2000, 2500, 3000, 5000])

policies = [
    {
        "name": "Comprehensive Diabetes Care Plan",
        "conditions": [
            "Type 1 Diabetes",
            "Type 2 Diabetes",
            "Gestational Diabetes",
            "Diabetic Neuropathy",
            "Diabetic Retinopathy"
        ]
    },
    {"name": "Cardiovascular Health Shield",
     "conditions": [
         "Hypertension (High Blood Pressure)",
         "Coronary Artery Disease",
         "Congestive Heart Failure",
         "Arrhythmias",
         "Peripheral Artery Disease"
     ]},
    {"name": "Respiratory Wellness Policy",
     "conditions": [
         "Asthma",
         "Chronic Obstructive Pulmonary Disease (COPD)",
         "Cystic Fibrosis",
         "Pulmonary Fibrosis",
         "Sleep Apnea"
     ]},
    {"name": "Neuro-protective Coverage",
     "conditions": [
         "Multiple Sclerosis",
         "Parkinson's Disease",
         "Alzheimer's Disease",
         "Epilepsy",
         "Chronic Migraine"
     ]},
    {"name": "Autoimmune Disorder Shield",
     "conditions": [
         "Rheumatoid Arthritis",
         "Lupus (Systemic Lupus Erythematosus)",
         "Crohn's Disease",
         "Ulcerative Colitis",
         "Psoriasis"
     ]},
    {"name": "Renal Care Assurance",
     "conditions": [
         "Chronic Kidney Disease",
         "Polycystic Kidney Disease",
         "Glomerulonephritis",
         "Diabetic Nephropathy",
         "Hypertensive Nephropathy"
     ]},
    {"name": "Bone & Joint Health Plan",
     "conditions": [
         "Osteoarthritis",
         "Osteoporosis",
         "Fibromyalgia",
         "Gout",
         "Ankylosing Spondylitis"
     ]},
    {"name": "Comprehensive Cancer Care",
     "conditions": [
         "Various types of cancer (e.g., breast, lung, colorectal)",
         "Leukemia",
         "Lymphoma",
         "Multiple Myeloma",
         "Long-term effects of cancer treatments"
     ]}
]

providers = [
    "Central City Hospital", "Mercy Medical Center", "St. John's Health",
    "University Hospital", "Regional Medical Center", "Family Health Clinic",
    "Wellness Center", "Community Care Clinic", "Specialty Treatment Center",
    "Integrated Health Services", "Dr. Smith Endocrinology", "Dr. Johnson Cardiology",
    "Dr. Williams Pulmonology", "Dr. Brown Neurology", "Dr. Davis Rheumatology",
    "Dr. Miller Nephrology", "Dr. Wilson Orthopedics", "Dr. Moore Oncology"
]

def generate_providers_for_policy(num_providers=5):
    return random.sample(providers, num_providers)

def create_all_csv_files(policy_filename, conditions_filename, providers_filename):
    policy_ids = {}  # To store generated PolicyIDs

    # First, generate PolicyIDs and create the Policy CSV
    with open(policy_filename, 'w', newline='', encoding='utf-8') as policyfile:
        policy_writer = csv.writer(policyfile)
        policy_writer.writerow(['PolicyID', 'PolicyName', 'MaximumLifeTimeBenefit', 'RenewalTerms', 'Copayment', 'CoInsuranceRate', 'Deductible'])
        
        for policy in policies:
            policy_id = generate_policy_id(policy['name'])
            policy_ids[policy['name']] = policy_id  # Store the PolicyID
            policy_writer.writerow([
                policy_id,
                policy['name'],
                generate_max_lifetime_benefit(),
                generate_renewal_terms(),
                generate_copayment(),
                generate_coinsurance_rate(),
                generate_deductible()
            ])

    print(f"CSV file '{policy_filename}' has been created successfully.")

    # Now create the CoveredConditions CSV using the stored PolicyIDs
    with open(conditions_filename, 'w', newline='', encoding='utf-8') as conditionsfile:
        conditions_writer = csv.writer(conditionsfile)
        conditions_writer.writerow(['PolicyID', 'CoveredCondition'])
        
        for policy in policies:
            policy_id = policy_ids[policy['name']]  # Use the stored PolicyID
            for condition in policy['conditions']:
                conditions_writer.writerow([policy_id, condition])

    print(f"CSV file '{conditions_filename}' has been created successfully.")

    # Finally, create the InNetworkProviders CSV using the stored PolicyIDs
    with open(providers_filename, 'w', newline='', encoding='utf-8') as providersfile:
        providers_writer = csv.writer(providersfile)
        providers_writer.writerow(['PolicyID', 'InNetworkProvider'])
        
        for policy in policies:
            policy_id = policy_ids[policy['name']]  # Use the stored PolicyID
            policy_providers = generate_providers_for_policy()
            for provider_name in policy_providers:
                providers_writer.writerow([policy_id, provider_name])

    print(f"CSV file '{providers_filename}' has been created successfully.")

# Create all CSV files
create_all_csv_files('data/Policy.csv', 'data/CoveredConditions.csv', 'data/InNetworkProviders.csv')