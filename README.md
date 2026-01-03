# Order Management System (OMS)

A RESTful API backend for managing orders, products, suppliers, inventory, and users built with Flask.

## Tech Stack

- **Framework:** Flask 3.1
- **Database:** SQLite (SQLAlchemy 2.0 ORM)
- **Authentication:** JWT (Flask-JWT-Extended)
- **API Documentation:** OpenAPI 3.0 (flask-smorest)
- **Validation:** Marshmallow
- **Password Hashing:** Passlib (PBKDF2-SHA256)

## Project Structure

```
OMS/
├── app.py                 # Application factory
├── requirements.txt       # Dependencies
├── core/                  # Core configuration & extensions
│   ├── config.py          # App configuration
│   ├── extension.py       # Flask extensions (JWT, API)
│   └── error_handling.py  # Global error handlers
├── models/                # SQLAlchemy models
│   ├── base.py            # Database engine & session
│   ├── user.py
│   ├── order.py
│   ├── order_item.py
│   ├── product.py
│   ├── category.py
│   ├── supplier.py
│   ├── inventory.py
│   └── product_category.py
├── resources/             # API endpoints (controllers)
│   ├── auth.py
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   ├── supplier.py
│   └── inventory.py
├── schemas/               # Marshmallow schemas
│   ├── base_schema.py
│   └── ...
└── data/                  # Database files
    └── db.sqlite3
```

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DB_URL=sqlite:///data/db.sqlite3
SECRET_KEY=your-super-secret-key-here
```

### 4. Run the application

```bash
python app.py
```

The server will start at `http://localhost:8080`

## API Documentation

Swagger UI is available at:
```
http://localhost:8080/api/swagger
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login with email/password |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Logout (revoke token) |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users |
| POST | `/users` | Create a new user |
| GET | `/users/<id>` | Get user by ID |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List products (with filters) |
| POST | `/products` | Create a product |
| GET | `/products/<id>` | Get product by ID |
| PUT | `/products/<id>` | Update product |
| DELETE | `/products/<id>` | Delete product |

**Query Parameters for GET /products:**
- `supplier_id` - Filter by supplier
- `category_id` - Filter by category
- `min_price` - Minimum price
- `max_price` - Maximum price

### Suppliers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/suppliers` | List all suppliers |
| POST | `/suppliers` | Create a supplier |
| GET | `/supplier/<id>` | Get supplier by ID |
| PUT | `/supplier/<id>` | Update supplier |
| DELETE | `/supplier/<id>` | Delete supplier |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| POST | `/categories` | Create a category |
| GET | `/categories/<id>` | Get category by ID |
| PUT | `/categories/<id>` | Update category |
| DELETE | `/categories/<id>` | Delete category |

### Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | List all inventory |
| POST | `/inventory` | Add product to inventory |
| PUT | `/inventory/<id>` | Update inventory quantity |
| GET | `/inventory/product/<product_id>` | Get inventory for product |

