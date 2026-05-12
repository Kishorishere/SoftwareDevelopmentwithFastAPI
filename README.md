# Fusemachines Fellowship — Week 2: PostgreSQL + FastAPI

A REST API built with FastAPI and PostgreSQL, containerized with Docker. Based on the Classic Models dataset with 8 tables and ~3,800 rows.

## Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **PostgreSQL 15** — database (via Docker)
- **Pydantic** — data validation
- **Docker Compose** — containerized database

## Project Structure

```
week2/
├── docker-compose.yml
├── .env                   # credentials (not committed)
├── .env.example           # template for credentials
├── seed.sql               # database schema + data
└── app/
    ├── main.py            # app entry point, router registration
    ├── database.py        # SQLAlchemy engine + session
    ├── models.py          # ORM models for all 8 tables
    ├── schemas/           # Pydantic request/response models
    ├── crud/              # database query logic
    └── routers/           # FastAPI route definitions
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Kishorishere/SoftwareDevelopmentwithFastAPI.git
cd SoftwareDevelopmentwithFastAPI
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials.

### 3. Start the database

```bash
docker compose up -d
```

This starts PostgreSQL and automatically runs `seed.sql` to create and populate all 8 tables.

### 4. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic email-validator
```

### 5. Run the API

```bash
cd app
python -m uvicorn main:app --reload
```

API is available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

## API Endpoints

### Resources (full CRUD for each)

| Resource | Base URL |
|----------|----------|
| Customers | `/customers` |
| Products | `/products` |
| Product Lines | `/productlines` |
| Offices | `/offices` |
| Employees | `/employees` |
| Orders | `/orders` |
| Order Details | `/orderdetails` |
| Payments | `/payments` |

Each resource supports:
- `GET /resource` — list all (with `skip` and `limit` pagination)
- `GET /resource/{id}` — get by ID
- `POST /resource` — create
- `PUT /resource/{id}` — update
- `DELETE /resource/{id}` — delete

### Related Data

- `GET /customers/{id}/orders`
- `GET /customers/{id}/payments`
- `GET /employees/{id}/customers`
- `GET /employees/{id}/reports`
- `GET /offices/{id}/employees`
- `GET /products/{id}/orderdetails`
- `GET /productlines/{id}/products`
- `GET /orders/{id}/orderdetails`

### Counts (Task 3 — Concurrency)

- `GET /overall_counts` — fetches all 8 table counts simultaneously using `asyncio.gather()`
- `GET /customers/count`
- `GET /orders/count`
- `GET /products/count`
- `GET /employees/count`
- `GET /offices/count`
- `GET /payments/count`
- `GET /orderdetails/count`
- `GET /productlines/count`

## Twelve-Factor App Principles Applied

- **Factor III (Config)** — credentials stored in `.env`, never hardcoded
- **Factor IV (Backing Services)** — PostgreSQL runs as an attached service via Docker
- **Factor VIII (Concurrency)** — `/overall_counts` uses `asyncio.gather()` to query all tables simultaneously
- **Factor X (Dev/Prod Parity)** — Docker ensures the same database environment everywhere
