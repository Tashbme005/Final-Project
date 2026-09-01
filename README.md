# OAS Bay: Oyera Auto Service Bay Ltd

Records management web app for a Refactory final-year project. The bay services heavy, small and commercial cars for engine oil and filters, gearbox oil and filters, brake fluids, brake pads, greasing, minor repairs, wheel alignment and wheel balance.

A car can receive one or more services in a day. One technician or more can handle a job. Parts (filters, oils and related items) are also sold at the bay.

## Business rules (UGX)

- After the owner buys the required parts, labour is **20,000**.
- Wheel alignment is **30,000**.
- Wheel balance is **20,000**.
- Engine oils range **79,000–200,000**.
- Brake fluids range **13,000–20,000**.
- Oil filters range **15,000–20,000**.

Typical flow: register the customer and vehicle → senior technician inspects and lists parts → owner buys parts → job card is opened in a bay → payment and receipt.

## Setup with pip

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run the app

```bash
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

If you submit an empty or invalid form, the page stays open and shows red error messages. Validation runs on the server, not only in the browser.

Then open [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/).

Demo logins:

- Admin: `admin` / `OasAdmin1` — all pages
- Senior technician: `james` / `OasSenior1` — inspect and record findings, request parts, view services and pick them on a job card. Cannot add services or parts.
- Technician: `mary` / `OasTech1` — only jobs assigned to her, parts issued to her, and client receipts for those jobs


If you see `Error: That port is already in use`, either stop the other server or run:

```bash
python manage.py runserver 8001
```

## Main pages

- `/` Dashboard
- `/orders/customers/` Customers
- `/orders/vehicles/` Vehicles
- `/orders/inspections/` Senior technician inspections
- `/orders/` Job cards
- `/services/` Services and charges
- `/inventory/` Parts on sale
- `/payments/` Payments and receipts
- `/staff/` Technicians and staff
- `/admin/` Django admin
