import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("📊 Student Performance Analyzer")

st.markdown(
    """
    **An interactive academic analytics dashboard** that evaluates
    student marks, grades, attendance and performance trends.
    """
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Controls")

st.sidebar.write(
    "Upload a CSV file to analyze your own student data."
)

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Student CSV",
    type=["csv"]
)

# =========================================================
# SAMPLE DATA
# =========================================================

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

else:

    st.info(
        "📌 No CSV uploaded — showing sample data."
    )

    data = {
        "Name": [
            "Akshra",
            "Rahul",
            "Priya",
            "Ananya",
            "Arjun",
            "Simran"
        ],

        "Math": [
            85,
            72,
            94,
            81,
            65,
            88
        ],

        "Python": [
            92,
            68,
            89,
            85,
            72,
            91
        ],

        "DBMS": [
            78,
            75,
            96,
            88,
            70,
            84
        ],

        "Attendance": [
            91,
            82,
            97,
            89,
            76,
            93
        ]
    }

    df = pd.DataFrame(data)

# =========================================================
# VALIDATE DATA
# =========================================================

required_columns = [
    "Name",
    "Math",
    "Python",
    "DBMS",
    "Attendance"
]

if not all(column in df.columns for column in required_columns):

    st.error(
        "❌ Invalid CSV format."
    )

    st.write(
        "Your CSV must contain:"
    )

    st.code(
        "Name, Math, Python, DBMS, Attendance"
    )

    st.stop()

# =========================================================
# CALCULATIONS
# =========================================================

subjects = [
    "Math",
    "Python",
    "DBMS"
]

df["Total"] = (
    df["Math"]
    + df["Python"]
    + df["DBMS"]
)

df["Average"] = (
    df["Total"] / len(subjects)
)

# =========================================================
# GRADE FUNCTION
# =========================================================

def calculate_grade(average):

    if average >= 90:
        return "A+"

    elif average >= 80:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    elif average >= 50:
        return "D"

    else:
        return "F"


df["Grade"] = df["Average"].apply(
    calculate_grade
)

# =========================================================
# RESULT
# =========================================================

df["Result"] = df["Average"].apply(
    lambda x: "PASS"
    if x >= 40
    else "FAIL"
)

# =========================================================
# KEY METRICS
# =========================================================

topper = df.loc[
    df["Average"].idxmax()
]

lowest_student = df.loc[
    df["Average"].idxmin()
]

class_average = df["Average"].mean()

highest_average = df["Average"].max()

lowest_average = df["Average"].min()

best_subject = df[subjects].mean().idxmax()

weakest_subject = df[subjects].mean().idxmin()

# =========================================================
# DASHBOARD
# =========================================================

st.header("📈 Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👩‍🎓 Total Students",
        len(df)
    )

with col2:

    st.metric(
        "📊 Class Average",
        f"{class_average:.2f}%"
    )

with col3:

    st.metric(
        "🏆 Top Performer",
        topper["Name"]
    )

with col4:

    st.metric(
        "⭐ Highest Average",
        f"{highest_average:.2f}%"
    )

st.divider()

# =========================================================
# STUDENT SELECTOR
# =========================================================

st.header("👤 Individual Student Analysis")

selected_student = st.selectbox(
    "Select a student",
    df["Name"].tolist()
)

student = df[
    df["Name"] == selected_student
].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Average",
        f"{student['Average']:.2f}%"
    )

with col2:

    st.metric(
        "Grade",
        student["Grade"]
    )

with col3:

    st.metric(
        "Attendance",
        f"{student['Attendance']}%"
    )

with col4:

    st.metric(
        "Result",
        student["Result"]
    )

# =========================================================
# STUDENT SUBJECT PERFORMANCE
# =========================================================

st.subheader(
    f"📚 {selected_student}'s Subject Performance"
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    subjects,
    [student[s] for s in subjects]
)

ax.set_ylim(0, 100)

ax.set_ylabel("Marks")

