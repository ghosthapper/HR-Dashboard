# ============================================================================
# HR ATTRITION DASHBOARD
# ============================================================================
# File: hr_dashboard.py
# Purpose: Interactive HR Analytics Dashboard using Streamlit
# Usage: streamlit run hr_dashboard.py
# Requirements: Run generate_hr_data.py first to create the CSV file

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="HR Attrition Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🏢"
)

# Load data function
@st.cache_data
def load_hr_data(filename='hr_employee_data.csv'):
    """Load HR data from CSV file"""
    if not os.path.exists(filename):
        st.error(f"❌ Data file '{filename}' not found!")
        st.error("Please run the data generation script first to create the CSV file.")
        st.info("💡 Run: `python generate_hr_data.py` in your terminal")
        st.stop()
    
    try:
        df = pd.read_csv(filename)
        st.success(f"✅ Successfully loaded {len(df):,} employee records from {filename}")
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

# Load the data
df = load_hr_data()

# Dashboard Title
st.title("🏢 HR Attrition Analytics Dashboard")
st.markdown("*Comprehensive analysis of employee attrition patterns and key insights*")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")
st.sidebar.markdown("*Filter the data to focus on specific employee segments*")

selected_dept = st.sidebar.multiselect(
    "🏢 Department", 
    options=df['Department'].unique(), 
    default=df['Department'].unique(),
    help="Select one or more departments to analyze"
)

selected_age = st.sidebar.multiselect(
    "👥 Age Band", 
    options=df['CF_age_band'].unique(), 
    default=df['CF_age_band'].unique(),
    help="Filter by employee age groups"
)

income_range = st.sidebar.slider(
    "💰 Monthly Income Range", 
    int(df['Monthly_Income'].min()), 
    int(df['Monthly_Income'].max()), 
    (int(df['Monthly_Income'].min()), int(df['Monthly_Income'].max())),
    help="Select income range to analyze"
)

job_level_filter = st.sidebar.multiselect(
    "📈 Job Level",
    options=sorted(df['Job_Level'].unique()),
    default=sorted(df['Job_Level'].unique()),
    help="Filter by job level (1=Entry, 4=Senior)"
)

# Advanced filters in expander
with st.sidebar.expander("🔍 Advanced Filters"):
    performance_filter = st.multiselect(
        "Performance Rating",
        options=sorted(df['Performance_Rating'].unique()),
        default=sorted(df['Performance_Rating'].unique())
    )
    
    travel_filter = st.multiselect(
        "Business Travel",
        options=df['Business_Travel'].unique(),
        default=df['Business_Travel'].unique()
    )

# Filter data
filtered_df = df[
    (df['Department'].isin(selected_dept)) & 
    (df['CF_age_band'].isin(selected_age)) &
    (df['Monthly_Income'] >= income_range[0]) &
    (df['Monthly_Income'] <= income_range[1]) &
    (df['Job_Level'].isin(job_level_filter)) &
    (df['Performance_Rating'].isin(performance_filter)) &
    (df['Business_Travel'].isin(travel_filter))
]

# Data validation
if len(filtered_df) == 0:
    st.warning("⚠️ No data matches your filter criteria. Please adjust your filters.")
    st.stop()

