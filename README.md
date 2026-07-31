Zayidni Django scaffold

This folder contains a minimal Django project scaffold for the Zayidni MVP.

Quickstart (local):
1. python -m venv .venv
2. .\.venv\Scripts\Activate.ps1  # or use the appropriate activation for your shell
3. python -m pip install -r requirements.txt
4. set env vars for POSTGRES_* or use sqlite3 by adjusting settings
5. python manage.py migrate
6. python manage.py runserver

Note: This is a scaffold created by Copilot CLI. Install dependencies and finalize settings before production use.

Supported languages: Arabic (default), Kurdish, English. Users choose language on first visit; LocaleMiddleware is enabled.

API endpoints (examples):
- POST /api/users/register/  → register (username, password, email, phone)
- POST /api/users/otp/request/ → request OTP (phone)
- POST /api/users/otp/verify/ → verify OTP (phone, code)
- POST /api/users/login/ → login (username, password)
- POST /api/bids/place/ → place bid (authenticated; phone verified required)

Testing (sqlite in-memory): use zayidni/test_settings.py as DJANGO_SETTINGS_MODULE when running tests.

Security & notes:
- Phone verification is required to place bids to reduce fake bidding.
- Sellers can choose to show contact info; communication and cash collection are between buyer and seller. Platform supports COD and escrow hold flows — implement payment adapters for Zain Cash / Qi Card later.
- Do not store secrets in repository. Use environment variables or GitHub Secrets for CI.
