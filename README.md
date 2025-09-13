# Hotel Booking Cancellation Prediction System

A FastAPI backend system for predicting hotel booking cancellations using machine learning. This system provides a comprehensive API for managing users, rooms, bookings, and cancellation predictions.

## Features

- **User Management**: Registration and authentication for clients and admins
- **Room Management**: CRUD operations for hotel rooms with ML-compatible room codes
- **Booking System**: Complete booking lifecycle with cancellation tracking
- **ML Integration Ready**: Prepared endpoints for cancellation prediction models
- **Role-based Access Control**: Separate permissions for clients and admins
- **Database Integration**: Supabase PostgreSQL with proper schema design

## Project Structure

```
hotel-booking-prediction/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration and environment variables
│   ├── database.py            # Database connection and operations
│   ├── models.py              # Pydantic models for data validation
│   ├── auth.py                # Authentication and authorization
│   └── routes/
│       ├── __init__.py
│       ├── auth.py            # Authentication endpoints
│       ├── rooms.py           # Room management endpoints
│       └── bookings.py        # Booking management endpoints
├── requirements.txt           # Python dependencies
├── env_example.txt           # Environment variables template
├── database_schema.sql       # Database schema for Supabase
├── rooms_table_modification.sql  # Room table modifications
└── README.md                 # This file
```

## Prerequisites

- Python 3.8+
- Supabase account and project
- PostgreSQL database (via Supabase)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hotel-booking-prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file with your Supabase credentials:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   DATABASE_URL=postgresql://postgres:[password]@[host]:[port]/[database]
   SECRET_KEY=your_secret_key_for_jwt
   ```

5. **Set up database**
   - Execute `database_schema.sql` in Supabase SQL Editor
   - Execute `rooms_table_modification.sql` in Supabase SQL Editor

## Running the Application

### Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user (client or admin)
- `POST /login` - User login
- `GET /me` - Get current user info
- `POST /logout` - User logout

### Rooms (`/api/v1/rooms`)
- `GET /` - List all rooms (with filtering)
- `GET /{room_id}` - Get specific room
- `POST /` - Create room (Admin only)
- `PUT /{room_id}` - Update room (Admin only)
- `DELETE /{room_id}` - Delete room (Admin only)

### Bookings (`/api/v1/bookings`)
- `POST /` - Create booking (Client only)
- `GET /` - Get user's bookings
- `GET /{booking_id}` - Get specific booking
- `PUT /{booking_id}` - Update booking
- `POST /{booking_id}/cancel` - Cancel booking (Client only)
- `POST /predict-cancellation` - Predict cancellation (Admin only)

## Database Schema

The system uses a PostgreSQL database with the following main tables:

- **users**: User accounts (clients and admins)
- **rooms**: Hotel room types with ML-compatible codes
- **bookings**: Booking details with prediction features
- **history**: Cancellation history tracking

See `database_schema.sql` for complete schema details.

## ML Integration

The system is prepared for ML model integration:

1. **Room Codes**: Rooms have ML-compatible codes (`room_type_1`, `room_type_2`, etc.)
2. **Prediction Endpoint**: `/api/v1/bookings/predict-cancellation` ready for ML integration
3. **Feature Extraction**: Booking data includes all necessary features for prediction
4. **Prediction Storage**: Results are stored in the database for analysis

### ML Integration Steps (Future)

1. Train your cancellation prediction model
2. Replace the mock prediction in `app/routes/bookings.py`
3. Add model loading and preprocessing logic
4. Update the prediction endpoint with your model

## Authentication

The system uses JWT tokens for authentication:

1. **Register/Login**: Get JWT token
2. **Authorization**: Include token in `Authorization: Bearer <token>` header
3. **Role-based Access**: Different permissions for clients and admins

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase anonymous key | Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | Yes |
| `DATABASE_URL` | Direct PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT secret key | Yes |
| `DEBUG` | Debug mode (True/False) | No |
| `HOST` | Server host | No |
| `PORT` | Server port | No |

## Development

### Adding New Endpoints

1. Create new route file in `app/routes/`
2. Define Pydantic models in `app/models.py`
3. Add route to `app/main.py`
4. Update this README

### Database Changes

1. Create migration SQL files
2. Update Pydantic models if needed
3. Test with existing data

## Testing

The API can be tested using:

1. **FastAPI Docs**: http://localhost:8000/docs
2. **Postman**: Import the API collection
3. **curl**: Command-line testing
4. **Python requests**: Programmatic testing

## Production Deployment

1. Set `DEBUG=False` in environment
2. Use production WSGI server (Gunicorn + Uvicorn)
3. Configure proper CORS origins
4. Set up SSL/TLS
5. Use environment variable management
6. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the database schema in `database_schema.sql`