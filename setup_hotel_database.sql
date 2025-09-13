-- Complete Database Setup for Hotel Booking System
-- Execute these scripts in Supabase SQL Editor in the following order

-- ===========================================
-- STEP 1: Execute the main database_schema.sql first
-- ===========================================

-- ===========================================
-- STEP 2: Execute this file to add hotel support
-- ===========================================

-- Create hotels table
CREATE TABLE hotels (
    hotel_id SERIAL PRIMARY KEY,
    hotel_name TEXT NOT NULL,
    admin_user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    contact_person TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    website TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add hotel_id to rooms table
ALTER TABLE rooms ADD COLUMN hotel_id INTEGER REFERENCES hotels(hotel_id) ON DELETE CASCADE;

-- Add hotel_id to bookings table  
ALTER TABLE bookings ADD COLUMN hotel_id INTEGER REFERENCES hotels(hotel_id) ON DELETE CASCADE;

-- Create indexes
CREATE INDEX idx_hotels_admin_user_id ON hotels(admin_user_id);
CREATE INDEX idx_hotels_email ON hotels(email);
CREATE INDEX idx_hotels_city ON hotels(city);
CREATE INDEX idx_hotels_is_active ON hotels(is_active);
CREATE INDEX idx_rooms_hotel_id ON rooms(hotel_id);
CREATE INDEX idx_bookings_hotel_id ON bookings(hotel_id);

-- Add constraints
ALTER TABLE hotels ADD CONSTRAINT check_hotel_name_length CHECK (char_length(hotel_name) >= 1 AND char_length(hotel_name) <= 200);
ALTER TABLE hotels ADD CONSTRAINT check_contact_person_length CHECK (char_length(contact_person) >= 1 AND char_length(contact_person) <= 100);
ALTER TABLE hotels ADD CONSTRAINT check_phone_length CHECK (char_length(phone) >= 10 AND char_length(phone) <= 15);
ALTER TABLE hotels ADD CONSTRAINT check_city_length CHECK (char_length(city) >= 1 AND char_length(city) <= 100);

-- Add comments
COMMENT ON TABLE hotels IS 'Stores hotel information and links to admin users';
COMMENT ON COLUMN hotels.admin_user_id IS 'References the admin user who manages this hotel';
COMMENT ON COLUMN hotels.is_active IS 'Whether the hotel is currently active in the system';
COMMENT ON COLUMN rooms.hotel_id IS 'Which hotel this room belongs to';
COMMENT ON COLUMN bookings.hotel_id IS 'Which hotel this booking is for';

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_hotels_updated_at 
    BEFORE UPDATE ON hotels 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
