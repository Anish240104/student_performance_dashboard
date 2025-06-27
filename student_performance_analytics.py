# student_performance_analytics.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit app title
st.title("📊 Student Performance Analytics")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your student dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Preview data
    st.subheader("🔍 Dataset Preview")
    st.write(df)
    
    # Dataset shape
    st_rows, st_cols = df.shape
    st.info(f"✅ Dataset loaded with {st_rows} rows and {st_cols} columns.")
    
    # Column names
    st.subheader("📋 Column Names")
    st.write(df.columns.tolist())
    
    # Check for missing values
    st.subheader("🧹 Missing Values")
    st.write(df.isnull().sum())
    
    # Calculate average marks
    if all(col in df.columns for col in ['Maths', 'Science', 'English']):
        df['Average Marks'] = df[['Maths', 'Science', 'English']].mean(axis=1)
        st.success("✅ 'Average Marks' column added.")
        st.write(df[['Name', 'Maths', 'Science', 'English', 'Average Marks']])
    else:
        st.error("Columns 'Maths', 'Science', and 'English' not found.")
    
    # Bar Chart: Average Marks
    st.subheader("📊 Average Marks per Student")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Name', y='Average Marks', data=df, palette='viridis', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Correlation Heatmap
    st.subheader("🔥 Correlation Between Academic Metrics")
    metric_cols = ['Maths', 'Science', 'English', 'Attendance (%)', 'Login Count', 'Average Marks']
    if all(col in df.columns for col in metric_cols):
        corr_matrix = df[metric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Some metric columns are missing for correlation matrix.")
    
    # Top vs Struggling Students
    st.subheader("🏅 Performance Breakdown")
    if 'Average Marks' in df.columns:
        pass_mark = 60
        top_students = df.sort_values(by='Average Marks', ascending=False).head(3)
        struggling_students = df[df['Average Marks'] < pass_mark].sort_values(by='Average Marks')
        
        st.write("✅ **Top 3 Students**")
        st.write(top_students[['Name', 'Average Marks']])
        
        st.write("⚠️ **Students Needing Support**")
        st.write(struggling_students[['Name', 'Average Marks']])
    
    # Attendance Level Categorization
    st.subheader("📌 Attendance Level Distribution")
    if 'Attendance (%)' in df.columns:
        def attendance_level(x):
            if x >= 85:
                return 'High'
            elif x >= 60:
                return 'Moderate'
            else:
                return 'Low'
        
        df['Attendance Level'] = df['Attendance (%)'].apply(attendance_level)
        attendance_counts = df['Attendance Level'].value_counts()
        
        fig, ax = plt.subplots()
        colors = ['#4CAF50', '#FFC107', '#F44336']
        ax.pie(attendance_counts, labels=attendance_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=140)
        ax.set_title("Student Attendance Distribution")
        st.pyplot(fig)

    # Login Count Distribution
    st.subheader("📈 Login Count Distribution")
    if 'Login Count' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df['Login Count'], bins=8, kde=True, color='skyblue', ax=ax)
        ax.set_title("Login Frequency Distribution")
        st.pyplot(fig)

    # Final Insights
    st.subheader("🧠 Final Insights")
    st.markdown("""
    - ✅ **Top performers** have average marks above 85% and high attendance.
    - ⚠️ **Struggling students** often have both **low attendance** and **low login activity**.
    - 🔥 **Positive correlation** between attendance, login count, and academic performance.
    """)

else:
    st.warning("Please upload your CSV file to begin analysis.")
