# 🏢 HR Attrition Analytics Dashboard

A comprehensive, interactive HR analytics dashboard built with Streamlit and Plotly that provides deep insights into employee attrition patterns, helping HR teams make data-driven retention decisions.

![Dashboard Preview](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 📊 Features

### Key Performance Indicators (KPIs)
- **Total Employees** - Complete workforce overview
- **Current Employees** - Active employee count
- **Attrition Count** - Number of employees who left
- **Attrition Rate** - Percentage-based attrition metrics
- **Average Tenure** - Employee retention duration analysis

### Interactive Visualizations
1. **Departmental Analysis** - Attrition rates across different departments
2. **Demographic Analysis** - Age-based attrition patterns
3. **Satisfaction Analysis** - Multi-dimensional satisfaction vs attrition correlation
4. **Compensation Analysis** - Income distribution impact on retention
5. **Tenure Analysis** - Years at company vs attrition trends
6. **Work-Life Balance** - Overtime and travel impact on attrition
7. **Performance Analysis** - Performance rating correlation with attrition
8. **Training Analysis** - Training frequency vs retention rates
9. **Correlation Matrix** - Advanced factor correlation analysis

### Advanced Features
- **Dynamic Filtering** - Multi-level filtering system
- **Real-time Updates** - Instant chart updates based on filters
- **Export Capabilities** - CSV downloads for further analysis
- **Automated Insights** - AI-generated recommendations
- **Responsive Design** - Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files:**
   ```bash
   # Create project directory
   mkdir hr-dashboard
   cd hr-dashboard
   ```

2. **Install required packages:**
   ```bash
   pip install streamlit pandas plotly numpy
   ```

3. **Create the data generation script** (`generate_hr_data.py`):
   ```python
   # This file should generate the hr_employee_data.csv file
   # Contact your data team or create sample data with required columns
   ```

4. **Generate sample data:**
   ```bash
   python generate_hr_data.py
   ```

5. **Run the dashboard:**
   ```bash
   streamlit run hr_dashboard.py
   ```

6. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
hr-dashboard/
├── hr_dashboard.py          # Main dashboard application
├── generate_hr_data.py      # Data generation script
├── hr_employee_data.csv     # Employee data (generated)
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## 📋 Required Data Columns

The dashboard expects a CSV file with the following columns:

| Column Name | Type | Description |
|-------------|------|-------------|
| `Employee_ID` | Integer | Unique employee identifier |
| `Department` | String | Employee department |
| `CF_age_band` | String | Age bands (Under 25, 25-34, etc.) |
| `Monthly_Income` | Float | Employee monthly salary |
| `Job_Level` | Integer | Job level (1-4, where 1=Entry, 4=Senior) |
| `Attrition` | String | 'Yes' or 'No' |
| `Years_At_Company` | Float | Tenure in years |
| `Job_Satisfaction` | Integer | Rating 1-4 |
| `Environment_Satisfaction` | Integer | Rating 1-4 |
| `Relationship_Satisfaction` | Integer | Rating 1-4 |
| `Work_Life_Balance` | Integer | Rating 1-4 |
| `Performance_Rating` | Integer | Rating 1-4 |
| `Business_Travel` | String | Travel frequency |
| `Over_Time` | String | 'Yes' or 'No' |
| `Training_Times_Last_Year` | Integer | Number of training sessions |

## 🎛️ Dashboard Controls

### Sidebar Filters
- **Department Filter** - Select specific departments
- **Age Band Filter** - Filter by age groups
- **Income Range** - Salary range slider
- **Job Level** - Filter by career levels
- **Advanced Filters** - Performance rating and travel filters

### Main Dashboard Sections
1. **KPI Row** - Key metrics at a glance
2. **Departmental Analysis** - Department and age-based insights
3. **Satisfaction Analysis** - Employee satisfaction correlations
4. **Tenure Analysis** - Work-life balance impact
5. **Performance Analysis** - Performance and training insights
6. **Correlation Analysis** - Advanced statistical analysis
7. **Insights & Recommendations** - Automated findings
8. **Data Export** - Download capabilities

## 💡 How to Use

### Basic Analysis
1. **Launch the dashboard** and review the KPI metrics
2. **Use department filters** to focus on specific teams
3. **Analyze the charts** to identify attrition patterns
4. **Review automated insights** for key findings

### Advanced Analysis
1. **Combine multiple filters** for detailed segmentation
2. **Study correlation analysis** to understand factor relationships
3. **Export filtered data** for external analysis
4. **Use insights section** for actionable recommendations

### Export Options
- **Filtered Data** - Download current view as CSV
- **Summary Stats** - Statistical summary of filtered data
- **Attrition Analysis** - Department-level attrition metrics

## 🔧 Customization

### Adding New Visualizations
```python
# Add to the main dashboard code
fig_new = px.your_chart_type(
    filtered_df,
    x='your_x_column',
    y='your_y_column',
    title='Your Chart Title'
)
st.plotly_chart(fig_new, use_container_width=True)
```

### Custom Filters
```python
# Add to sidebar section
custom_filter = st.sidebar.multiselect(
    "Your Filter Name",
    options=df['Your_Column'].unique(),
    default=df['Your_Column'].unique()
)
```

### Theme Customization
The dashboard uses Streamlit's default theme. For custom styling, add CSS:
```python
st.markdown("""
<style>
/* Your custom CSS here */
</style>
""", unsafe_allow_html=True)
```

## 📊 Sample Insights Generated

The dashboard automatically generates insights such as:
- **High-risk departments** with elevated attrition rates
- **Vulnerable age groups** requiring targeted retention
- **Compensation gaps** between staying and leaving employees
- **Work-life balance** impact on retention rates
- **Training effectiveness** on employee retention

## 🚨 Troubleshooting

### Common Issues

**"Data file not found" error:**
```bash
# Make sure to run the data generation script first
python generate_hr_data.py
```

**Module import errors:**
```bash
# Install missing packages
pip install streamlit pandas plotly numpy
```

**Empty charts or filters:**
- Check that your CSV has the required columns
- Verify data types match the expected format
- Ensure there are no empty values in key columns

**Performance issues:**
- Large datasets (>100k rows) may load slowly
- Consider data sampling for very large files
- Use the filtering options to reduce data size

### Performance Optimization
- **Data Caching**: The `@st.cache_data` decorator optimizes data loading
- **Filtering**: Use sidebar filters to reduce computational load
- **Chart Optimization**: Charts automatically adjust based on data size

## 🛠️ Dependencies

Create a `requirements.txt` file:
```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
numpy>=1.24.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 📈 Advanced Features

### Correlation Analysis
- Automatically calculates correlations between all numeric factors and attrition
- Visualizes factor importance in an intuitive bar chart
- Helps identify the most impactful retention factors

### Automated Insights
- Real-time calculation of key risk factors
- Automatic identification of high-risk departments and age groups
- Income gap analysis between staying and leaving employees
- Data-driven recommendations for HR action

### Export Capabilities
- **CSV Export**: Download filtered datasets
- **Summary Statistics**: Export statistical summaries
- **Analysis Results**: Download department-level analysis

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 📧 Support

For support or questions:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Create an issue for bugs or feature requests

## 🔄 Version History

- **v1.0** - Initial release with basic dashboard functionality
- **v1.1** - Added advanced filters and correlation analysis
- **v1.2** - Enhanced export capabilities and automated insights
- **v1.3** - Performance improvements and better error handling

---

**Built with ❤️ using Streamlit, Plotly, and Python**

*Transform your HR data into actionable insights with this comprehensive analytics dashboard.*
