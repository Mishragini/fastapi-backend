# FastAPI E-commerce Backend

A simple e-commerce backend API built with FastAPI, featuring user authentication, role-based access control, product management, and order processing. The system includes comprehensive database management using SQLAlchemy with PostgreSQL.

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- PyJWT
- Python-dotenv
- Bcrypt
- Pydantic
- Uvicorn
- Alembic


## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - User login and token generation

### Admin Routes
- `POST /admin/product` - Add new products (Admin only)

### User Routes
- `POST /user/onramp` - Add balance to user account
- `POST /user/buy/{product_id}` - Purchase products
- `GET /user/myOrders` - View order history