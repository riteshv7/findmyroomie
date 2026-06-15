# FindMyRoomie (Bangalore)

A mobile-first, responsive web application (Progressive Web App) designed to match roommate seekers and flat listers in Bangalore based on lifestyle preferences that actually cause conflicts (food, smoking, drinking, cleanliness, noise level, guests, pets, and languages).

---

## Features (MVP Scope)

- **Simulated OTP Auth**: Verification via a simulated 6-digit phone SMS OTP code.
- **Profile Roles Setup**: Dual-role select ("Seeker" and/or "Lister") with editable profiles.
- **Multi-step Preferences Wizard**: Detailed input for food cooking preferences, languages, target tenant types, budget limits, and target locations.
- **Post Flat Listings**: Form for listing properties with pricing details (rent, deposit, setup costs), metro landmarks, house rules, and room images (placeholders or custom file uploads).
- **Grouped Lifestyle Search**: Filter room listings by area, rent budget, food options, smoking/drinking tolerances, parking, and pet policies.
- **Compatibility Match Percentage**: Matches listings against user profiles using weighted lifestyle attributes.
- **Proximity Distance Estimation**: Realistically calculates straight-line distances from listings to user work/study neighborhoods.
- **Shortlist Dashboard**: Bidirectional list showing rooms you shortlisted and listers interested in you.
- **1:1 Interactive Chat**: Messaging thread with simulated conversational auto-replies from listers when a seeker expresses interest.
- **Admin Moderation**: Django Admin portal for list reviews and user moderation.

---

## Technology Stack

- **Backend & Templating**: Django (Python 3.14) & Django HTML Templates
- **Database**: SQLite (via Django ORM)
- **Styling**: Vanilla CSS (Mobile-first responsive grids, modern shadows, and glassmorphism)
- **Containerization**: Docker (via production `Dockerfile`)
- **PWA**: PWA Web Manifest & Service Worker caching script

---

## Local Development Guide

### 1. Requirements & Virtual Env
Ensure Python 3.12+ and Node (for workspace tasks) are installed.

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Migration & Seeding
Create the local database and populate it with 9 realistic Bangalore room listings and default test users:

```bash
# Make migrations and migrate
python manage.py makemigrations roommate
python manage.py migrate

# Seed Bangalore listings and create "admin" superuser
python manage.py seed_listings
```
*Note: The seed command automatically creates a superuser account:*
* **Username**: `admin`
* **Password**: `password123`
* **Phone**: `9999999999` (verified)

### 3. Run Server
Start the Django development server:

```bash
python manage.py runserver
```
Go to **[http://localhost:8000/](http://localhost:8000/)** in your browser.

---

## Run Automated Tests

Run the test suite checking matching math, mock distance matrices, and model constraints:

```bash
python manage.py test
```

---

## Deployment to Railway (Production)

This project contains a `Dockerfile` and is fully ready to deploy to **Railway.app** or **Render**:

1. Go to **Railway.app** and link your GitHub account.
2. Click **New Project** -> **Deploy from GitHub repository** -> Select **`findmyroomie`**.
3. Railway will build the container, run migrations, seed listings, and boot the Gunicorn server.
4. **Volume Persistence (Optional but recommended)**: To keep database changes on container rebuilds:
   - In the Railway Canvas, click **+ Add** -> **Volume**.
   - Mount the volume at `/code` so `db.sqlite3` is persisted.
5. In **Settings**, generate a public domain link to share with testers.
