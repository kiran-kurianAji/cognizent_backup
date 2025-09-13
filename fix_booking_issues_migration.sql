-- Migration script to fix booking calculation issues
-- Execute these statements in Supabase SQL Editor

-- Step 1: Change repeated_guest from BOOLEAN to INTEGER
-- First, add a new column with the correct type
ALTER TABLE bookings 
ADD COLUMN repeated_guest_new INTEGER;

-- Step 2: Update the new column based on existing data
-- For existing bookings, set repeated_guest_new based on user's booking history
UPDATE bookings 
SET repeated_guest_new = (
    SELECT COUNT(*) - 1  -- Subtract 1 because current booking is included in count
    FROM bookings b2 
    WHERE b2.user_id = bookings.user_id 
    AND b2.booking_id <= bookings.booking_id
);

-- Step 3: Drop the old column and rename the new one
ALTER TABLE bookings DROP COLUMN repeated_guest;
ALTER TABLE bookings RENAME COLUMN repeated_guest_new TO repeated_guest;

-- Step 4: Add NOT NULL constraint and check constraint
ALTER TABLE bookings 
ALTER COLUMN repeated_guest SET NOT NULL;

ALTER TABLE bookings 
ADD CONSTRAINT check_repeated_guest_non_negative 
CHECK (repeated_guest >= 0);

-- Step 5: Add comment explaining the field
COMMENT ON COLUMN bookings.repeated_guest IS 'Number of previous bookings made by this user (0 for first-time guests)';

-- Step 6: Modify history table to allow NULL booking_id for signup entries
ALTER TABLE history 
ALTER COLUMN booking_id DROP NOT NULL;

-- Step 7: Add comment explaining the history table usage
COMMENT ON TABLE history IS 'Tracks user activity including signups (booking_id=NULL) and cancellations (booking_id=booking_id)';
COMMENT ON COLUMN history.booking_id IS 'NULL for signup entries, booking_id for cancellation entries';

-- Step 8: Verify the changes
SELECT 
    booking_id, 
    user_id, 
    repeated_guest,
    booking_time
FROM bookings 
ORDER BY user_id, booking_time;
