import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io

# Set page config
st.set_page_config(page_title="AzRBAC-Insight", layout="wide")

# Title and Description
st.title("🛡️ AzRBAC-Insight")
st.markdown("""
This dashboard provides a comprehensive analysis of Azure Role Assignments. 
**Upload your latest report** or explore the default data using the sidebar filters.
""")

# Default CSV Path
DEFAULT_CSV_PATH = "./data/role-assignments-2025-07-14.csv"

def extract_resource_name(scope):
    if not isinstance(scope, str) or not scope:
        return "Unknown"
    # Azure scopes are paths like /subscriptions/xxx/resourceGroups/yyy/...
    # The last part is usually the resource name
    return scope.split('/')[-1]

@st.cache_data
def process_data(data):
    # Process either a file path or a file-like object
    if isinstance(data, str):
        if not os.path.exists(data):
            return pd.DataFrame()
        df = pd.read_csv(data)
    else:
        df = pd.read_csv(data)
        
    # Clean column names (strip BOM or whitespace)
    df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
    
    # Add Simplified Scope (Resource Name)
    if 'Scope' in df.columns:
        df['Resource Name'] = df['Scope'].apply(extract_resource_name)
    
    return df

# Sidebar for Configuration and Filters
st.sidebar.header("📁 Data Source")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload Azure RBAC CSV", type=["csv"])

if uploaded_file is not None:
    df = process_data(uploaded_file)
    st.sidebar.success("Loaded uploaded file!")
else:
    df = process_data(DEFAULT_CSV_PATH)
    if not df.empty:
        st.sidebar.info("Using default report data.")
    else:
        st.sidebar.warning("Default data not found. Please upload a CSV report.")

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("🔍 Filters")
    
    # Resource Name Filter (Simplified Scope)
    all_resources = sorted(df['Resource Name'].unique())
    selected_resources = st.sidebar.multiselect("Select Resource Name", options=all_resources, default=[])
    
    # Role Filter
    all_roles = sorted(df['RoleDefinitionName'].unique())
    selected_roles = st.sidebar.multiselect("Select Roles", options=all_roles, default=[])
    
    # Object Type Filter
    all_types = sorted(df['ObjectType'].unique().astype(str).tolist())
    selected_types = st.sidebar.multiselect("Select Object Types", options=all_types, default=[])

    # Apply Filters
    filtered_df = df.copy()
    if selected_resources:
        filtered_df = filtered_df[filtered_df['Resource Name'].isin(selected_resources)]
    if selected_roles:
        filtered_df = filtered_df[filtered_df['RoleDefinitionName'].isin(selected_roles)]
    if selected_types:
        filtered_df = filtered_df[filtered_df['ObjectType'].astype(str).isin(selected_types)]

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Assignments", len(filtered_df))
    with col2:
        st.metric("Unique Roles", filtered_df['RoleDefinitionName'].nunique())
    with col3:
        st.metric("Unique Principals", filtered_df['ObjectId'].nunique())
    with col4:
        st.metric("Unique Resources", filtered_df['Resource Name'].nunique())

    st.divider()

    # Visualizations
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Top Roles by number of assignments")
        role_counts = filtered_df['RoleDefinitionName'].value_counts().reset_index().head(10)
        role_counts.columns = ['Role', 'Count']
        fig_roles = px.bar(role_counts, x='Count', y='Role', orientation='h', 
                          color='Count', color_continuous_scale='Viridis')
        fig_roles.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_roles, use_container_width=True)

    with col_chart2:
        st.subheader("Assignments by Object Type")
        type_counts = filtered_df['ObjectType'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig_types = px.pie(type_counts, values='Count', names='Type', hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_types, use_container_width=True)

    st.divider()

    # Data Table
    st.subheader("📋 Detailed Assignment Data")
    # Show Resource Name instead of Scope in the default view
    st.dataframe(filtered_df[['DisplayName', 'SignInName', 'RoleDefinitionName', 'ObjectType', 'Resource Name']], use_container_width=True)

else:
    st.info("👋 Welcome! Please upload an Azure Role Assignments CSV file to get started.")

# Footer
st.markdown("---")
st.caption("RBAC Dashboard - Dynamic Auditing Tool")