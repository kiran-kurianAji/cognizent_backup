-- Update Database for Single Hotel System
-- Execute this script in Supabase SQL Editor

-- Add hotel information columns to users table for admin users
ALTER TABLE users ADD COLUMN IF NOT EXISTS hotel_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS hotel_address TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS hotel_website TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS hotel_description TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS hotel_phone TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS hotel_contact_person TEXT;

-- Add constraints for hotel information
ALTER TABLE users ADD CONSTRAINT check_hotel_name_length 
    CHECK (hotel_name IS NULL OR (char_length(hotel_name) >= 1 AND char_length(hotel_name) <= 200));

ALTER TABLE users ADD CONSTRAINT check_hotel_contact_length 
    CHECK (hotel_contact_person IS NULL OR (char_length(hotel_contact_person) >= 1 AND char_length(hotel_contact_person) <= 100));

-- Add comments
COMMENT ON COLUMN users.hotel_name IS 'Hotel name (only for admin users)';
COMMENT ON COLUMN users.hotel_address IS 'Hotel address (only for admin users)';
COMMENT ON COLUMN users.hotel_website IS 'Hotel website (only for admin users)';
COMMENT ON COLUMN users.hotel_description IS 'Hotel description (only for admin users)';
COMMENT ON COLUMN users.hotel_phone IS 'Hotel phone (only for admin users)';
COMMENT ON COLUMN users.hotel_contact_person IS 'Hotel contact person (only for admin users)';
