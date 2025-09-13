-- Hotel Booking Cancellation Prediction System Database Schema
-- Execute these scripts in Supabase SQL Editor in the following order

-- Step 1: Create ENUM types
CREATE TYPE user_role AS ENUM ('client', 'admin');
CREATE TYPE booking_status AS ENUM ('confirmed', 'canceled');

-- Step 2: Create users table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    role user_role NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    phone TEXT,
    city TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add constraint to ensure user_id starts with 'C' or 'A'
ALTER TABLE users ADD CONSTRAINT check_user_id_format 
CHECK (user_id ~ '^[CA][A-Za-z0-9]+$');

-- Step 3: Create rooms table
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_type TEXT NOT NULL,
    total_rooms INTEGER NOT NULL CHECK (total_rooms > 0),
    available_rooms INTEGER NOT NULL CHECK (available_rooms >= 0 AND available_rooms <= total_rooms),
    price DECIMAL(10,2) NOT NULL CHECK (price > 0)
);

-- Step 4: Create bookings table
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    room_id INTEGER NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
    lead_time INTEGER NOT NULL CHECK (lead_time >= 0),
    market_segment_type TEXT NOT NULL,
    no_of_children INTEGER NOT NULL CHECK (no_of_children >= 0),
    no_of_adults INTEGER NOT NULL CHECK (no_of_adults > 0),
    arrival_date DATE NOT NULL,
    arrival_month INTEGER NOT NULL CHECK (arrival_month >= 1 AND arrival_month <= 12),
    no_of_previous_cancellations INTEGER NOT NULL CHECK (no_of_previous_cancellations >= 0),
    room_type_reserved TEXT NOT NULL,
    no_of_week_nights INTEGER NOT NULL CHECK (no_of_week_nights >= 0),
    no_of_weekend_nights INTEGER NOT NULL CHECK (no_of_weekend_nights >= 0),
    repeated_guest BOOLEAN NOT NULL,
    type_of_meal_plan INTEGER NOT NULL CHECK (type_of_meal_plan >= 0),
    no_of_special_requests INTEGER NOT NULL CHECK (no_of_special_requests >= 0),
    avg_price_per_room DECIMAL(10,2) NOT NULL CHECK (avg_price_per_room > 0),
    booking_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    cancellation_prediction DECIMAL(3,2) CHECK (cancellation_prediction >= 0 AND cancellation_prediction <= 1),
    status booking_status DEFAULT 'confirmed'
);

-- Step 5: Create history table
CREATE TABLE history (
    history_id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    cancellation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Step 6: Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_room_id ON bookings(room_id);
CREATE INDEX idx_bookings_arrival_date ON bookings(arrival_date);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_history_user_id ON history(user_id);
CREATE INDEX idx_history_booking_id ON history(booking_id);

-- Step 7: Add comments for documentation
COMMENT ON TABLE users IS 'Stores both clients and admins with user_id starting with C for clients and A for admins';
COMMENT ON TABLE rooms IS 'Stores different types of rooms with availability and pricing';
COMMENT ON TABLE bookings IS 'Stores booking details with cancellation prediction data';
COMMENT ON TABLE history IS 'Stores cancellation history for tracking purposes';

COMMENT ON COLUMN users.user_id IS 'Primary key starting with C for clients, A for admins';
COMMENT ON COLUMN bookings.cancellation_prediction IS 'ML prediction score between 0 and 1';
COMMENT ON COLUMN bookings.lead_time IS 'Days between booking and arrival';
COMMENT ON COLUMN bookings.arrival_month IS 'Month of arrival (1-12)';
