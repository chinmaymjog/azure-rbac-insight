import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.authorization import AuthorizationManagementClient

# Set page config
st.set_page_config(page_title="AzRBAC-Insight", layout="wide", page_icon="🛡️")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Description
st.title("🛡️ AzRBAC-Insight")
st.markdown("""
Analyzing Azure Role-Based Access Control (RBAC) across multiple subscriptions.
**Fetch directly from Azure** (requires `az login`) or **Upload a CSV export**.
""")

# --- Helper Functions ---

@st.cache_resource
def get_credentials():
    return DefaultAzureCredential()

@st.cache_data
def get_subscriptions():
    try:
        cred = get_credentials()
        sub_client = SubscriptionClient(cred)
        subs = list(sub_client.subscriptions.list())
        return {sub.display_name: sub.subscription_id for sub in subs}
    except Exception as e:
        st.sidebar.error(f"Error fetching subscriptions: {e}")
        return {}

@st.cache_data
def get_role_definitions(subscription_id):
    """Fetch role definitions to map GUIDs to names."""
    try:
        cred = get_credentials()
        auth_client = AuthorizationManagementClient(cred, subscription_id)
        role_defs = list(auth_client.role_definitions.list(scope=f"/subscriptions/{subscription_id}"))
        return {rd.id.split('/')[-1]: rd.role_name for rd in role_defs}
    except Exception:
        return {}

def extract_resource_name(scope):
    if not isinstance(scope, str) or not scope:
        return "Subscription Level"
    # Azure scopes are paths like /subscriptions/xxx/resourceGroups/yyy/...
    parts = scope.split('/')
    if len(parts) > 4:
        return parts[-1]
    return "Subscription Level"

@st.cache_data
def fetch_all_rbac(selected_subs_dict):
    """Fetch and aggregate RBAC assignments from multiple subscriptions."""
    all_data = []
    progress_text = "Fetching Azure Data..."
    my_bar = st.progress(0, text=progress_text)
    
    total = len(selected_subs_dict)
    for i, (name, sub_id) in enumerate(selected_subs_dict.items()):
        my_bar.progress((i + 1) / total, text=f"Processing {name}...")
        try:
            cred = get_credentials()
            auth_client = AuthorizationManagementClient(cred, sub_id)
            assignments = list(auth_client.role_assignments.list_for_subscription())
            
            # Get role mapping for this sub
            role_map = get_role_definitions(sub_id)
            
            for ra in assignments:
                role_def_id = ra.role_definition_id.split('/')[-1]
                role_name = role_map.get(role_def_id, role_def_id)
                
                all_data.append({
                    'Subscription': name,
                    'Principal (ID)': ra.principal_id, # SDK only returns ID, Name requires Graph API
                    'ObjectId': ra.principal_id,
                    'RoleDefinitionName': role_name,
                    'ObjectType': ra.principal_type,
                    'Scope': ra.scope,
                })
        except Exception as e:
            st.error(f"Failed to fetch for {name}: {e}")
            
    my_bar.empty()
    return pd.DataFrame(all_data)

def process_csv(uploaded_files):
    all_dfs = []
    try:
        for file in uploaded_files:
            temp_df = pd.read_csv(file)
            # Clean column names
            temp_df.columns = [col.strip().replace('\ufeff', '') for col in temp_df.columns]
            # Use filename (minus ext) as sub name if not present or generic
            sub_name = os.path.splitext(file.name)[0]
            # Clean up Azure Portal default suffix (e.g., _role-assignments-2024-05-16)
            for suffix in ["_role-assignments", "-role-assignments", " role-assignments"]:
                if suffix in sub_name:
                    sub_name = sub_name.split(suffix)[0]
            
            if 'Subscription' not in temp_df.columns:
                temp_df['Subscription'] = sub_name
            all_dfs.append(temp_df)
            
        if not all_dfs:
            return pd.DataFrame()
        return pd.concat(all_dfs, ignore_index=True)
    except Exception as e:
        st.error(f"Error processing CSV files: {e}")
        return pd.DataFrame()

# --- Sidebar ---

st.sidebar.header("📥 Data Input")

# Mode Selection
input_mode = st.sidebar.radio("Input Source", ["Azure SDK (Live)", "CSV Upload (Offline)"])

df = pd.DataFrame()

