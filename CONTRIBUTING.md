# Contributing & Testing Guidelines

Thank you for contributing to **Azure RBAC Insight**! This guide ensures that the tool remains a reliable, secure, and user-friendly dashboard for auditing Azure permissions.

## 🛠️ Development Workflow

1.  **Branch First**: Do not commit directly to `main`. Create a short-lived branch such as `feature/<topic>` or `bugfix/<topic>`.
2.  **Environment Setup**:
    *   Python 3.12+ recommended.
    *   Install dependencies: `pip install -r requirements.txt`.
3.  **Local Validation**:
    *   [ ] Run `streamlit run app.py` and verify the UI loads.
    *   [ ] Test **Azure Fetch**: Ensure you are logged in via `az login`.
    *   [ ] Test **CSV Upload**: Use a sample Azure RBAC export.
4.  **Docker Validation**:
    *   [ ] Run `docker-compose up --build` and verify the container starts correctly.
5.  **Commit and PR**:
    *   Use Conventional Commits, for example `feat: add scope hotspot chart` or `docs: update csv export guide`.
    *   Open a Pull Request with summary, testing performed, and any screenshots if the UI changed.

## 🏗️ Adding New Features

When adding new charts, filters, or ingestion methods:

1.  **State Management**: Use `st.session_state` to store processed data so the user doesn't lose their audit progress on every filter change.
2.  **Performance**: Use `@st.cache_data` for heavy processing or SDK calls to keep the UI snappy.
3.  **Visuals**: Follow the `plotly_dark` template for charts to maintain the professional aesthetic.
4.  **Security**: Never hardcode credentials. Use `DefaultAzureCredential` for SDK calls or allow the user to upload local files.

## 🧪 Testing Checklist

Before submitting a Pull Request, verify the following:

### 1. Data Integrity
- [ ] Role names are correctly mapped from GUIDs (via role definition lookup).
- [ ] Scopes are correctly parsed to show human-readable resource names.
- [ ] Multi-subscription fetch correctly aggregates data without duplication.

### 2. UI/UX
- [ ] The dashboard is responsive on different screen sizes.
- [ ] The "Clear Cache / Reset" button works as expected.
- [ ] "Why AzRBAC-Insight?" section is visible and informative for new users.

### 3. Containerization
- [ ] The `.dockerignore` file prevents junk (like `.venv` or `.git`) from entering the build.
- [ ] The `Dockerfile` uses a multi-stage build to keep the image size minimal.

## 📝 Documentation Requirements
- Update `HOW_TO_GUIDE.md` if you add new auditing steps.
- Update `docs/project-spec.md` if scope or success criteria change.
- Update `docs/architecture.md` when a non-trivial design decision is introduced.
- Update `docs/tasks.md` when starting or finishing tracked work.
- If you add a new dependency, ensure it's listed in `requirements.txt`.

---
*Questions? Reach out to [Chinmay Jog](https://github.com/chinmaymjog).*
