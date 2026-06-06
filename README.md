# SpacePoint Website - Official Landing Page & Platform

A premium, immersive, and fully responsive space-themed web ecosystem built for **SpacePoint**. This project empowers the next generation of space explorers through hands-on satellite education, workshops, and innovative digital platforms.

It features a high-end static front-end coupled with an **MVC-architected FastAPI Admin Panel** to manage, publish, edit, delete, and reorder dynamic blog articles without the overhead of an external database.

---

## 🚀 Key Features & Implementation Summary

### 1. Visual & Immersive Design
*   **Space Aesthetic**: Deep space color palette (`#05030A`) with violet/purple accents and premium glassmorphic UI components.
*   **Dynamic Backgrounds**: Custom HTML5 Canvas-based starry background with twinkling and shooting star animations.
*   **Nebula Effects**: High-performance responsive "nebula" glows that adapt across all device types.
*   **Interactive Cursor**: Custom glowing star cursor with responsive scaling on interactive elements.

### 2. Multi-Page Architecture
*   **Unified Ecosystem**: 12+ integrated pages including **About**, **Our Journey**, **Team**, **Alumni**, **Ambassadors**, and **Our Platforms**.
*   **Ambassadors Page**: A dedicated high-end grid showcasing global SpacePoint ambassadors with profile-integrated flags and glassmorphic cards.
*   **Our Platforms**: A centralized hub for SpacePoint's LMS and training portals (Africa LMS, Space Industry LMS, Instructor Platform, etc.).
*   **Resources Hub**: Official branding assets, logos, and a dedicated **Monthly Newsletter** archive with integrated PDF viewing/downloading.

### 3. FastAPI MVC Admin Panel (Control Room)
*   **Dynamic Blog Manager**: Full CRUD actions (Publish, Edit, Update, Delete) and custom ordering (Move Up/Down) of static blog cards.
*   **Registry-Based Storage**: Database-free structure relying on `blogs_registry.json`. Keeps raw text formatting (e.g. `**bold**`) intact for editing inputs.
*   **Static Site Generator (SSG)**: Creates physical `article[ID].html` pages on disk using Jinja2 templates and regenerates the cards grid in `blog.html` inside strict marker blocks.
*   **Rich Text Toolbar**: In-browser selection-aware markdown formatting toolbar for Bold, Italic, Link insertion, Subheadings, and Paragraph structures.
*   **Tailwind Override Protection**: Custom stylesheet resets to force rendering of `strong`, `em`, and `a` styles inside static articles.

### 4. Responsiveness & Security
*   **Mobile-First Design**: Optimized using Tailwind CSS with a collapsible slide-over sidebar and overlays.
*   **Secure Authentication**: Secure level-1 login auth session cookie verification guarding dashboard operations.
*   **Automation Tools**: Python-based synchronization scripts to maintain structural consistency (Navigation, Footers) across all pages.

---

## 📂 Project Structure

```text
SpacePoint-LandingPage/
├── admin_backend/                # MVC Admin Dashboard Backend
│   ├── main.py                   # FastAPI server entry point
│   ├── controllers/              # Request routers & formatting logic
│   │   ├── __init__.py
│   │   └── blog_controller.py    # Login, publish, edit, delete, and reorder routes
│   ├── models/                   # Data logic, templates, and bootstrap utilities
│   │   ├── article_template.html # Jinja2 HTML layout for generated articles
│   │   ├── blog_model.py         # JSON storage handlers & Blog SSG page rebuilder
│   │   ├── blogs_registry.json   # Datastore containing article records
│   │   └── init_registry.py      # Bootstrap script to parse legacy HTML files
│   └── views/                    # UI views (HTML templates)
│       ├── admin_panel.html      # Control panel management dashboard
│       └── login.html            # Admin authorization portal
│
├── assets/                       # Static media, CSS, and interactive scripts
│   ├── css/
│   │   └── style.css             # starfield effects, cursor animations, custom scrollbars
│   ├── js/
│   │   └── script.js             # Global menus, modal triggers, scroll systems
│   └── img/                      # Organized branding images & media clips
│
├── scripts/                      # Site-wide HTML validation & header sync scripts
│   └── update_nav.py
│
├── articles/                     # Generated article viewpages
│   ├── article1.html
│   └── articleN.html
├── run_admin.bat                 # Windows batch shortcut to launch admin panel
├── index.html                    # Homepage portal
├── blog.html                     # Blog landing index (programmatically updated)
└── README.md                     # Documentation
```

---

## 🛠 Setup & Running Locally

### 1. Requirements
*   Python 3.8+
*   FastAPI & Uvicorn
*   Jinja2

Install required packages:
```bash
pip install fastapi uvicorn jinja2 requests
```

### 2. Start the Server
You can launch the admin dashboard using the command line:
```bash
python admin_backend/main.py
```
Or double-click the **`run_admin.bat`** file from the root directory on Windows systems.

The server will spin up on **`http://localhost:8000`**:
*   Public Landing Page: `http://localhost:8000/`
*   Blog Page: `http://localhost:8000/blog.html`
*   Admin Control Panel: `http://localhost:8000/admin` (Redirects to `/login`)

### 3. Dashboard Authentication Credentials
Access the administrator suite using the following credentials:
*   **Username**: `admin`
*   **Password**: `SpacePoint2026!`

---

## 🧪 Testing and Verification
Run programmatic end-to-end integration tests to verify routes, templates, edits, and reordering flows:
```bash
python "C:\Users\ahmad yacine\.gemini\antigravity-ide\brain\de7dbd1e-9080-4c64-8a33-d1dbd7adcf62\scratch\test_admin.py"
```
*(All endpoints are verified against authorization redirects, file modifications, deletion hooks, and HTML builds).*
