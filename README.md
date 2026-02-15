# 🛡️ AzRBAC-Insight

AzRBAC-Insight is a Streamlit-based dashboard designed for deep-dive analysis and visualization of Azure Role-Based Access Control (RBAC) assignments. It empowers cloud administrators and security teams to audit permissions, identify over-privileged identities, and maintain a secure cloud posture.

---

## 1. Project Overview & Architecture

### About the Project
AzRBAC-Insight provides a clean, interactive interface to explore complex Azure RBAC data that is otherwise difficult to parse in raw CSV format. It helps answer critical questions like:
- Who has high-privilege roles across the subscription?
- What resources have the most direct role assignments?
- What is the distribution of roles between Users, Groups, and Service Principals?

### Project Structure
```text
AzRBAC-Insight/
├── app.py              # Main Streamlit application and visualization logic
├── requirements.txt    # Python dependencies (Pandas, Plotly, Streamlit, etc.)
├── Dockerfile          # Multi-stage Docker build for containerization
├── .gitignore          # Repository hygiene (ignores .venv, data/, etc.)
├── data/               # Local directory for temporary storage of CSV reports
├── k8s/                # Kubernetes manifests for AKS deployment
│   └── manifests.yaml  # Deployment and Service definitions
├── .gitignore          # Repository hygiene (ignores .venv, data/, etc.)
├── data/               # Local directory for temporary storage of CSV reports
├── k8s/                # Kubernetes manifests for deployment
│   └── manifests.yaml  # Deployment and Service definitions
└── .github/            # GitHub Actions for CI/CD
```

### High-Level Architecture
The application follows a simple but effective data-processing pattern:
1.  **Data Ingestion**: Accepts Azure Role Assignment CSV reports (either via upload or environment variable).
2.  **Processing Layer**: Uses Pandas to clean column names, extract resource names from long Azure scopes, and filter data dynamically.
3.  **Visualization Layer**: Leverages Plotly and Streamlit to generate interactive charts and tables.
4.  **Deployment**: Designed to run as a stateless container in Kubernetes or as a standalone Python process.

---

## 2. How to Test Locally

To run and test the dashboard on your local machine, follow these steps:

### Prerequisites
- Python 3.12 or higher.
- A virtual environment is highly recommended.

### Step-by-Step Setup
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/chinmaymjog/AzRBAC-Insight.git
    cd AzRBAC-Insight
    ```

2.  **Initialize Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

5.  **Access the Dashboard**:
    Open your browser and navigate to `http://localhost:8501`.

---

## 3. End-User Guide (How to Use)

Using AzRBAC-Insight is straightforward and requires no coding knowledge.

### Getting Started
1.  **Export Data from Azure**:
    - Go to the Azure Portal.
    - Navigate to **Subscriptions** or **Management Groups**.
    - Click on **Access Control (IAM)** -> **Role Assignments**.
    - Click **Download Role Assignments** and check **Children** and **CSV** format.

2.  **Upload to Dashboard**:
    - Once the dashboard is running, use the **Sidebar** to find the file uploader.
    - Drag and drop your exported CSV file.
    - The dashboard will automatically update with your data.

---

## Technologies Used

- **Frontend/Dashboard**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **Charts**: [Plotly Express](https://plotly.com/python/plotly-express/)
- **Infrastructure**: Docker, Kubernetes, GitHub Actions