ax.set_title(
    f"{selected_student} - Subject Performance"
)

plt.tight_layout()

st.pyplot(fig)

# =========================================================
# STUDENT TABLE
# =========================================================

st.header("📋 Complete Student Data")

display_columns = [
    "Name",
    "Math",
    "Python",
    "DBMS",
    "Attendance",
    "Total",
    "Average",
    "Grade",
    "Result"
]

st.dataframe(
    df[display_columns],
    use_container_width=True
)

# =========================================================
# VISUAL ANALYSIS
# =========================================================

st.header("📊 Visual Analysis")

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# Student Performance
# ---------------------------------------------------------

with col1:

    st.subheader(
        "Student Performance Comparison"
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        df["Name"],
        df["Average"]
    )

    ax.set_ylim(0, 100)

    ax.set_ylabel(
        "Average Marks"
    )

    ax.set_xlabel(
        "Students"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)

# ---------------------------------------------------------
# Subject Performance
# ---------------------------------------------------------

with col2:

    st.subheader(
        "Subject-wise Performance"
    )

    subject_averages = df[
        subjects
    ].mean()

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        subject_averages.index,
        subject_averages.values
    )

    ax.set_ylim(0, 100)

    ax.set_ylabel(
        "Average Marks"
    )

    ax.set_xlabel(
        "Subjects"
    )

    plt.tight_layout()

    st.pyplot(fig)

# =========================================================
# GRADE DISTRIBUTION
# =========================================================

st.header("🏅 Grade Distribution")

grade_counts = df[
    "Grade"
].value_counts()

fig, ax = plt.subplots(
    figsize=(8, 4)
)

ax.bar(
    grade_counts.index,
    grade_counts.values
)

ax.set_xlabel(
    "Grades"
)

ax.set_ylabel(
    "Number of Students"
)

ax.set_title(
    "Distribution of Student Grades"
)

plt.tight_layout()

st.pyplot(fig)

# =========================================================
# ATTENDANCE ANALYSIS
# =========================================================

st.header(
    "📈 Attendance vs Academic Performance"
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

ax.scatter(
    df["Attendance"],
    df["Average"],
    s=100
)

ax.set_xlabel(
    "Attendance (%)"
)

ax.set_ylabel(
    "Average Marks"
)

ax.set_title(
    "Attendance vs Academic Performance"
)

ax.grid(True)

plt.tight_layout()

st.pyplot(fig)

# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

st.header("💡 Key Insights")

st.success(
    f"🏆 **Top Performer:** {topper['Name']} "
    f"with an average of "
    f"{topper['Average']:.2f}%."
)

st.info(
    f"📚 **Best Performing Subject:** "
    f"{best_subject}."
)

st.warning(
    f"📖 **Subject Needing Improvement:** "
    f"{weakest_subject}."
)

st.write(
    f"📉 **Lowest Performing Student:** "
    f"{lowest_student['Name']} "
    f"({lowest_student['Average']:.2f}%)."
)

# =========================================================
# ATTENDANCE INSIGHT
# =========================================================

attendance_correlation = df[
    "Attendance"
].corr(
    df["Average"]
)

st.write(
    f"📈 **Attendance-Performance Correlation:** "
    f"{attendance_correlation:.2f}"
)

if attendance_correlation > 0.5:

    st.write(
        "The dataset shows a positive relationship "
        "between attendance and academic performance."
    )

elif attendance_correlation < -0.5:

    st.write(
        "The dataset shows a negative relationship "
        "between attendance and academic performance."
    )

else:

    st.write(
        "The dataset shows a weak relationship "
        "between attendance and academic performance."
    )

# =========================================================
# DOWNLOAD RESULTS
# =========================================================

st.divider()

st.header("💾 Download Results")

csv = df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Analyzed CSV",
    data=csv,
    file_name="student_performance_analysis.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Student Performance Analyzer | "
    "Python • Pandas • Matplotlib • Streamlit"
)
