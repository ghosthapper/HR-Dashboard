import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(page_title="HR Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

# Function to generate mock HR data
@st.cache_data
def generate_mock_data(n_employees=1500):
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
        # Demographics
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
        
        # Experience and tenure
        total_working_years = max(0, int(np.random.normal(emp_age - 22, 5)))
        years_at_company = max(0, min(total_working_years, int(np.random.exponential(3))))
        years_in_role = max(0, min(years_at_company, int(np.random.exponential(2))))
        years_since_promotion = max(0, min(years_in_role, int(np.random.exponential(1.5))))
        years_with_manager = max(0, min(years_at_company, int(np.random.exponential(2))))
        
        # Job characteristics
        job_level = min(4, max(1, int(np.random.gamma(2, 0.7)) + 1))
        monthly_income = int(np.random.normal(5000 + job_level * 2000, 1500))
        monthly_income = max(2000, monthly_income)
        
        # Satisfaction scores (1-4 scale)
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
        
        # Satisfaction factor (lower satisfaction = higher attrition)
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
        
        # Income factor (relative to job level)
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
        
        # Stock options (higher level = more likely to have)
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
    
    return pd.DataFrame(data)

# Generate data
df = generate_mock_data()

# Dashboard Title
st.title("🏢 HR Attrition Analytics Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")
selected_dept = st.sidebar.multiselect("Department", options=df['Department'].unique(), default=df['Department'].unique())
selected_age = st.sidebar.multiselect("Age Band", options=df['CF_age_band'].unique(), default=df['CF_age_band'].unique())
income_range = st.sidebar.slider("Monthly Income Range", int(df['Monthly_Income'].min()), int(df['Monthly_Income'].max()), 
                                 (int(df['Monthly_Income'].min()), int(df['Monthly_Income'].max())))

# Filter data
filtered_df = df[
    (df['Department'].isin(selected_dept)) & 
    (df['CF_age_band'].isin(selected_age)) &
    (df['Monthly_Income'] >= income_range[0]) &
    (df['Monthly_Income'] <= income_range[1])
]

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

total_employees = len(filtered_df)
current_employees = len(filtered_df[filtered_df['Attrition'] == 'No'])
attrition_count = len(filtered_df[filtered_df['Attrition'] == 'Yes'])
attrition_rate = (attrition_count / total_employees * 100) if total_employees > 0 else 0
avg_tenure = filtered_df['Years_At_Company'].mean()

with col1:
    st.metric("Total Employees", f"{total_employees:,}")
with col2:
    st.metric("Current Employees", f"{current_employees:,}")
with col3:
    st.metric("Attrition Count", f"{attrition_count:,}")
with col4:
    st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
with col5:
    st.metric("Avg. Tenure", f"{avg_tenure:.1f} years")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    # Attrition by Department
    dept_attrition = filtered_df.groupby(['Department', 'Attrition']).size().unstack(fill_value=0)
    dept_attrition['Total'] = dept_attrition.sum(axis=1)
    dept_attrition['Attrition_Rate'] = (dept_attrition['Yes'] / dept_attrition['Total'] * 100).round(1)
    
    fig1 = px.bar(dept_attrition.reset_index(), x='Department', y='Attrition_Rate',
                  title='Attrition Rate by Department', color='Attrition_Rate',
                  color_continuous_scale='Reds')
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Attrition by Age Band
    age_attrition = filtered_df.groupby(['CF_age_band', 'Attrition']).size().unstack(fill_value=0)
    age_attrition['Total'] = age_attrition.sum(axis=1)
    age_attrition['Attrition_Rate'] = (age_attrition['Yes'] / age_attrition['Total'] * 100).round(1)
    
    fig2 = px.bar(age_attrition.reset_index(), x='CF_age_band', y='Attrition_Rate',
                  title='Attrition Rate by Age Band', color='Attrition_Rate',
                  color_continuous_scale='Blues')
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    # Satisfaction vs Attrition
    satisfaction_cols = ['Job_Satisfaction', 'Environment_Satisfaction', 
                        'Relationship_Satisfaction', 'Work_Life_Balance']
    
    sat_data = []
    for col in satisfaction_cols:
        for rating in range(1, 5):
            subset = filtered_df[filtered_df[col] == rating]
            if len(subset) > 0:
                attrition_rate = (subset['Attrition'] == 'Yes').mean() * 100
                sat_data.append({
                    'Satisfaction_Type': col.replace('_', ' '),
                    'Rating': rating,
                    'Attrition_Rate': attrition_rate,
                    'Count': len(subset)
                })
    
    sat_df = pd.DataFrame(sat_data)
    
    fig3 = px.scatter(sat_df, x='Rating', y='Attrition_Rate', 
                      color='Satisfaction_Type', size='Count',
                      title='Satisfaction Ratings vs Attrition Rate')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Income Distribution by Attrition
    fig4 = px.box(filtered_df, x='Attrition', y='Monthly_Income',
                  title='Monthly Income Distribution by Attrition Status',
                  color='Attrition')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# Charts Row 3
col1, col2 = st.columns(2)

with col1:
    # Tenure vs Attrition
    tenure_bins = pd.cut(filtered_df['Years_At_Company'], bins=5, precision=0)
    tenure_attrition = filtered_df.groupby([tenure_bins, 'Attrition']).size().unstack(fill_value=0)
    tenure_attrition['Total'] = tenure_attrition.sum(axis=1)
    tenure_attrition['Attrition_Rate'] = (tenure_attrition['Yes'] / tenure_attrition['Total'] * 100).round(1)
    
    fig5 = px.line(tenure_attrition.reset_index(), x='Years_At_Company', y='Attrition_Rate',
                   title='Attrition Rate by Years at Company', markers=True)
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Overtime and Travel Impact
    overtime_travel = filtered_df.groupby(['Over_Time', 'Business_Travel', 'Attrition']).size().unstack(fill_value=0)
    overtime_travel['Total'] = overtime_travel.sum(axis=1)
    overtime_travel['Attrition_Rate'] = (overtime_travel['Yes'] / overtime_travel['Total'] * 100).round(1)
    overtime_travel_reset = overtime_travel.reset_index()
    overtime_travel_reset['Category'] = overtime_travel_reset['Over_Time'] + ' + ' + overtime_travel_reset['Business_Travel']
    
    fig6 = px.bar(overtime_travel_reset, x='Category', y='Attrition_Rate',
                  title='Attrition Rate by Overtime & Travel', color='Attrition_Rate',
                  color_continuous_scale='Oranges')
    fig6.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig6, use_container_width=True)

