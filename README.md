# 👗 Wardrobe Share — Peer-to-Peer Clothing Rental Platform

Wardrobe Share is a community-driven, peer-to-peer clothing rental web application designed to promote sustainable fashion. It allows users to monetize their unused wardrobe items by lending them, while borrowers can access high-quality outfits at a fraction of their retail cost. Built on Python's **Django Framework** and integrated with **Stripe Checkout** for secure, PCI-DSS compliant transactions.

---

## 🚀 Key Features

*   **Flexible Role-Based Accounts:** Users can register as an **Owner** (lender), **Customer** (borrower), or **Both** dynamically.
*   **Secure Authentication & OTP Verification:** Registration is safeguarded by time-limited (5-minute expiry) email OTP validation via SMTP.
*   **Product Listings & Search:** Extensive browsing with server-side filters for Category, Size, Condition, and keyword search.
*   **Automated Booking Workflow:** Real-time rental availability tracking, automated price calculations based on selected days, and return verification.
*   **Late Return Penalty System:** Programmatic calculation of overdue days and automated penalty charge accumulation.
*   **Stripe Integration:** Integrated card payment sessions via Stripe Checkout API with automated transaction logs.
*   **Direct Chat:** Real-time message exchange enabling direct P2P communication between owners and borrowers.
*   **AI Chatbot Assistant:** Built-in keyword-based help agent to answer frequently asked questions about bookings, payments, and listings.
*   **Rating & Review System:** Star-rating and comments module with database constraints preventing review duplication.

---

## 🛠️ Technology Stack

*   **Backend Framework:** Django 4.2 (Python)
*   **Database:** SQLite (Default for development), easily migratable to PostgreSQL
*   **Payment Gateway:** Stripe API
*   **Email Client:** SMTP (Gmail configuration)
*   **Frontend:** HTML5, CSS3,java (Vanilla + Bootstrap components), JavaScript

---

## 📂 Project Structure 

```text
wardrobeshare/
│
├── bookings/          # Booking, rental tracking, and penalty calculations
├── chat/              # Direct P2P chat routing and handling
├── chatbot/           # Automated support assistant views
├── config/            # Core settings, routing, and URL configurations
├── media/             # Dynamic user uploaded images (ignored in Git)
├── payments/          # Stripe transaction sessions and logs
├── products/          # Clothes listings, category filters, and search
├── reviews/           # Product feedback, ratings, and database constraints
├── static/            # Static assets (CSS styles, JS libraries, graphics)
├── templates/         # UI templates
├── users/             # Custom User model, dynamic roles, OTP auth, and decorators
└── manage.py          # Django command line manager
```

---

## ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/bhagyeshnayak/wardrobeshare.git
    cd wardrobeshare
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Copy the example environment template and fill in your credentials:
    ```bash
    # On Linux/macOS:
    cp .env.example .env

    # On Windows (Command Prompt):
    copy .env.example .env

    # On Windows (PowerShell):
    Copy-Item .env.example .env
    ```
    Open the `.env` file and set the required variables:
    *   `DJANGO_SECRET_KEY`: A secure random key for cryptographic signing.
    *   `EMAIL_HOST_USER` & `EMAIL_HOST_PASSWORD`: Your Gmail email address and 16-digit Google App Password for OTP email verification.
    *   `STRIPE_PUBLISHABLE_KEY` & `STRIPE_SECRET_KEY`: Stripe API keys from your dashboard.

5.  **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    Access the application locally at `http://127.0.0.1:8000/`.

---

## 🔒 Security & Standards Implemented

*   **OWASP Top 10 Mitigation:** Built-in safeguards against SQL Injection (parameterized Django ORM), Cross-Site Scripting (HTML auto-escaping), and Cross-Site Request Forgery (`csrf_token` tags).
*   **Cryptographic Cryptography:** Password hashing via **PBKDF2 with SHA-256**.
*   **Financial Precision:** Uses Django `DecimalField` (fixed-point arithmetic) for currency computations to prevent floating-point calculation errors.
