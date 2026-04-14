import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# =============================
# 🔥 PAGE CONFIG
# =============================
st.set_page_config(page_title="AI Maintenance", layout="wide")

# =============================
# 🔥 CUSTOM CSS (PREMIUM UI)
# =============================
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }
    </style>
""", unsafe_allow_html=True)

# =============================
# 🔥 TITLE
# =============================
st.title("🚀 AI Predictive Maintenance Dashboard")

# =============================
# 🔥 LOAD MODEL
# =============================
model = joblib.load("models/model.pkl")

# =============================
# 🔥 TABS (VERY IMPORTANT)
# =============================

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Analytics", "📂 Upload"])
# =====================================================
# 🚀 TAB 1: DASHBOARD
# =====================================================
with tab1:
    st.header("📊 Real-Time Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        temp = st.slider("Temperature", 0, 100, 50)

    with col2:
        vib = st.slider("Vibration", 0.0, 5.0, 1.0)

    with col3:
        curr = st.slider("Current", 0, 20, 5)

    # Prediction
    features = np.array([[temp, vib, curr]])
    prediction = model.predict(features)

    st.subheader("🔍 Result")

    if prediction[0] == 1:
        st.error("⚠️ Machine Failure Predicted!")
    else:
        st.success("✅ Machine Running Normally")
# Bar Graph
st.subheader("📊 Sensor Values")

# Center the graph using columns
col1, col2, col3 = st.columns([1,2,1])

with col2:
    fig, ax = plt.subplots(figsize=(3.5,2.2))  # smaller size

    # ax.bar(["Temp", "Vibration", "Current"], [temp, vib, curr])
    ax.bar(["Temp", "Vibration", "Current"], [temp, vib, curr],
       color=["#00c6ff", "#f7971e", "#ff4b5c"])

    # Styling (clean look)
    ax.set_title("Sensor Values", fontsize=9)
    ax.tick_params(labelsize=7)
    ax.spines[['top','right']].set_visible(False)

    st.pyplot(fig, use_container_width=False)
# =====================================================
# 🚀 TAB 2: ANALYTICS
# =====================================================
with tab2:
    st.header("📈 Data Analytics")

    df = pd.read_csv("data/sensor_data.csv")

    st.write(df.head())

    # =========================================
    # 🔹 ROW 1 → Heatmap + Feature Importance
    # =========================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(5,3))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("🔥 Feature Importance")
        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(['temperature','vibration','current'], model.feature_importances_)
        st.pyplot(fig)

    # =========================================
    # 🔹 ROW 2 → Line Chart
    # =========================================
    st.subheader("📈 Sensor Trends")
    st.line_chart(df[['temperature','vibration','current']], height=250)

    # =========================================
    # 🔹 ROW 3 → Pie Chart + Histogram
    # =========================================
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🥧 Failure Distribution")
        fig, ax = plt.subplots(figsize=(4,4))
        counts = df['failure'].value_counts()
        ax.pie(counts, labels=["Normal","Failure"], autopct='%1.1f%%')
        st.pyplot(fig)

    with col4:
        st.subheader("📊 Sensor Distribution")
        fig, ax = plt.subplots(figsize=(5,5))
        df[['temperature','vibration','current']].hist(ax=ax)
        st.pyplot(fig)
   

 
# =====================================================
# 🚀 TAB 3: CSV UPLOAD + PREDICTION
# =====================================================


with tab3:
    st.header("📂 Upload CSV & Predict")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file is not None:
        df = pd.read_csv(io.StringIO(file.getvalue().decode("utf-8")))

        st.subheader("📊 Uploaded Data")
        st.write(df.head())

        # Prediction
        predictions = model.predict(df[['temperature','vibration','current']])
        df['Prediction'] = predictions

        st.subheader("🔍 Results")
        st.write(df)

        # Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Predictions",
            data=csv,
            file_name='predictions.csv',
            mime='text/csv'
        )

        # =========================
        # 📊 GRAPH (ONLY HEATMAP)
        # =========================
        st.subheader("📊 Uploaded Data Visualization")

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            fig, ax = plt.subplots(figsize=(4,2.5))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)

            ax.set_title("Correlation Heatmap", fontsize=9)
            ax.tick_params(labelsize=7)
            ax.spines[['top','right']].set_visible(False)

            st.pyplot(fig, use_container_width=False)
# with tab3:
#     st.header("📂 Upload CSV & Predict")

#     file = st.file_uploader("Upload CSV", type=["csv"])

#     if file is not None:
#         df = pd.read_csv(io.StringIO(file.getvalue().decode("utf-8")))

#         st.subheader("📊 Uploaded Data")
#         st.write(df.head())

#         # Prediction
#         predictions = model.predict(df[['temperature','vibration','current']])
#         df['Prediction'] = predictions

#         st.subheader("🔍 Results")
#         st.write(df)

#         # Download Button 🔥
#         csv = df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="📥 Download Predictions",
#             data=csv,
#             file_name='predictions.csv',
#             mime='text/csv'
#         )
# # # Graphs
# # st.subheader("📊 Uploaded Data Visualization")

# # # Center layout
# # col1, col2, col3 = st.columns([1,2,1])

# # with col2:
#     # Graphs
#     st.subheader("📊 Uploaded Data Visualization")

# # Center layout
# col1, col2, col3 = st.columns([1,2,1])

# with col2:
#     # 🔥 Heatmap only
#     fig, ax = plt.subplots(figsize=(4,2.5))
#     sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)

#     ax.set_title("Correlation Heatmap", fontsize=9)
#     ax.tick_params(labelsize=7)
#     ax.spines[['top','right']].set_visible(False)

#     st.pyplot(fig, use_container_width=False)
# # =============================
# # 🎉 FINAL TOUCH
# # =============================
