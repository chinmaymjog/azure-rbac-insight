# 🛡️ Azure RBAC Insight
## A Local-First Azure RBAC Review Dashboard

A Streamlit-powered security dashboard for analyzing Azure Role-Based Access Control assignments across one or more subscriptions from a single local interface.

> [!TIP]
> This project is optimized for end-user review flow: choose live Azure fetch or offline CSV upload, then filter and inspect RBAC assignments without leaving your local machine.

![Dashboard Preview](./docs/assets/dashboard-preview.png)

## 🚀 Overview

Azure RBAC Insight exists for a common operations problem: reviewing Azure permissions at scale is slow and fragmented in the Azure Portal. This tool provides one place to inspect assignments, filter by role or scope, and identify hotspots quickly.

## System Docs (Engineering Workflow)

- Project specification: docs/project-spec.md
- Architecture decisions: docs/architecture.md
- Execution tracker: docs/tasks.md

---

## ✨ Key Features

| Capability | Description |
| :--- | :--- |
| **Multi-Subscription Fetch** | Aggregate role assignments from multiple subscriptions in one run |
| **Dual-Mode Ingestion** | Use live Azure SDK fetch or offline CSV upload |
| **Visual Analytics** | Review role distribution, principal types, and target hotspots |
| **Granular Filtering** | Slice by subscription, role, and scope |
| **Local-First Runtime** | Keep RBAC data on your machine rather than a hosted backend |

---

## 📋 Prerequisites

### System Requirements
*   **Operating System**: macOS, Linux, or Windows with Python support.
*   **Python**: 3.12+ for local execution.
*   **Docker**: Optional, only needed for container-based local run.
*   **Azure Access**: Reader access to target subscriptions if using live fetch.

Important behavior:
- **Live mode** depends on your local Azure authentication context.
- **CSV mode** is the better choice when you need human-readable display names or need to work offline.

---

## 🛠️ Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/chinmaymjog/azure-rbac-insight.git
cd azure-rbac-insight
```

### 2. Choose Run Mode

#### Mode A (Recommended): Local Python Run

Install dependencies:

```bash
pip install -r requirements.txt
```

If you plan to use live Azure fetch, authenticate first:

```bash
az login
```

Start the dashboard:

```bash
streamlit run app.py
```

Expected local access:
- `http://localhost:8501`

#### Mode B: Docker Compose

Run the app in a container:

```bash
docker-compose up --build
```

Expected local access:
- `http://localhost:8501`

### 3. Choose Data Source Mode

#### Live Azure Fetch

Use this when you want current RBAC data directly from Azure.

Requirements:
- `az login` completed locally
- Reader access to the subscription(s) you want to inspect

Best for:
- Current-state review
- Multi-subscription sweeps
- Fast operator validation

#### Offline CSV Upload

Use this when you want air-gapped review or better identity readability.

Best for:
- Audit snapshots
- Offline analysis
- Human-readable display names from Azure exports

Detailed export instructions are in [HOW_TO_GUIDE.md](/Users/chinmayjog/repos/personal/azure-rbac-insight/HOW_TO_GUIDE.md).

### 4. Verify Health

After startup, confirm:
- The Streamlit app loads at `http://localhost:8501`
- You can select either live fetch or CSV upload
- Charts and filters render after data is loaded

### 5. First Review Flow (Recommended)

Start with one of these user journeys:

1. **Live mode**
    - Login with `az login`
    - Fetch RBAC data
    - Filter by high-privilege roles such as Owner or Contributor

2. **CSV mode**
    - Export RBAC assignments from Azure Portal
    - Upload one or more CSV files
    - Filter by subscription, principal type, and role

Recommended first checks:
- Review role distribution
- Review top resource targets
- Filter for privileged roles
- Compare users, groups, and service principals

### 6. Troubleshooting Notes

- If live fetch fails, re-run `az login` and confirm the correct Azure tenant/subscription context.
- If CSV columns do not parse correctly, re-export using the documented Azure Portal flow.
- If the app starts but charts are empty, verify that data was loaded before filtering.

---

## 📖 Documentation

Use these documents depending on what you need:
- 👉 **[Comprehensive User Guide](./HOW_TO_GUIDE.md)** for CSV export steps and audit walkthrough.
- 👉 **[Project Spec](./docs/project-spec.md)** for goals, scope, and success criteria.
- 👉 **[Architecture Notes](./docs/architecture.md)** for design decisions and runtime boundaries.
- 👉 **[Task Tracker](./docs/tasks.md)** for current work and validation status.

## 🤝 Contributing

Contributions are welcome. See **[CONTRIBUTING.md](./CONTRIBUTING.md)** for branch, validation, and PR workflow expectations.

## 🛡️ Security

This project uses your local Azure authentication context in live mode and keeps analysis local.

- No credentials are hardcoded in the repository.
- No RBAC data is sent to an external backend by design.
- Minimum expected Azure permission for read-only inspection is **Reader**.

---
*Maintained by [Chinmay Jog](https://github.com/chinmaymjog) | 📖 [Read my articles on Medium](https://medium.com/@chinmaymjog)*