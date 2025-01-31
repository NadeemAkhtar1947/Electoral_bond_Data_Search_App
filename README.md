# 📊 Electoral Bond Analysis App

## 📝 Overview
This **Streamlit** application provides an interactive analysis of **Electoral Bond Data** by visualizing donation distributions from companies to political parties. It offers insights into donation trends, company-wise and party-wise funding, and year-wise analysis using various **data visualization tools**.

## 🌟 Features
- **👥 Party-wise Analysis:**
  - Top political parties by donations.
  - Donation distribution across different parties.
  - Year-wise donations received by each party.
  - Overall summary of party-wise contributions.
- **🏢 Company-wise Analysis:**
  - Top companies by donation amounts.
  - Donation distribution across different companies.
  - Year-wise contributions by companies.
  - Overall summary of company-wise donations.
- **📊 Data Visualization:**
  - **Pie Charts**, **Bar Graphs**, **Line Charts** for deep insights.
  - Interactive filters to customize views.
  - Dynamic tables showing donations at different levels.

## 📂 Dataset
- **📌 Source:** Merged dataset containing **electoral bond transactions**.
- **📑 Columns:**
  - `Bond Number`: Unique bond ID.
  - `Redeemed Date`: Date when the bond was redeemed.
  - `Political Party`: The recipient political party.
  - `Account No.`: Account details of the party.
  - `Denomination (Crore)`: Value of the bond (converted to crore for easy readability).
  - `Purchase Date`: Date when the bond was purchased.
  - `Company`: The entity that purchased the bond.
  - `Status`: Current status of the bond.

## 📊 Data Processing & Cleaning
- Converted date fields (`Purchase Date`, `Redeemed Date`) to **datetime format**.
- Extracted **year-wise** data for in-depth analysis.
- Removed duplicate values and handled missing entries.
- Renamed columns for consistency.

## 🛠️ Installation & Usage
### **📌 Requirements**
Ensure you have the following Python libraries installed:
```bash
pip install streamlit pandas plotly seaborn matplotlib
```

### **▶️ Running the App**
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd electoral-bond-analysis
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 📷 Output Example
![App Screenshot](output_image.png)

## 🔮 Future Enhancements
- Implement **machine learning models** for predictive analysis.
- Add **real-time data updates** using APIs.
- Deploy as a **web-based dashboard** for broader accessibility.

## 📬 Contact & Support
Connect with me for feedback or contributions:
- **🔗 [LinkedIn](https://www.linkedin.com/in/nadeem-akhtar-/)**
- **🐙 [GitHub](https://github.com/NadeemAkhtar1947)**
- **📊 [Kaggle](https://www.kaggle.com/mdnadeemakhtar/code)**
- **🌎 [Portfolio](https://nsde.netlify.app/)**

🚀 **Developed by Nadeem Akhtar** | 📅 **Copyright © 2024**

