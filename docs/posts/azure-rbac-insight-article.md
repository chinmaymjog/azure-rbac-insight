# Auditing Azure RBAC Shouldn't Be This Hard

If you've ever been tasked with reviewing Role-Based Access Control (RBAC) across multiple Azure subscriptions, you know the pain. Navigating the Azure Portal, clicking through every individual resource, and trying to piece together who has access to what is like solving a jigsaw puzzle in the dark.

I built **Azure RBAC Insight** to solve exactly this.

## The Problem: Portal Fatigue
Azure's Access Control (IAM) blade is great for single-resource checks, but it fails at scale. When you need to answer:
- "Which service principals have Owner access anywhere in the tenant?"
- "What are the hotspot resources with the most direct assignments?"
- "Can I see a unified view of all my subscriptions?"

...the portal becomes a bottleneck.

## The Solution: Azure RBAC Insight
Azure RBAC Insight is a lightweight, local Streamlit dashboard that aggregates your Azure role assignments into a single, filterable view.

![Azure RBAC Insight Dashboard](https://raw.githubusercontent.com/chinmaymjog/azure-rbac-insight/main/docs/assets/dashboard-preview.png)

### ✨ Key Features
- **Multi-Subscription Support**: Fetch data from dozens of subscriptions in one click.
- **Visual Analytics**: Instantly spot role distributions and principal types.
- **Granular Auditing**: Drill down into specific identities and resource scopes with ease.
- **Dual-Mode Ingestion**: Use live Azure fetch with `az login` or work from offline CSV exports.

![Detailed Audit Logs](https://raw.githubusercontent.com/chinmaymjog/azure-rbac-insight/main/docs/assets/audit-logs-preview.png)

- **Local & Secure**: Runs on your machine, using your existing `az login` credentials. No data leaves your environment.
- **Offline Mode**: Already have a CSV export? Just upload it for instant analysis.

## 🚀 How to Use It
The tool is open-source and ready to run via Python or Docker, following the same end-user flow documented in the repository README.

```bash
# Clone and Run
git clone https://github.com/chinmaymjog/azure-rbac-insight.git
cd azure-rbac-insight
pip install -r requirements.txt
streamlit run app.py
```

## 🏗️ Architecture
Built with a platform engineering mindset, the tool uses the Azure SDK for Python to securely fetch live data and Plotly for interactive visualizations.

Check out the project on GitHub: [Azure RBAC Insight](https://github.com/chinmaymjog/azure-rbac-insight)

For the full user flow, troubleshooting steps, and project docs, start with the repository README and linked guide files.

---
*Follow me for more DevOps and Platform Engineering tools!*
