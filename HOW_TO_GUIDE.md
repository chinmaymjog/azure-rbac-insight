# 📖 User Guide: Analyzing Azure RBAC Assignments

This guide provides step-by-step instructions on how to use the **Azure RBAC Insight** dashboard to audit your subscription permissions.

---

## Step 1: Exporting Data from Azure

The dashboard requires a CSV export from the Azure Portal.

1.  Log in to the **Azure Portal**.
2.  Navigate to the level you want to audit: **Subscription**, **Management Group**, or a specific **Resource Group**.
3.  Click on **Access Control (IAM)** in the left-hand menu.
4.  Navigate to the **Role Assignments** tab.
5.  Click the **Download Role Assignments** button (at the top).
6.  **Crucial Settings**:
    *   **Format**: Select `CSV`.
    *   **Scope**: Check `Include children` to get the most granular detail.
7.  Click **Download**.

---

## Step 2: Running the Dashboard

### Option A: Local Run (Python)
If you have Python installed locally:
```bash
# Install dependencies
pip install -r requirements.txt
# Ensure you are logged in for live fetch
az login
# Run the app
streamlit run app.py
```

### Option B: Docker Compose (Recommended for Container)
Run the application without installing Python locally:
```bash
docker-compose up --build
```

Open `http://localhost:8501` in your browser.

---

## Step 3: Performing the Audit

Once the dashboard is open:

1.  **Upload**: Drag and drop your downloaded CSV file into the sidebar uploader.
2.  **Filter**: Use the sidebar to filter by:
    *   **Role Name**: Focus on high-privilege roles like `Owner` or `Contributor`.
    *   **Principal Type**: Compare access between `Users`, `Groups`, and `Service Principals`.
3.  **Analyze**:
    *   **Role Distribution**: See which roles are most common.
    *   **Top Resource Targets**: Identify "Hotspot" resources with the most direct assignments.
    *   **Identity Depth**: Find specific identities that hold multiple high-level permissions.

---

## 🛡️ Security Best Practices
*   **Rotate Exports**: Data exported via CSV is a point-in-time snapshot. Re-run your export weekly for accurate auditing.
*   **Secure Your Local Session**: Ensure your `az login` session is terminated when not in use. This tool only uses your local context and never stores credentials.

---
*Maintained by [Chinmay Jog](https://github.com/chinmaymjog)*
