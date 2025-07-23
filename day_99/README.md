# Day 99 - ⚡ Energy Lens AI (SaaS Edition)

**Discover, analyze, and optimize your team's energy patterns with a secure, multi-user, organization-ready AI platform.**

---

## 🚀 What’s New in Day 99 (vs Day 98)?

- **Explicit Team Creation & Joining:** Admins create teams and generate unique codes; users join teams using these codes. Team names are shown everywhere for clarity.
- **Role Management:** Admins can promote/demote users between admin and user roles from the dashboard.
- **Admin Dashboard Enhancements:** Admins see all users, their roles, and all energy/team data. Team names are shown instead of UUIDs.
- **Team Analytics & Export:** Team tab now includes CSV export, average confidence, and energy level distribution analytics.
- **User Data Sync:** Every authenticated user is automatically added to the users table on login/registration, ensuring robust team and role management.
- **Security Improvements:** Role-based access enforced everywhere. (Email verification, password reset, and MFA are supported via Supabase Auth settings.)
- **Better User Experience:** After joining/creating a team, users see confirmation and the team dashboard. Team code is always displayed for easy sharing.

---

## 🎯 Key Features

### 👥 **Team & Organization Management**
- Admins create teams and share unique codes for users to join
- Team names shown everywhere (no more UUIDs!)
- Admin dashboard: view all users, roles, and team analytics
- Promote/demote users between admin/user roles
- CSV export of team energy data

### 🔒 **Authentication & Security**
- Email verification, password reset, and (optionally) MFA via Supabase Auth
- Role-based access control for all sensitive actions and data
- User data is private to their team/org

### 📸 **Smart Energy Detection**
- Take photos or upload images for energy analysis
- Local ML (DeepFace) for privacy-first emotion/energy detection
- Fallback to OpenCV if needed

### 📊 **AI-Powered Insights & Analytics**
- Personalized productivity tips and scheduling suggestions
- Team-level analytics: average confidence, energy distribution, leaderboard
- Visualize your energy journey and team trends

### 🛠️ **Tech Stack**
- **Frontend:** Streamlit
- **Backend/Auth/DB:** Supabase (Postgres, Auth, Storage)
- **AI/ML:** DeepFace, OpenCV, Pandas, Plotly

---

## 🚀 Quick Start

1. **Clone the repo and navigate to the project directory:**
   ```bash
   cd day_99
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run energy_lens_app.py
   ```
4. **Open your browser:**
   Navigate to `http://localhost:8501`

---

## 🏢 For Organizations & Admins
- Create a team and share the code with your users
- Promote trusted users to admin for co-management
- Download team analytics as CSV for reporting
- All user/team data is private and secure

## 👤 For Users
- Join your team using the code from your admin
- Track your energy, get personalized tips, and see anonymized team stats
- Your data is only visible to your team and admins

---

## 📁 Project Structure

```
day_99/
├── energy_lens_app.py      # Main Streamlit application (SaaS, teams, admin)
├── energy_detector.py      # DeepFace + energy classification
├── pattern_analyzer.py     # Energy pattern analysis
├── visualizations.py       # Charts and graphs
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔧 Customization & Extensibility
- Add new energy levels in `energy_detector.py`
- Customize productivity tips in `pattern_analyzer.py`
- Extend team/org model for enterprise use
- Integrate with Stripe/Paddle for billing (see SaaS checklist in repo)

---

## 🤝 Contributing

This is Day 99 of a 100-day Python and AI challenge. The project demonstrates:
- Multi-user SaaS with Supabase
- Computer vision with local ML
- Data analysis and visualization
- Privacy-first design
- Real-world problem solving

---

## 📄 License

This project is part of a learning journey. Feel free to use, modify, and build upon it!

---

**⚡ Energy Lens - Because knowing your patterns is power!** 
