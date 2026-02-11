# AzRBAC-Insight

A Streamlit-based dashboard for analyzing Azure Role-Based Access Control (RBAC) assignments. This tool helps security and cloud administrators visualize and audit role assignments from exported Azure data.

## Features

- **Dynamic Report Upload**: Upload your own Azure role assignment CSV reports directly in the dashboard.
- **Summary Metrics**: Instantly see total assignments, unique roles, unique principals, and scopes.
- **Top Roles Analysis**: Visualization of the most frequently assigned roles.
- **Principal Distribution**: Breakdown of assignments by object type (User, Group, ServicePrincipal).
- **Interactive Filters**: Filter data by scope, role name, and object type using the sidebar.
- **Searchable Data Table**: Detailed view of all filtered assignments.

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Prepare Data
You can either:
- **Upload a CSV**: Use the file uploader in the dashboard sidebar to analyze any report.
- **Use Default**: Place your report in the `data/` directory. The default is `data/role-assignments-2025-07-14.csv`.

### 3. Run the Dashboard
Execute the following command from the project root:
```bash
streamlit run app.py
```

## Cloud Deployment (AKS)

**AzRBAC-Insight** is container-ready and can be deployed to Azure Kubernetes Service (AKS).

### 1. Build and Push Docker Image
```bash
# Build the image
docker build -t <your-registry>/azrbac-insight:latest .

# Push to your Container Registry (e.g., ACR)
docker push <your-registry>/azrbac-insight:latest
```

### 2. Deploy to AKS
Update the image path in `k8s/manifests.yaml`, then run:
```bash
kubectl apply -f k8s/manifests.yaml
```

## Project Structure

- `app.py`: Main dashboard application logic.
- `requirements.txt`: Python dependency list.
- `Dockerfile`: Containerization setup.
- `data/`: Directory for CSV reports.
- `k8s/`: Kubernetes manifests for deployment.

## Technologies Used

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)