# Key Metrics Row
st.subheader("📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

total_employees = len(filtered_df)
current_employees = len(filtered_df[filtered_df['Attrition'] == 'No'])
attrition_count = len(filtered_df[filtered_df['Attrition'] == 'Yes'])
attrition_rate = (attrition_count / total_employees * 100) if total_employees > 0 else 0
avg_tenure = filtered_df['Years_At_Company'].mean()

with col1:
    st.metric(
        "Total Employees", 
        f"{total_employees:,}",
        help="Total number of employees in filtered data"
    )
with col2:
    st.metric(
        "Current Employees", 
        f"{current_employees:,}",
        help="Number of active employees"
    )
with col3:
    st.metric(
        "Attrition Count", 
        f"{attrition_count:,}",
        help="Number of employees who left"
    )
with col4:
    delta_color = "inverse" if attrition_rate > 15 else "normal"
    st.metric(
        "Attrition Rate", 
        f"{attrition_rate:.1f}%",
        help="Percentage of employees who left the company"
    )
with col5:
    st.metric(
        "Avg. Tenure", 
        f"{avg_tenure:.1f} years",
        help="Average years employees stay with the company"
    )

st.markdown("---")

# Charts Row 1
st.subheader("📈 Departmental & Demographic Analysis")
col1, col2 = st.columns(2)

with col1:
    # Attrition by Department
    dept_attrition = filtered_df.groupby(['Department', 'Attrition']).size().unstack(fill_value=0)
    dept_attrition['Total'] = dept_attrition.sum(axis=1)
    dept_attrition['Attrition_Rate'] = (dept_attrition['Yes'] / dept_attrition['Total'] * 100).round(1)
    
    fig1 = px.bar(
        dept_attrition.reset_index(), 
        x='Department', 
        y='Attrition_Rate',
        title='Attrition Rate by Department (%)', 
        color='Attrition_Rate',
        color_continuous_scale='Reds',
        text='Attrition_Rate'
    )
    fig1.update_traces(texttemplate='%{text}%', textposition='outside')
    fig1.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Attrition by Age Band
    age_attrition = filtered_df.groupby(['CF_age_band', 'Attrition']).size().unstack(fill_value=0)
    age_attrition['Total'] = age_attrition.sum(axis=1)
    age_attrition['Attrition_Rate'] = (age_attrition['Yes'] / age_attrition['Total'] * 100).round(1)
    
    # Reorder age bands logically
    age_order = ['Under 25', '25 - 34', '35 - 44', '45 - 54', 'Over 55']
    age_attrition_reset = age_attrition.reset_index()
    age_attrition_reset['CF_age_band'] = pd.Categorical(
        age_attrition_reset['CF_age_band'], 
        categories=age_order, 
        ordered=True
    )
    age_attrition_reset = age_attrition_reset.sort_values('CF_age_band')
    
    fig2 = px.bar(
        age_attrition_reset, 
        x='CF_age_band', 
        y='Attrition_Rate',
        title='Attrition Rate by Age Band (%)', 
        color='Attrition_Rate',
        color_continuous_scale='Blues',
        text='Attrition_Rate'
    )
    fig2.update_traces(texttemplate='%{text}%', textposition='outside')
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
st.subheader("💡 Satisfaction & Compensation Analysis")
col1, col2 = st.columns(2)

with col1:
    # Satisfaction vs Attrition Heatmap
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
    
    if sat_data:
        sat_df = pd.DataFrame(sat_data)
        
        fig3 = px.scatter(
            sat_df, 
            x='Rating', 
            y='Attrition_Rate', 
            color='Satisfaction_Type', 
            size='Count',
            title='Satisfaction Ratings vs Attrition Rate',
            hover_data=['Count']
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Income Distribution by Attrition
    fig4 = px.box(
        filtered_df, 
        x='Attrition', 
        y='Monthly_Income',
        title='Monthly Income Distribution by Attrition Status',
        color='Attrition',
        color_discrete_map={'Yes': '#ff7f7f', 'No': '#7fbf7f'}
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# Charts Row 3
st.subheader("⏱️ Tenure & Work-Life Balance Impact")
col1, col2 = st.columns(2)

# Replace the tenure analysis section (around lines 270-284) with this fixed version:

with col1:
    # Tenure vs Attrition - FIXED VERSION
    if filtered_df['Years_At_Company'].max() > 0:
        # Create tenure bins and convert to string labels
        tenure_bins = pd.cut(filtered_df['Years_At_Company'], bins=5, precision=0)
        
        # Convert intervals to string labels for JSON serialization
        tenure_labels = tenure_bins.astype(str)
        
        # Create a temporary dataframe for grouping
        temp_df = filtered_df.copy()
        temp_df['Tenure_Range'] = tenure_labels
        
        tenure_attrition = temp_df.groupby(['Tenure_Range', 'Attrition']).size().unstack(fill_value=0)
        
        if len(tenure_attrition) > 0:
            tenure_attrition['Total'] = tenure_attrition.sum(axis=1)
            tenure_attrition['Attrition_Rate'] = (tenure_attrition['Yes'] / tenure_attrition['Total'] * 100).round(1)
            
            # Reset index to get tenure ranges as a column
            tenure_plot_data = tenure_attrition.reset_index()
            
            fig5 = px.line(
                tenure_plot_data, 
                x='Tenure_Range', 
                y='Attrition_Rate',
                title='Attrition Rate by Years at Company', 
                markers=True,
                line_shape='spline'
            )
            fig5.update_layout(
                height=400,
                xaxis_title="Years at Company (Range)",
                xaxis_tickangle=-45  # Rotate labels for better readability
            )
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("Insufficient data for tenure analysis")
    else:
        st.info("No tenure data available for analysis")

with col2:
    # Overtime and Travel Impact
    overtime_travel = filtered_df.groupby(['Over_Time', 'Business_Travel', 'Attrition']).size().unstack(fill_value=0)
    
    if len(overtime_travel) > 0:
        overtime_travel['Total'] = overtime_travel.sum(axis=1)
        overtime_travel['Attrition_Rate'] = (overtime_travel['Yes'] / overtime_travel['Total'] * 100).round(1)
        overtime_travel_reset = overtime_travel.reset_index()
        overtime_travel_reset['Category'] = (overtime_travel_reset['Over_Time'] + 
                                           ' OT + ' + 
                                           overtime_travel_reset['Business_Travel'])
        
        fig6 = px.bar(
            overtime_travel_reset, 
            x='Category', 
            y='Attrition_Rate',
            title='Attrition Rate by Overtime & Travel (%)', 
            color='Attrition_Rate',
            color_continuous_scale='Oranges',
            text='Attrition_Rate'
        )
        fig6.update_traces(texttemplate='%{text}%', textposition='outside')
        fig6.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)

# Performance Analysis
st.subheader("🎯 Performance & Development Analysis")
col1, col2 = st.columns(2)

with col1:
    # Performance Rating vs Attrition
    perf_attrition = filtered_df.groupby(['Performance_Rating', 'Attrition']).size().unstack(fill_value=0)
    perf_attrition['Total'] = perf_attrition.sum(axis=1)
    perf_attrition['Attrition_Rate'] = (perf_attrition['Yes'] / perf_attrition['Total'] * 100).round(1)
    
    fig7 = px.bar(
        perf_attrition.reset_index(),
        x='Performance_Rating',
        y='Attrition_Rate',
        title='Attrition Rate by Performance Rating',
        color='Attrition_Rate',
        color_continuous_scale='Viridis',
        text='Attrition_Rate'
    )
    fig7.update_traces(texttemplate='%{text}%', textposition='outside')
    fig7.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    # Training vs Attrition
    training_attrition = filtered_df.groupby(['Training_Times_Last_Year', 'Attrition']).size().unstack(fill_value=0)
    training_attrition['Total'] = training_attrition.sum(axis=1)
    training_attrition['Attrition_Rate'] = (training_attrition['Yes'] / training_attrition['Total'] * 100).round(1)
    
    fig8 = px.bar(
        training_attrition.reset_index(),
        x='Training_Times_Last_Year',
        y='Attrition_Rate',
        title='Attrition Rate by Training Times Last Year',
        color='Attrition_Rate',
        color_continuous_scale='Purples',
        text='Attrition_Rate'
    )
    fig8.update_traces(texttemplate='%{text}%', textposition='outside')
    fig8.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)

# Advanced Analytics
st.subheader("🔍 Advanced Analytics & Insights")

# Correlation Analysis
st.subheader("📊 Factor Correlation Matrix")
numeric_cols = ['Monthly_Income', 'Years_At_Company', 'Job_Satisfaction', 
                'Environment_Satisfaction', 'Work_Life_Balance', 'Job_Level',
                'Performance_Rating', 'Training_Times_Last_Year']

# Create binary attrition column for correlation
filtered_df_corr = filtered_df.copy()
filtered_df_corr['Attrition_Binary'] = (filtered_df_corr['Attrition'] == 'Yes').astype(int)

# Calculate correlations with attrition
correlations = []
for col in numeric_cols:
    if col in filtered_df_corr.columns:
        corr = filtered_df_corr[col].corr(filtered_df_corr['Attrition_Binary'])
        correlations.append({'Factor': col.replace('_', ' '), 'Correlation_with_Attrition': corr})

if correlations:
    corr_df = pd.DataFrame(correlations).sort_values('Correlation_with_Attrition', key=abs, ascending=False)
    
    fig9 = px.bar(
        corr_df,
        x='Correlation_with_Attrition',
        y='Factor',
        orientation='h',
        title='Correlation of Factors with Attrition',
        color='Correlation_with_Attrition',
        color_continuous_scale='RdBu_r',
        text='Correlation_with_Attrition'
    )
    fig9.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig9.update_layout(height=500)
    st.plotly_chart(fig9, use_container_width=True)

# Summary Insights
st.subheader("💡 Key Insights & Recommendations")

# Calculate key insights
high_risk_dept = dept_attrition['Attrition_Rate'].idxmax() if len(dept_attrition) > 0 else "N/A"
high_risk_age = age_attrition['Attrition_Rate'].idxmax() if len(age_attrition) > 0 else "N/A"
avg_income_staying = filtered_df[filtered_df['Attrition'] == 'No']['Monthly_Income'].mean()
avg_income_leaving = filtered_df[filtered_df['Attrition'] == 'Yes']['Monthly_Income'].mean()

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    **🔍 Key Risk Factors:**
    - Highest risk department: **{high_risk_dept}** ({dept_attrition.loc[high_risk_dept, 'Attrition_Rate']:.1f}% attrition)
    - Highest risk age group: **{high_risk_age}** ({age_attrition.loc[high_risk_age, 'Attrition_Rate']:.1f}% attrition)
    - Income gap: Leaving employees earn **${avg_income_leaving-avg_income_staying:,.0f}** {'more' if avg_income_leaving > avg_income_staying else 'less'} on average
    """)

with col2:
    st.success(f"""
    **💡 Recommendations:**
    - Focus retention efforts on **{high_risk_dept}** department
    - Develop targeted programs for **{high_risk_age}** age group
    - Review compensation strategy - {'consider salary adjustments' if avg_income_leaving < avg_income_staying else 'investigate non-monetary factors'}
    - Enhance work-life balance initiatives
    """)

# Data Export Section
st.subheader("📥 Data Export")
col1, col2, col3 = st.columns(3)

with col1:
    # Export filtered data
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="📊 Download Filtered Data (CSV)",
        data=csv_data,
        file_name=f"hr_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    # Export summary statistics
    summary_stats = filtered_df.describe()
    summary_csv = summary_stats.to_csv()
    st.download_button(
        label="📈 Download Summary Stats (CSV)",
        data=summary_csv,
        file_name=f"hr_summary_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col3:
    # Export attrition analysis
    if len(dept_attrition) > 0:
        analysis_csv = dept_attrition.to_csv()
        st.download_button(
            label="🔍 Download Attrition Analysis (CSV)",
            data=analysis_csv,
            file_name=f"hr_attrition_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 HR Attrition Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p>💡 Use the filters on the left to explore different employee segments and identify key attrition patterns</p>
</div>
""", unsafe_allow_html=True)