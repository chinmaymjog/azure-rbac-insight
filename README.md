# 🛡️ Azure RBAC Insight

**Azure RBAC Insight** is a Streamlit-powered security dashboard designed for deep-dive analysis and visualization of Azure Role-Based Access Control (RBAC) assignments. 

It empowers cloud administrators to identify over-privileged identities, visualize complex permissions, and maintain a secure cloud posture through interactive data exploration.

---

## ✨ Key Features

*   **Visual Insights**: Instantly see role distributions between Users, Groups, and Service Principals using interactive Plotly charts.
*   **Resource Hotspots**: Identify which Azure resources have the most direct role assignments.
*   **Granular Filtering**: Slice and dice permission data by Scope, Role Name, and Identity Type.
*   **Multi-Platform**: Deployable as a Python process, a Docker container, or a Kubernetes pod.

---

## 🏗️ Quick Start

### 1. Requirements
*   Python 3.12+
*   An Azure Role Assignments CSV export ([See Guide](./HOW_TO_GUIDE.md))

### 2. Installation
```bash
git clone https://github.com/chinmaymjog/azure-rbac-insight.git
cd azure-rbac-insight
pip install -r requirements.txt
```

### 3. Run
```bash
streamlit run app.py
```

---

## 📖 Documentation
For detailed instructions on how to export your data from Azure and use the advanced filtering features, check out the:
👉 **[Comprehensive User Guide](./HOW_TO_GUIDE.md)**

---

## 🛠️ Deployment

### Docker
```bash
docker build -t azure-rbac-insight .
docker run -p 8501:8501 azure-rbac-insight
```

### Kubernetes (AKS)
Manifests for deploying to a Kubernetes cluster are provided in the `k8s/` directory.
```bash
kubectl apply -f k8s/manifests.yaml
```

---
*Maintained by [Chinmay Jog](https://github.com/chinmaymjog)*