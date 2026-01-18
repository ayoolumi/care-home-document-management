"""
Care Home Document Management System
=====================================
A comprehensive document management solution for care home environments
featuring version control, compliance tracking, and searchable repository.

Created: July 2023
Author: Ayoolumi Melehon
GitHub: github.com/ayoolumi
Portfolio: ayofemimelehon.com
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import database as db
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Care Home Document Management System",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with teal accents
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f1f5f9 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #2dd4bf !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    /* Custom card styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 24px;
        margin: 8px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card h3 {
        color: #94a3b8 !important;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .metric-card .value {
        color: #2dd4bf;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
    }
    
    .metric-card.warning .value {
        color: #fbbf24;
    }
    
    .metric-card.danger .value {
        color: #f87171;
    }
    
    /* Document card */
    .doc-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .doc-card:hover {
        border-color: #2dd4bf;
        box-shadow: 0 0 20px rgba(45, 212, 191, 0.15);
        transform: translateY(-2px);
    }
    
    .doc-title {
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .doc-meta {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    
    .category-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
    }
    
    /* Alert boxes */
    .alert-box {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        border: 1px solid #dc2626;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
    }
    
    .alert-box.warning {
        background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
        border-color: #f59e0b;
    }
    
    .alert-box.info {
        background: linear-gradient(135deg, #164e63 0%, #155e75 100%);
        border-color: #06b6d4;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0d9488 0%, #0891b2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.4);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #1e293b;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 20px;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #2dd4bf;
    }
    
    /* Tables */
    .stDataFrame {
        background: #1e293b;
        border-radius: 12px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #1e293b;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 8px;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0d9488 0%, #0891b2 100%);
        color: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #1e293b;
        border: 1px solid #475569;
        border-radius: 8px;
        color: #f1f5f9;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #1e293b;
        border-color: #475569;
        color: #f1f5f9;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background: #1e293b;
        border-color: #475569;
        color: #f1f5f9;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background: #1e293b;
        border-color: #475569;
        color: #f1f5f9;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0d9488 0%, #0891b2 100%);
    }
    
    /* Footer */
    .footer {
        background: #0f172a;
        border-top: 1px solid #334155;
        padding: 24px;
        margin-top: 48px;
        text-align: center;
        color: #64748b;
    }
    
    .footer a {
        color: #2dd4bf;
        text-decoration: none;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes is None:
        return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_file_icon(file_type):
    """Get icon based on file type"""
    icons = {
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'xls': '📗',
        'xlsx': '📗',
        'ppt': '📙',
        'pptx': '📙',
        'txt': '📄',
        'csv': '📊',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'gif': '🖼️'
    }
    return icons.get(file_type.lower() if file_type else '', '📄')


def render_header():
    """Render the application header"""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 40px 0;">
        <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 8px; 
                   background: linear-gradient(135deg, #2dd4bf 0%, #3b82f6 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📁 Care Home Document Management System
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Centralized document control with version tracking, compliance monitoring, and intelligent search
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem;">📁</div>
            <h2 style="color: #2dd4bf; margin: 10px 0 5px 0;">DocManager</h2>
            <p style="color: #64748b; font-size: 0.85rem;">Care Home Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        menu_options = {
            "🏠 Dashboard": "dashboard",
            "📄 All Documents": "documents",
            "📤 Upload Document": "upload",
            "🔍 Search": "search",
            "⚠️ Expiring Soon": "expiring",
            "📋 Due for Review": "review",
            "📊 Analytics": "analytics",
            "📝 Activity Log": "activity",
            "⚙️ Settings": "settings"
        }
        
        selected = st.radio(
            "Navigation",
            list(menu_options.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick stats
        stats = db.get_dashboard_stats()
        st.markdown(f"""
        <div style="padding: 16px; background: #1e293b; border-radius: 12px; margin-top: 16px;">
            <h4 style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 12px;">QUICK STATS</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b;">Total Docs</span>
                <span style="color: #2dd4bf; font-weight: 600;">{stats['total_documents']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b;">Expiring</span>
                <span style="color: #fbbf24; font-weight: 600;">{stats['expiring_soon']}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748b;">For Review</span>
                <span style="color: #f87171; font-weight: 600;">{stats['due_for_review']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 16px 0; color: #64748b; font-size: 0.75rem;">
            <p>Created by <a href="https://ayofemimelehon.com" target="_blank" style="color: #2dd4bf;">Ayoolumi Melehon</a></p>
            <p>July 2023 • v1.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        return menu_options[selected]


def render_dashboard():
    """Render the main dashboard"""
    render_header()
    
    stats = db.get_dashboard_stats()
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📄 TOTAL DOCUMENTS</h3>
            <div class="value">{stats['total_documents']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card warning">
            <h3>⚠️ EXPIRING SOON</h3>
            <div class="value">{stats['expiring_soon']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card danger">
            <h3>📋 DUE FOR REVIEW</h3>
            <div class="value">{stats['due_for_review']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📥 RECENT UPLOADS</h3>
            <div class="value">{stats['recent_uploads']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Documents by Category")
        
        category_stats = db.get_category_stats()
        if category_stats:
            df = pd.DataFrame([dict(row) for row in category_stats])
            
            fig = px.pie(
                df, 
                values='doc_count', 
                names='name',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                ),
                margin=dict(l=20, r=120, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No documents uploaded yet")
    
    with col2:
        st.markdown("### ⏰ Upcoming Deadlines")
        
        expiring = db.get_expiring_documents(30)
        review_due = db.get_documents_for_review(30)
        
        if expiring or review_due:
            # Timeline chart
            deadlines = []
            
            for doc in expiring[:5]:
                deadlines.append({
                    'Document': doc['title'][:30] + '...' if len(doc['title']) > 30 else doc['title'],
                    'Date': doc['expiry_date'],
                    'Type': 'Expiry',
                    'Color': '#ef4444'
                })
            
            for doc in review_due[:5]:
                deadlines.append({
                    'Document': doc['title'][:30] + '...' if len(doc['title']) > 30 else doc['title'],
                    'Date': doc['review_date'],
                    'Type': 'Review',
                    'Color': '#f59e0b'
                })
            
            if deadlines:
                df = pd.DataFrame(deadlines)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
                
                fig = px.timeline(
                    df,
                    x_start='Date',
                    x_end='Date',
                    y='Document',
                    color='Type',
                    color_discrete_map={'Expiry': '#ef4444', 'Review': '#f59e0b'}
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8',
                    showlegend=True,
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No upcoming deadlines in the next 30 days")
    
    # Recent documents
    st.markdown("### 📄 Recent Documents")
    
    recent_docs = db.get_all_documents()[:6]
    
    if recent_docs:
        cols = st.columns(3)
        for i, doc in enumerate(recent_docs):
            with cols[i % 3]:
                file_icon = get_file_icon(doc['file_type'])
                st.markdown(f"""
                <div class="doc-card">
                    <div class="doc-title">{file_icon} {doc['title']}</div>
                    <div class="doc-meta">
                        <span class="category-badge" style="background: {doc['category_color']}20; color: {doc['category_color']};">
                            {doc['category_name'] or 'Uncategorized'}
                        </span>
                        <br><br>
                        📅 {doc['created_at'][:10] if doc['created_at'] else 'Unknown'} • 
                        📦 {format_file_size(doc['file_size'])} •
                        v{doc['version']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No documents uploaded yet. Click 'Upload Document' to get started!")
    
    # Activity feed
    st.markdown("### 📝 Recent Activity")
    
    activity = db.get_recent_activity(10)
    
    if activity:
        for item in activity[:5]:
            action_icons = {
                'upload': '📤',
                'download': '📥',
                'update': '✏️',
                'delete': '🗑️',
                'view': '👁️',
                'new_version': '🔄'
            }
            icon = action_icons.get(item['action'], '📌')
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px 16px; 
                        background: #1e293b; border-radius: 8px; margin: 8px 0;
                        border-left: 3px solid #2dd4bf;">
                <span style="font-size: 1.5rem; margin-right: 16px;">{icon}</span>
                <div style="flex: 1;">
                    <div style="color: #f1f5f9; font-weight: 500;">{item['document_title'] or 'System'}</div>
                    <div style="color: #64748b; font-size: 0.85rem;">
                        {item['details']} • {item['created_at'][:16] if item['created_at'] else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No activity recorded yet")


def render_documents():
    """Render the documents listing page"""
    st.markdown("## 📄 All Documents")
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search documents...", placeholder="Enter keywords...")
    
    with col2:
        categories = db.get_categories()
        category_options = {cat['name']: cat['id'] for cat in categories}
        category_options = {'All Categories': None, **category_options}
        selected_category = st.selectbox("📁 Filter by Category", list(category_options.keys()))
    
    with col3:
        sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Name A-Z"])
    
    # Get documents
    category_id = category_options.get(selected_category)
    documents = db.get_all_documents(category_id=category_id, search_term=search_term if search_term else None)
    
    if documents:
        st.markdown(f"**Found {len(documents)} documents**")
        
        for doc in documents:
            file_icon = get_file_icon(doc['file_type'])
            
            with st.expander(f"{file_icon} {doc['title']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Description:** {doc['description'] or 'No description provided'}
                    
                    **Category:** {doc['category_name'] or 'Uncategorized'}
                    
                    **File:** {doc['file_name']} ({format_file_size(doc['file_size'])})
                    
                    **Version:** {doc['version']}
                    
                    **Uploaded by:** {doc['uploaded_by'] or 'Unknown'}
                    
                    **Upload Date:** {doc['created_at'][:10] if doc['created_at'] else 'Unknown'}
                    """)
                    
                    if doc['expiry_date']:
                        st.markdown(f"**Expiry Date:** {doc['expiry_date']}")
                    if doc['review_date']:
                        st.markdown(f"**Review Date:** {doc['review_date']}")
                
                with col2:
                    # Download button
                    if doc['file_data']:
                        st.download_button(
                            label="📥 Download",
                            data=doc['file_data'],
                            file_name=doc['file_name'],
                            mime="application/octet-stream",
                            key=f"download_{doc['id']}"
                        )
                    
                    # View versions
                    versions = db.get_document_versions(doc['id'])
                    if versions:
                        st.markdown(f"**Version History:** {len(versions)} previous versions")
                    
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{doc['id']}"):
                        db.delete_document(doc['id'], "Admin")
                        st.success("Document deleted!")
                        st.rerun()
    else:
        st.info("No documents found matching your criteria")


def render_upload():
    """Render the upload document page"""
    st.markdown("## 📤 Upload New Document")
    
    with st.form("upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📌 Document Title *", placeholder="e.g., Fire Safety Policy 2023")
            
            categories = db.get_categories()
            category_options = {cat['name']: cat['id'] for cat in categories}
            selected_category = st.selectbox("📁 Category *", list(category_options.keys()))
            
            review_date = st.date_input("📅 Review Date", value=None, help="When should this document be reviewed?")
        
        with col2:
            description = st.text_area("📝 Description", placeholder="Brief description of the document...", height=100)
            
            expiry_date = st.date_input("⏰ Expiry Date", value=None, help="When does this document expire?")
            
            tags = st.text_input("🏷️ Tags", placeholder="Comma-separated tags (e.g., safety, policy, annual)")
        
        uploaded_file = st.file_uploader(
            "📎 Choose file to upload",
            type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv', 'jpg', 'jpeg', 'png', 'gif'],
            help="Supported formats: PDF, Word, Excel, PowerPoint, Text, CSV, Images"
        )
        
        submitted = st.form_submit_button("📤 Upload Document", use_container_width=True)
        
        if submitted:
            if not title:
                st.error("Please enter a document title")
            elif not uploaded_file:
                st.error("Please select a file to upload")
            else:
                # Process upload
                file_data = uploaded_file.read()
                file_name = uploaded_file.name
                file_type = file_name.split('.')[-1] if '.' in file_name else ''
                file_size = len(file_data)
                
                # Parse tags
                tag_list = [t.strip() for t in tags.split(',')] if tags else None
                
                # Add to database
                doc_id = db.add_document(
                    title=title,
                    description=description,
                    category_id=category_options.get(selected_category),
                    file_name=file_name,
                    file_type=file_type,
                    file_size=file_size,
                    file_data=file_data,
                    uploaded_by="Admin",
                    review_date=str(review_date) if review_date else None,
                    expiry_date=str(expiry_date) if expiry_date else None,
                    tags=tag_list
                )
                
                st.success(f"✅ Document '{title}' uploaded successfully!")
                st.balloons()


def render_search():
    """Render the search page"""
    st.markdown("## 🔍 Advanced Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search documents",
            placeholder="Enter keywords, document titles, or tags...",
            label_visibility="collapsed"
        )
    
    with col2:
        search_btn = st.button("🔍 Search", use_container_width=True)
    
    # Filters
    with st.expander("🎛️ Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = db.get_categories()
            category_options = {cat['name']: cat['id'] for cat in categories}
            category_options = {'All Categories': None, **category_options}
            selected_category = st.selectbox("Category", list(category_options.keys()))
        
        with col2:
            date_range = st.selectbox("Date Range", ["Any Time", "Last 7 Days", "Last 30 Days", "Last Year"])
        
        with col3:
            file_type = st.selectbox("File Type", ["All Types", "PDF", "Word", "Excel", "Images"])
    
    if search_query or search_btn:
        category_id = category_options.get(selected_category)
        results = db.get_all_documents(category_id=category_id, search_term=search_query)
        
        st.markdown(f"### Found {len(results)} results")
        
        for doc in results:
            file_icon = get_file_icon(doc['file_type'])
            
            st.markdown(f"""
            <div class="doc-card">
                <div class="doc-title">{file_icon} {doc['title']}</div>
                <div class="doc-meta">
                    <span class="category-badge" style="background: {doc['category_color']}20; color: {doc['category_color']};">
                        {doc['category_name'] or 'Uncategorized'}
                    </span>
                    {doc['description'][:100] + '...' if doc['description'] and len(doc['description']) > 100 else doc['description'] or ''}
                    <br><br>
                    📅 {doc['created_at'][:10] if doc['created_at'] else 'Unknown'} • 
                    📦 {format_file_size(doc['file_size'])} •
                    v{doc['version']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if doc['file_data']:
                st.download_button(
                    label="📥 Download",
                    data=doc['file_data'],
                    file_name=doc['file_name'],
                    mime="application/octet-stream",
                    key=f"search_download_{doc['id']}"
                )


def render_expiring():
    """Render expiring documents page"""
    st.markdown("## ⚠️ Documents Expiring Soon")
    
    days = st.slider("Show documents expiring within:", 7, 90, 30, 7)
    
    expiring_docs = db.get_expiring_documents(days)
    
    if expiring_docs:
        st.warning(f"⚠️ {len(expiring_docs)} documents expiring within {days} days")
        
        for doc in expiring_docs:
            days_until = (datetime.strptime(doc['expiry_date'], '%Y-%m-%d') - datetime.now()).days
            
            urgency_color = '#ef4444' if days_until <= 7 else '#f59e0b' if days_until <= 14 else '#eab308'
            
            st.markdown(f"""
            <div class="alert-box" style="border-left: 4px solid {urgency_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #f1f5f9; font-weight: 600; font-size: 1.1rem;">{doc['title']}</div>
                        <div style="color: #94a3b8; margin-top: 4px;">
                            {doc['category_name'] or 'Uncategorized'} • 
                            Expires: {doc['expiry_date']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {urgency_color}; font-size: 1.5rem; font-weight: 700;">{days_until}</div>
                        <div style="color: #94a3b8; font-size: 0.85rem;">days left</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No documents expiring within the selected timeframe")


def render_review():
    """Render documents due for review"""
    st.markdown("## 📋 Documents Due for Review")
    
    days = st.slider("Show documents due for review within:", 7, 90, 30, 7)
    
    review_docs = db.get_documents_for_review(days)
    
    if review_docs:
        st.info(f"📋 {len(review_docs)} documents due for review")
        
        for doc in review_docs:
            review_date = datetime.strptime(doc['review_date'], '%Y-%m-%d')
            days_until = (review_date - datetime.now()).days
            is_overdue = days_until < 0
            
            if is_overdue:
                st.markdown(f"""
                <div class="alert-box">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #f1f5f9; font-weight: 600; font-size: 1.1rem;">{doc['title']}</div>
                            <div style="color: #fca5a5; margin-top: 4px;">
                                ⚠️ OVERDUE by {abs(days_until)} days • Due: {doc['review_date']}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-box warning">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #f1f5f9; font-weight: 600; font-size: 1.1rem;">{doc['title']}</div>
                            <div style="color: #fcd34d; margin-top: 4px;">
                                Review due: {doc['review_date']} ({days_until} days)
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ No documents due for review within the selected timeframe")


def render_analytics():
    """Render analytics page"""
    st.markdown("## 📊 Document Analytics")
    
    stats = db.get_dashboard_stats()
    
    # Storage usage
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💾 Storage Overview")
        st.metric("Total Storage Used", format_file_size(stats['total_size']))
        st.metric("Total Documents", stats['total_documents'])
    
    with col2:
        st.markdown("### 📈 Document Trends")
        st.metric("Uploaded This Week", stats['recent_uploads'])
        st.metric("Requiring Action", stats['expiring_soon'] + stats['due_for_review'])
    
    # Category breakdown
    st.markdown("### 📁 Documents by Category")
    
    category_stats = db.get_category_stats()
    if category_stats:
        df = pd.DataFrame([dict(row) for row in category_stats])
        
        fig = px.bar(
            df,
            x='name',
            y='doc_count',
            color='doc_count',
            color_continuous_scale=['#0d9488', '#3b82f6'],
            labels={'name': 'Category', 'doc_count': 'Documents'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#334155')
        )
        st.plotly_chart(fig, use_container_width=True)


def render_activity():
    """Render activity log"""
    st.markdown("## 📝 Activity Log")
    
    activity = db.get_recent_activity(100)
    
    if activity:
        # Convert to dataframe
        df = pd.DataFrame([dict(row) for row in activity])
        
        # Format the dataframe
        df = df[['created_at', 'user', 'action', 'document_title', 'details']]
        df.columns = ['Timestamp', 'User', 'Action', 'Document', 'Details']
        
        st.dataframe(df, use_container_width=True, height=500)
    else:
        st.info("No activity recorded yet")


def render_settings():
    """Render settings page"""
    st.markdown("## ⚙️ Settings")
    
    tab1, tab2 = st.tabs(["📁 Categories", "ℹ️ About"])
    
    with tab1:
        st.markdown("### Document Categories")
        
        categories = db.get_categories()
        
        for cat in categories:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px; 
                        background: #1e293b; border-radius: 8px; margin: 8px 0;">
                <span style="font-size: 1.5rem; margin-right: 12px;">{cat['icon']}</span>
                <div style="flex: 1;">
                    <div style="color: #f1f5f9; font-weight: 500;">{cat['name']}</div>
                    <div style="color: #64748b; font-size: 0.85rem;">{cat['description']}</div>
                </div>
                <div style="width: 20px; height: 20px; background: {cat['color']}; border-radius: 50%;"></div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ### About This System
        
        **Care Home Document Management System** is designed specifically for care home environments 
        to manage, track, and organize documents efficiently.
        
        #### Features:
        - 📄 **Document Storage** - Centralized repository for all documents
        - 🔍 **Smart Search** - Find documents quickly by title, content, or tags
        - 📊 **Version Control** - Track document changes and maintain history
        - ⏰ **Compliance Tracking** - Monitor expiry dates and review schedules
        - 📈 **Analytics** - Visual insights into document usage
        - 📝 **Activity Logging** - Complete audit trail of all actions
        
        ---
        
        **Created:** July 2023
        
        **Author:** Ayoolumi Melehon
        
        **Contact:** ayoolumimelehon@gmail.com
        
        **Portfolio:** [ayofemimelehon.com](https://ayofemimelehon.com)
        
        **GitHub:** [github.com/ayoolumi](https://github.com/ayoolumi)
        """)


def main():
    """Main application entry point"""
    # Initialize database
    db.init_database()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "dashboard":
        render_dashboard()
    elif page == "documents":
        render_documents()
    elif page == "upload":
        render_upload()
    elif page == "search":
        render_search()
    elif page == "expiring":
        render_expiring()
    elif page == "review":
        render_review()
    elif page == "analytics":
        render_analytics()
    elif page == "activity":
        render_activity()
    elif page == "settings":
        render_settings()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2023 Care Home Document Management System | Created by 
        <a href="https://ayofemimelehon.com" target="_blank">Ayoolumi Melehon</a></p>
        <p style="margin-top: 8px;">
            <a href="https://github.com/ayoolumi" target="_blank">GitHub</a> • 
            <a href="https://linkedin.com/in/ayoolumi-melehon-b63237179" target="_blank">LinkedIn</a> • 
            <a href="mailto:ayoolumimelehon@gmail.com">Contact</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
