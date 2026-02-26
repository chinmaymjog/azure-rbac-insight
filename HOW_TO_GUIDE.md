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
source .venv/bin/activate
streamlit run app.py
```

### Option B: Container (Docker)
Run the pre-built container:
```bash
docker run -p 8501:8501 ghcr.io/chinmaymjog/azure-rbac-insight:latest
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
*   **Limit Dashboard Access**: If running in Kubernetes, ensure you use the provided [k8s/manifests.yaml](./k8s/manifests.yaml) which includes basic service exposure, but consider adding an Ingress with Auth for production use.

---
*Maintained by [Chinmay Jog](https://github.com/chinmaymjog)*
