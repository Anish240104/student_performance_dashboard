import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("🎓 Student Performance Analytics Dashboard")

uploaded_file = st.file_uploader("📂 Upload your student data CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df['Average Marks'] = df[['Maths', 'Science', 'English']].mean(axis=1)

    def attendance_level(x):
        if x >= 85:
            return 'High'
        elif x >= 60:
            return 'Moderate'
        else:
            return 'Low'
    df['Attendance Level'] = df['Attendance (%)'].apply(attendance_level)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Average Marks per Student")
        st.bar_chart(df[['Name', 'Average Marks']].set_index('Name'))

    with col2:
        st.subheader("🔥 Correlation Heatmap")
        fig1, ax1 = plt.subplots()
        sns.heatmap(df[['Maths', 'Science', 'English', 'Attendance (%)', 'Login Count', 'Average Marks']].corr(), annot=True, cmap='coolwarm', ax=ax1)
        st.pyplot(fig1)

    st.subheader("📌 Attendance Level Distribution")
    att_count = df['Attendance Level'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(att_count, labels=att_count.index, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'], startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)

    st.subheader("📥 Login Frequency Distribution")
    fig3, ax3 = plt.subplots()
    sns.histplot(df['Login Count'], bins=8, kde=True, color='skyblue', ax=ax3)
    ax3.set_xlabel("Login Count")
    ax3.set_ylabel("Number of Students")
    st.pyplot(fig3)

    st.subheader("🏆 Top vs Struggling Students")
    pass_mark = 60
    top_students = df.sort_values(by='Average Marks', ascending=False).head(3)
    struggling_students = df[df['Average Marks'] < pass_mark].sort_values(by='Average Marks')

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**💪 Top Performers:**")
        st.dataframe(top_students[['Name', 'Average Marks']])
    with col4:
        st.markdown("**⚠️ Students Needing Support:**")
        st.dataframe(struggling_students[['Name', 'Average Marks']])
else:
    st.info("Please upload a CSV file to start.")