if input_mode == "Azure SDK (Live)":
    st.sidebar.subheader("🔌 Azure Connection")
    subscriptions = get_subscriptions()
    if subscriptions:
        selected_sub_names = st.sidebar.multiselect("Select Subscriptions", 
                                                   options=list(subscriptions.keys()),
                                                   default=list(subscriptions.keys())[:1] if subscriptions else [])
        
        if st.sidebar.button("Fetch Data"):
            selected_dict = {name: subscriptions[name] for name in selected_sub_names}
            with st.spinner("Fetching data from Azure..."):
                df = fetch_all_rbac(selected_dict)
                if not df.empty:
                    st.session_state['df'] = df
                    st.sidebar.success(f"Fetched {len(df)} assignments!")
    else:
        st.sidebar.warning("No subscriptions found. Run 'az login' locally.")

else:
    st.sidebar.subheader("📄 Upload Reports")
    uploaded_files = st.sidebar.file_uploader("Choose CSV files (Azure Exports)", type="csv", accept_multiple_files=True)
    if uploaded_files:
        df = process_csv(uploaded_files)
        if not df.empty:
            st.session_state['df'] = df
            st.sidebar.success(f"Uploaded {len(uploaded_files)} files!")

# Load data from session state
if 'df' in st.session_state:
    df = st.session_state['df']

# --- Dashboard Logic ---

if not df.empty:
    # Add Resource Name helper
    if 'Resource Name' not in df.columns and 'Scope' in df.columns:
        df['Resource Name'] = df['Scope'].apply(extract_resource_name)

    # Filters
    st.sidebar.header("🔍 Filters")
    
    sub_list = sorted(df['Subscription'].unique())
    sel_subs = st.sidebar.multiselect("Subscriptions", sub_list, default=sub_list)
    
    role_list = sorted(df['RoleDefinitionName'].unique())
    sel_roles = st.sidebar.multiselect("Roles", role_list, default=role_list)

    type_list = sorted(df['ObjectType'].unique().astype(str).tolist())
    sel_types = st.sidebar.multiselect("Principal Types", type_list, default=type_list)

    # Apply Filters
    filtered_df = df[df['Subscription'].isin(sel_subs)]
    filtered_df = filtered_df[filtered_df['ObjectType'].astype(str).isin(sel_types)]
    if sel_roles:
        filtered_df = filtered_df[filtered_df['RoleDefinitionName'].isin(sel_roles)]

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Assignments", len(filtered_df))
    m2.metric("Unique Roles", filtered_df['RoleDefinitionName'].nunique())
    m3.metric("Principals", filtered_df['ObjectId'].nunique())
    m4.metric("Resources", filtered_df['Resource Name'].nunique())

    st.divider()

    # Visuals
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Top Roles")
        role_counts = filtered_df['RoleDefinitionName'].value_counts().reset_index().head(10)
        role_counts.columns = ['Role', 'Count']
        fig_roles = px.bar(role_counts, x='Count', y='Role', orientation='h', color='Count', template="plotly_dark")
        st.plotly_chart(fig_roles, width="stretch")

    with c2:
        st.subheader("Principal Distribution")
        type_counts = filtered_df['ObjectType'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig_types = px.pie(type_counts, values='Count', names='Type', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_types, width="stretch")

    st.divider()

    # Table
    st.subheader("📋 Detailed Audit Logs")
    # Determine the principal column name based on data
    p_col = 'Principal (ID)' if 'Principal (ID)' in filtered_df.columns else 'DisplayName'
    st.dataframe(filtered_df[['Subscription', p_col, 'RoleDefinitionName', 'ObjectType', 'Resource Name']], 
                 width="stretch", hide_index=True)

    if st.button("Clear Cache / Reset"):
        st.session_state.clear()
        st.rerun()

else:
    st.info("👋 Welcome! Fetch data from Azure or upload a CSV export to begin your RBAC audit.")
    
    with st.expander("Why AzRBAC-Insight?"):
        st.write("""
        Auditing RBAC via the Azure Portal can be tedious, especially when you need to see who has access to what 
        across dozens of subscriptions and thousands of resources. 
        
        **AzRBAC-Insight** was built to provide a unified, filterable view to:
        1. Identify over-privileged identities.
        2. Spot "Hotspot" resources with too many direct assignments.
        3. Compare permissions across multiple subscriptions in seconds.
        """)

# Footer
st.caption("Azure RBAC Insight - Built for Security Architects")