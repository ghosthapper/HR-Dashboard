import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_mock_hr_data(n_employees=1500, filename='hr_employee_data.csv'):
    """
    Generate mock HR employee data
    """
    print(f"Generating {n_employees:,} employee records...")
    
    np.random.seed(42)
    
    # Base employee data
    departments = ['R&D', 'Sales', 'HR', 'Finance', 'IT', 'Marketing']
    job_roles = {
        'R&D': ['Research Scientist', 'Laboratory Technician', 'Manufacturing Director', 'Healthcare Representative'],
        'Sales': ['Sales Executive', 'Sales Representative', 'Manager'],
        'HR': ['HR Manager', 'HR Specialist', 'Recruiter'],
        'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager'],
        'IT': ['Software Engineer', 'Data Analyst', 'IT Support'],
        'Marketing': ['Marketing Manager', 'Marketing Specialist', 'Content Creator']
    }
    
    education_fields = ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Other', 'Human Resources']
    education_levels = ['High School', 'Associates Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD']
    marital_status = ['Single', 'Married', 'Divorced']
    gender = ['Male', 'Female']
    travel_frequency = ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']
    age_bands = ['Under 25', '25 - 34', '35 - 44', '45 - 54', 'Over 55']
    
    data = []
    
    for i in range(n_employees):
        emp_age = np.random.normal(35, 10)
        emp_age = max(18, min(65, int(emp_age)))
        
        if emp_age < 25:
            age_band = 'Under 25'
        elif emp_age < 35:
            age_band = '25 - 34'
        elif emp_age < 45:
            age_band = '35 - 44'
        elif emp_age < 55:
            age_band = '45 - 54'
        else:
            age_band = 'Over 55'
        
        dept = np.random.choice(departments)
        job_role = np.random.choice(job_roles[dept])
        
        # Experience
        total_working_years = max(0, int(np.random.normal(emp_age - 22, 5)))
        years_at_company = max(0, min(total_working_years, int(np.random.exponential(3))))
        years_in_role = max(0, min(years_at_company, int(np.random.exponential(2))))
        years_since_promotion = max(0, min(years_in_role, int(np.random.exponential(1.5))))
        years_with_manager = max(0, min(years_at_company, int(np.random.exponential(2))))
        
        # Job characteristics
        job_level = min(4, max(1, int(np.random.gamma(2, 0.7)) + 1))
        monthly_income = int(np.random.normal(5000 + job_level * 2000, 1500))
        monthly_income = max(2000, monthly_income)
        
        # Satisfaction scores
        job_satisfaction = np.random.randint(1, 5)
        environment_satisfaction = np.random.randint(1, 5)
        relationship_satisfaction = np.random.randint(1, 5)
        work_life_balance = np.random.randint(1, 5)
        
        # Calculate attrition probability based on factors
        attrition_prob = 0.1  # Base probability
        
        # Age factor
        if age_band in ['Under 25', '25 - 34']:
            attrition_prob += 0.1
        elif age_band == 'Over 55':
            attrition_prob += 0.05
        
        # Satisfaction factor
        avg_satisfaction = (job_satisfaction + environment_satisfaction + 
                          relationship_satisfaction + work_life_balance) / 4
        attrition_prob += (4 - avg_satisfaction) * 0.15
        
        # Overtime factor
        overtime = np.random.choice(['Yes', 'No'], p=[0.3, 0.7])
        if overtime == 'Yes':
            attrition_prob += 0.1
        
        # Travel factor
        travel = np.random.choice(travel_frequency, p=[0.4, 0.4, 0.2])
        if travel == 'Travel_Frequently':
            attrition_prob += 0.08
        
        # Income factor 
        expected_income = 3000 + job_level * 2500
        if monthly_income < expected_income * 0.8:
            attrition_prob += 0.12
        
        # Years at company factor
        if years_at_company < 2:
            attrition_prob += 0.15
        elif years_at_company > 10:
            attrition_prob -= 0.05
        
        # Distance from home
        distance_from_home = max(1, int(np.random.exponential(8)))
        if distance_from_home > 20:
            attrition_prob += 0.05
        
        # Performance rating
        performance_rating = np.random.choice([1, 2, 3, 4], p=[0.05, 0.15, 0.6, 0.2])
        if performance_rating <= 2:
            attrition_prob += 0.1
        
        # Training factor
        training_times = np.random.randint(0, 7)
        if training_times == 0:
            attrition_prob += 0.05
        
        # Cap probability
        attrition_prob = min(0.8, max(0.02, attrition_prob))
        
        # Determine attrition
        attrition = 'Yes' if np.random.random() < attrition_prob else 'No'
        cf_attrition = 'Ex-Employees' if attrition == 'Yes' else 'Current Employees'
        cf_current_employee = 0 if attrition == 'Yes' else 1
        
        # Additional fields
        marital = np.random.choice(marital_status)
        emp_gender = np.random.choice(gender)
        education = np.random.choice(education_levels, p=[0.15, 0.25, 0.35, 0.2, 0.05])
        edu_field = np.random.choice(education_fields)
        
        # Stock options
        stock_option_level = np.random.choice([0, 1, 2, 3], 
                                            p=[0.6, 0.25, 0.1, 0.05] if job_level < 3 
                                            else [0.3, 0.3, 0.3, 0.1])
        
        # Companies worked
        num_companies = max(1, min(8, int(np.random.exponential(1.5)) + 1))
        
        # Salary hike percentage
        percent_salary_hike = max(0, int(np.random.normal(15, 5)))
        
        # Job involvement
        job_involvement = np.random.randint(1, 5)
        
        # Hourly and daily rates
        hourly_rate = max(30, int(np.random.normal(65, 20)))
        daily_rate = max(100, int(np.random.normal(800, 300)))
        monthly_rate = max(5000, int(np.random.normal(15000, 5000)))
        
        data.append({
            'Employee_Number': f'STAFF-{i+1}',
            'Age': emp_age,
            'CF_age_band': age_band,
            'Gender': emp_gender,
            'Marital_Status': marital,
            'Department': dept,
            'Job_Role': job_role,
            'Job_Level': job_level,
            'Education': education,
            'Education_Field': edu_field,
            'Total_Working_Years': total_working_years,
            'Years_At_Company': years_at_company,
            'Years_In_Current_Role': years_in_role,
            'Years_Since_Last_Promotion': years_since_promotion,
            'Years_With_Curr_Manager': years_with_manager,
            'Monthly_Income': monthly_income,
            'Percent_Salary_Hike': percent_salary_hike,
            'Stock_Option_Level': stock_option_level,
            'Job_Satisfaction': job_satisfaction,
            'Environment_Satisfaction': environment_satisfaction,
            'Relationship_Satisfaction': relationship_satisfaction,
            'Work_Life_Balance': work_life_balance,
            'Job_Involvement': job_involvement,
            'Performance_Rating': performance_rating,
            'Over_Time': overtime,
            'Business_Travel': travel,
            'Distance_From_Home': distance_from_home,
            'Training_Times_Last_Year': training_times,
            'Num_Companies_Worked': num_companies,
            'Attrition': attrition,
            'CF_attrition_label': cf_attrition,
            'CF_current_Employee': cf_current_employee,
            'Hourly_Rate': hourly_rate,
            'Daily_Rate': daily_rate,
            'Monthly_Rate': monthly_rate,
            'Employee_Count': 1,
            'Standard_Hours': 80,
            'Over18': 'Y'
        })
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"HR data generated successfully!")
    print(f"File saved as: {filename}")
    print(f"Total employees: {len(df):,}")
    
    return df

def check_and_generate_data(filename='hr_employee_data.csv'):
    """Check if CSV file exists, if not generate it"""
    if not os.path.exists(filename):
        print("CSV file not found. Generating new HR dataset...")
        generate_mock_hr_data(filename=filename)
    else:
        print(f"Found existing CSV file: {filename}")
        # Show file info
        df = pd.read_csv(filename)
        print(f"Records in file: {len(df):,}")

# Run data generation if this script is executed directly
if __name__ == "__main__":
    print("HR EMPLOYEE DATA GENERATOR")
    check_and_generate_data()
    print("Data generation complete!")
    print("Now you can run: streamlit run hr_dashboard.py")