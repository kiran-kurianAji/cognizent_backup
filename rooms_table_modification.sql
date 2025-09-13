-- Modify rooms table to add room_code for ML prediction mapping
-- Execute these statements in Supabase SQL Editor

-- Step 1: Add the room_code column to the rooms table
ALTER TABLE rooms 
ADD COLUMN room_code TEXT;

-- Step 2: Add a comment explaining the purpose of room_code
COMMENT ON COLUMN rooms.room_code IS 'ML prediction code mapping - must match expected input format for cancellation prediction model';

-- Step 3: Update existing rows with the room type to room code mapping
-- Update Standard Room to room_type_1
UPDATE rooms 
SET room_code = 'room_type_1' 
WHERE room_type = 'Standard Room';

-- Update Deluxe Room to room_type_2
UPDATE rooms 
SET room_code = 'room_type_2' 
WHERE room_type = 'Deluxe Room';

-- Update Suite to room_type_3
UPDATE rooms 
SET room_code = 'room_type_3' 
WHERE room_type = 'Suite';

-- Update Presidential to room_type_4
UPDATE rooms 
SET room_code = 'room_type_4' 
WHERE room_type = 'Presidential';

-- Step 4: Add a constraint to ensure room_code follows the expected format
ALTER TABLE rooms 
ADD CONSTRAINT check_room_code_format 
CHECK (room_code ~ '^room_type_[1-9][0-9]*$');

-- Step 5: Make room_code NOT NULL after updating existing data
ALTER TABLE rooms 
ALTER COLUMN room_code SET NOT NULL;

-- Step 6: Add a unique constraint to ensure each room_code is unique
ALTER TABLE rooms 
ADD CONSTRAINT unique_room_code UNIQUE (room_code);

-- Step 7: Create an index on room_code for better query performance
CREATE INDEX idx_rooms_room_code ON rooms(room_code);

-- Step 8: Insert sample room data if the table is empty (optional)
-- Uncomment the following lines if you need to create sample data
/*
INSERT INTO rooms (room_type, room_code, total_rooms, available_rooms, price) VALUES
('Standard Room', 'room_type_1', 50, 45, 100.00),
('Deluxe Room', 'room_type_2', 30, 28, 150.00),
('Suite', 'room_type_3', 15, 12, 250.00),
('Presidential', 'room_type_4', 5, 4, 500.00);
*/

-- Step 9: Verify the changes
-- Run this query to check the updated room data
SELECT room_id, room_type, room_code, total_rooms, available_rooms, price 
FROM rooms 
ORDER BY room_id;
