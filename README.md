# Care Home Document Management System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A comprehensive document management solution designed specifically for care home environments. Features version control, compliance tracking, searchable repository, and intuitive dark-themed interface.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen)

## 🎯 Project Overview

**Created:** July 2023  
**Author:** Ayoolumi Melehon  
**Category:** Care Administration / Document Management

### Problem Statement

Care homes face significant document management challenges:
- Documents scattered across shared drives, emails, and physical files
- Multiple versions of policies causing confusion and compliance risks
- No audit trail of document changes or approvals
- Difficulty finding correct, current versions of procedures
- Time-consuming preparation for regulatory inspections
- Inconsistent document formats across departments

### Solution

This system provides:
- **Centralized Repository** - Single source of truth for all documents
- **Version Control** - Complete history of document changes
- **Compliance Tracking** - Automated expiry and review date monitoring
- **Smart Search** - Find documents quickly by title, content, or tags
- **Activity Logging** - Full audit trail for regulatory compliance
- **Dark Theme UI** - Modern, professional interface matching care home branding

## 🚀 Features

### Core Features
- 📄 **Document Upload & Storage** - Support for PDF, Word, Excel, PowerPoint, Images
- 🔍 **Advanced Search** - Full-text search with filters
- 📊 **Version Control** - Track changes and maintain document history
- ⏰ **Expiry Tracking** - Automated alerts for expiring documents
- 📋 **Review Scheduling** - Monitor documents due for review
- 📈 **Analytics Dashboard** - Visual insights into document usage
- 📝 **Activity Logging** - Complete audit trail

### Document Categories
- Policies & Procedures
- Care Plans & Assessments
- Staff Training Records
- Health & Safety Documents
- Quality Assurance Reports
- HR Documents
- Meeting Minutes
- Regulatory Correspondence
- Templates & Forms
- Resident Records

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Database | SQLite |
| Charts | Plotly |
| PDF Processing | PyPDF2 |
| Word Processing | python-docx |
| Excel Processing | openpyxl |
| Styling | Custom CSS |

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/ayoolumi/care-home-document-management.git
cd care-home-document-management
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:8501`

## 🖥️ Usage

### Dashboard
- View document statistics at a glance
- Monitor expiring documents and review schedules
- See recent activity and uploads

### Upload Documents
1. Navigate to "Upload Document" in sidebar
2. Fill in document details (title, category, dates)
3. Select file to upload
4. Click "Upload Document"

### Search Documents
- Use the search bar on the Search page
- Apply category and date filters
- Download documents directly from search results

### Manage Compliance
- Check "Expiring Soon" for documents needing renewal
- Review "Due for Review" for scheduled document reviews
- Use Analytics to identify trends and gaps

## 📁 Project Structure

```
care-home-document-management/
├── app.py                  # Main Streamlit application
├── database.py             # Database operations module
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── documents.db           # SQLite database (created on first run)
```

## 🔐 Security Considerations

- All documents stored locally in SQLite database
- No external API calls or data transmission
- Designed for internal network deployment
- Activity logging for audit compliance

## 🎨 UI Design

The application features a modern dark theme with teal/blue accent colors:
- **Primary Color:** #0d9488 (Teal)
- **Accent Color:** #3b82f6 (Blue)
- **Background:** #0f172a (Dark Slate)
- **Cards:** #1e293b (Slate)

## 📊 Screenshots

### Dashboard
- Real-time statistics
- Category breakdown chart
- Upcoming deadlines timeline
- Recent documents grid

### Document Management
- List view with filtering
- Document details with version history
- One-click download

### Compliance Tracking
- Expiry alerts with countdown
- Review schedule management
- Visual urgency indicators

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ayoolumi Melehon**
- Portfolio: [ayofemimelehon.com](https://ayofemimelehon.com)
- GitHub: [@ayoolumi](https://github.com/ayoolumi)
- LinkedIn: [Ayoolumi Melehon](https://linkedin.com/in/ayoolumi-melehon-b63237179)
- Email: ayoolumimelehon@gmail.com

## 🙏 Acknowledgments

- Streamlit team for the excellent framework
- Plotly for beautiful visualizations
- The care home sector for inspiring this solution

---

*This project was created as part of a portfolio demonstrating data science and AI solutions for healthcare and care sector applications.*
