# SpacePoint Web Ecosystem - Version Control & Technical Log

This document tracks the technical architecture, development iterations, and feature implementations of the **Official SpacePoint Landing Page & FastAPI Admin Dashboard**.

---

## 🛠️ Technology Stack

The SpacePoint platform is engineered using a combination of lightweight, high-performance web technologies, ensuring maximum speed, visual impact, and scalability.

### 1. Front-End Core
*   **HTML5 / Semantic Markup**: Fully structured pages, SEO-optimized with proper title tags, meta descriptions, and descriptive element IDs.
*   **Vanilla CSS3 (Custom Styling)**: Used for responsive custom layouts, starry canvas backgrounds, galaxy gradients, glow animations, and custom scrollbar elements.
*   **Tailwind CSS**: Utility-first framework styling the pages, buttons, forms, and responsive components.
*   **JavaScript (ES6+)**: Handles user interaction, modal controllers, responsive navigation menus, scroll anchors, and floating micro-animations.
*   **HTML5 Canvas**: Powers the high-performance twinkling starfield and shooting star backgrounds.

### 2. Back-End Admin Suite (FastAPI MVC)
*   **FastAPI (Python 3)**: An asynchronous, high-speed micro-framework used to construct the backend admin API endpoints.
*   **Uvicorn**: Asynchronous Server Gateway Interface (ASGI) running the FastAPI server.
*   **Jinja2 Templates**: Server-side template rendering engine used to assemble raw HTML pages (`admin_panel.html`, `login.html`) and programmatically generate physical article files using `article_template.html`.
*   **Python-Multipart**: FastAPI dependency used to handle form submissions and image file uploads.
*   **Python Regex (`re`)**: Direct parser translating markdown syntax (`**bold**`, `*italic*`, `[link](url)`) into native semantic HTML tags (`<strong>`, `<em>`, `<a>`).

### 3. Server Deployment & Operations
*   **Nginx Reverse Proxy**: Directs external web traffic on `spacepoint.ae` securely to the internal Python port.
*   **Systemd**: Manages the background execution, crash recovery, and boot-persistence of the FastAPI app via `officialspacepoint.service`.
*   **Certbot (Let's Encrypt)**: Automatically manages SSL/TLS certificates for secure HTTPS routing.
*   **Local Python-based Sync Tools**: Automation scripts (such as `update_nav.py`) ensuring global layout adjustments propagate seamlessly to all page files.

---

## 📂 Implementation Timeline & Release Log

### `v1.4.0` — Production VPS Server Optimization (Current)
*   **Multi-Site Coexistence**: Configured the backend port mapping to run on port `8004` to avoid collisions with the legacy inventory portal running on port `8000` (via `inventory.spacepoint.ae`).
*   **Linux Environment Rebuild**: Resolved the `status=203/EXEC` crash by replacing Windows virtual environment paths with a fresh, clean Linux `venv` and installing required packages natively on the VPS.
*   **Multipart Validation**: Resolved the `1/FAILURE` startup error by installing `python-multipart` to support FastAPI form & image upload streams.
*   **Configured Nginx & Systemd Rules**: Created the verified `/etc/nginx/sites-available/spacepoint.ae` Nginx reverse proxy and `/etc/systemd/system/officialspacepoint.service` configurations.

### `v1.3.0` — Rich Text Upgrades & Formatting Engine
*   **Rich Text Toolbar**: Engineered a selection-aware editor in the Blog Manager. Allows editors to highlight text and apply formatting tags (`Bold`, `Italic`, `Link`, `Subheading`) instantly.
*   **Tailwind Override Protection**: Injected tailored `.article-body` styling overrides into the Jinja2 template header. Forces browser engines to render bold (`<strong>`), italic (`<em>`), and link (`<a>`) tags correctly, overriding Tailwind Preflight resets.
*   **Dynamic Card Deck Rebuilds**: Programmed the model to read `blog.html` and swap HTML blocks inside strict comment delimiters (`<!-- ARTICLE CARDS START -->` ... `<!-- ARTICLE CARDS END -->`), preserving page integrity.

### `v1.2.0` — MVC Admin Dashboard & Datastore
*   **Secure Authentication**: Implemented a cookie-based session token validation checking admin access (`SpacePoint2026!`) for all publishing and editing requests.
*   **Database-Free Registry (`blogs_registry.json`)**: Bootstrapped a JSON flat-file storage handler. This registry stores article metadata alongside raw markdown text, keeping markup readable for secondary edits.
*   **Static Site Generator (SSG)**: Implemented full CRUD logic to output physical HTML articles into `/articles/` during database operations.
*   **Ordering Mechanics**: Added `Move Up` and `Move Down` routing handlers allowing organizers to customize card sorting directly on the dashboard screen.

### `v1.1.0` — Multi-Page Ecosystem Expansion
*   **Integrated Pages (12+)**: Structured a clean navigation grid linking About, Team, Journey, Shop, Case Studies, and platform portals.
*   **Ambassadors Directory**: Crafted a glassmorphic layout displaying Global Ambassadors. Includes built-in SVG flag representations, name tags, and background gradients.
*   **Resources Hub**: Integrated a digital library to host branding guidelines, logos, and a newsletter repository linking PDF newsletters with inline browser preview support.

### `v1.0.0` — Immersive Theme & Front-End Setup
*   **Space Command Style**: Designed the deep-space core style system utilizing vibrant space hues (`#A77DFF`, `#0B0510`, `#5B21B6`) with subtle ambient backdrops.
*   **Canvas Starfields**: Created a customizable Javascript canvas that hooks to window resizing to draw twinkling stars and smooth shooting-star trails.
*   **Custom Intercom Widget**: Integrated customer chat utilities globally.
*   **Rocket Scroll**: Created a custom interactive scroll-to-top component styled as a rocket ship that animates on mouse hover and click.

---

## 🔬 Test Suite & Quality Assurance

A Python integration suite (`scratch/test_admin.py`) was created to programmatically verify all back-end endpoints:

| Endpoint | Method | Purpose | Verified Action |
| :--- | :--- | :--- | :--- |
| `/login` | `GET` | Serve admin login portal | Verifies brand asset mapping. |
| `/login` | `POST` | Authenticate user | Sets cookie token on correct credentials. |
| `/admin` | `GET` | Serve admin console | Loads current article deck. |
| `/publish` | `POST` | Create/Edit articles | Writes physical article files and registry updates. |
| `/reorder` | `GET` | Swap card sequences | Rearranges registry lists and updates `blog.html`. |
| `/delete` | `GET` | Destroy records | Deletes physical article and registry records. |