# Summary insights
st.markdown("---")
st.subheader("🔍 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**High Risk Factors:**")
    high_risk_overtime = filtered_df[filtered_df['Over_Time'] == 'Yes']['Attrition'].value_counts(normalize=True)['Yes'] * 100
    high_risk_travel = filtered_df[filtered_df['Business_Travel'] == 'Travel_Frequently']['Attrition'].value_counts(normalize=True)['Yes'] * 100
    
    if 'Yes' in high_risk_overtime:
        st.write(f"• Overtime workers: {high_risk_overtime:.1f}% attrition rate")
    if 'Yes' in high_risk_travel:
        st.write(f"• Frequent travelers: {high_risk_travel:.1f}% attrition rate")
    
    low_satisfaction = filtered_df[filtered_df['Job_Satisfaction'] <= 2]
    if len(low_satisfaction) > 0:
        low_sat_attrition = (low_satisfaction['Attrition'] == 'Yes').mean() * 100
        st.write(f"• Low job satisfaction: {low_sat_attrition:.1f}% attrition rate")

with col2:
    st.markdown("**Retention Factors:**")
    high_performers = filtered_df[filtered_df['Performance_Rating'] >= 3]
    if len(high_performers) > 0:
        high_perf_retention = (high_performers['Attrition'] == 'No').mean() * 100
        st.write(f"• High performers: {high_perf_retention:.1f}% retention rate")
    
    long_tenure = filtered_df[filtered_df['Years_At_Company'] >= 5]
    if len(long_tenure) > 0:
        long_tenure_retention = (long_tenure['Attrition'] == 'No').mean() * 100
        st.write(f"• 5+ years tenure: {long_tenure_retention:.1f}% retention rate")
    
    stock_options = filtered_df[filtered_df['Stock_Option_Level'] > 0]
    if len(stock_options) > 0:
        stock_retention = (stock_options['Attrition'] == 'No').mean() * 100
        st.write(f"• Stock options holders: {stock_retention:.1f}% retention rate")

# Data table
st.markdown("---")
st.subheader("📋 Employee Data Summary")
summary_cols = ['Department', 'Job_Role', 'CF_age_band', 'Monthly_Income', 
                'Years_At_Company', 'Job_Satisfaction', 'Attrition']
st.dataframe(filtered_df[summary_cols].head(20), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")