import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("📊 Student Performance Analyzer")
st.write(
    "An interactive application to analyze student academic "
    "performance using marks and attendance data."
)

st.divider()

# ---------------- FILE UPLOAD ----------------

st.subheader("📂 Upload Student Data")

uploaded_file = st.file_uploader(
    "Upload a CSV file containing student data",
    type=["csv"]
)

# ---------------- SAMPLE DATA ----------------

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

else:

    st.info(
        "No file uploaded. Sample data is being used for demonstration."
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
        "Math": [85, 72, 94, 81, 65, 88],
        "Python": [92, 68, 89, 85, 72, 91],
        "DBMS": [78, 75, 96, 88, 70, 84],
        "Attendance": [91, 82, 97, 89, 76, 93]
    }

    df = pd.DataFrame(data)


# ---------------- CHECK DATA ----------------

required_columns = [
    "Name",
    "Math",
    "Python",
    "DBMS",
    "Attendance"
]

if all(column in df.columns for column in required_columns):

    # ---------------- CALCULATIONS ----------------

    df["Total"] = (
        df["Math"]
        + df["Python"]
        + df["DBMS"]
    )

    df["Average"] = df["Total"] / 3


    # ---------------- GRADE FUNCTION ----------------

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


    df["Grade"] = df["Average"].apply(calculate_grade)


    # ---------------- PASS / FAIL ----------------

    df["Result"] = df["Average"].apply(
        lambda x: "PASS" if x >= 40 else "FAIL"
    )


    # ---------------- TOP PERFORMER ----------------

    topper = df.loc[df["Average"].idxmax()]


    # ---------------- SUBJECT ANALYSIS ----------------

    subjects = [
        "Math",
        "Python",
        "DBMS"
    ]

    subject_averages = df[subjects].mean()


    # ---------------- DASHBOARD ----------------

    st.subheader("📈 Performance Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Students",
            len(df)
        )

    with col2:

        st.metric(
            "Class Average",
            f"{df['Average'].mean():.2f}%"
        )

    with col3:

        st.metric(
            "Top Performer",
            topper["Name"]
        )

    with col4:

        st.metric(
            "Highest Average",
            f"{df['Average'].max():.2f}%"
        )


    st.divider()


    # ---------------- STUDENT TABLE ----------------

    st.subheader("👩‍🎓 Student Performance")

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


    st.divider()


    # ---------------- CHARTS ----------------

    col1, col2 = st.columns(2)


    # Student Performance Chart

    with col1:

        st.subheader("📊 Student Performance")

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.bar(
            df["Name"],
            df["Average"]
        )

        ax.set_title(
            "Student Performance Comparison"
        )

        ax.set_xlabel("Students")
        ax.set_ylabel("Average Marks")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)


    # Subject Performance Chart

    with col2:

        st.subheader("📚 Subject Performance")

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.bar(
            subject_averages.index,
            subject_averages.values
        )

        ax.set_title(
            "Subject-wise Average Performance"
        )

        ax.set_xlabel("Subjects")
        ax.set_ylabel("Average Marks")

        plt.tight_layout()

        st.pyplot(fig)


    # ---------------- ATTENDANCE ANALYSIS ----------------

    st.subheader(
        "📈 Attendance vs Academic Performance"
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        df["Attendance"],
        df["Average"],
        s=100
    )

    ax.set_title(
        "Attendance vs Academic Performance"
    )

    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average Marks")

    ax.grid(True)

    st.pyplot(fig)


    st.divider()


    # ---------------- KEY INSIGHTS ----------------

    st.subheader("💡 Key Insights")

    best_subject = subject_averages.idxmax()

    weakest_subject = subject_averages.idxmin()

    st.write(
        f"🏆 **Top Performer:** {topper['Name']} "
        f"with an average of "
        f"{topper['Average']:.2f}%."
    )

    st.write(
        f"📚 **Best Performing Subject:** "
        f"{best_subject} "
        f"({subject_averages.max():.2f}%)."
    )

    st.write(
        f"📖 **Subject Needing Improvement:** "
        f"{weakest_subject} "
        f"({subject_averages.min():.2f}%)."
    )


    # ---------------- DOWNLOAD RESULTS ----------------

    st.divider()

    st.subheader("💾 Download Analysis")

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Analyzed Results",
        data=csv,
        file_name="analyzed_students.csv",
        mime="text/csv"
    )


else:

    st.error(
        "❌ Invalid CSV format."
    )

    st.write(
        "Your CSV must contain these columns:"
    )

    st.code(
        "Name, Math, Python, DBMS, Attendance"
    )
