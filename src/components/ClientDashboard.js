import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ClientDashboard = () => {
  const navigate = useNavigate();
  const [rooms, setRooms] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [showBookingForm, setShowBookingForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userProfile, setUserProfile] = useState(null);

  // Helper function to get fresh token from localStorage
  const getAuthToken = () => {
    const freshToken = localStorage.getItem('token');
    if (!freshToken) {
      console.error('No token found in localStorage');
      navigate('/client-login');
      return null;
    }
    return freshToken;
  };

  // Helper function to handle authentication errors
  const handleAuthError = (error) => {
    console.error('Authentication error:', error);
    if (error.status === 401 || error.message?.includes('401')) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      alert('Your session has expired. Please log in again.');
      navigate('/client-login');
    }
  };

  // Booking form state
  const [bookingData, setBookingData] = useState({
    arrival_date: '',
    checkout_date: '',
    no_of_adults: 1,
    no_of_children: 0,
    type_of_meal_plan: 1,
    special_requests: ['']
  });

  // Room mapping for display
  const roomMapping = {
    'room_type_1': 'Deluxe Suite',
    'room_type_2': 'Standard Room',
    'room_type_3': 'Family Room',
    'room_type_4': 'Presidential Suite'
  };

  useEffect(() => {
    if (!token) {
      navigate('/client-login');
      return;
    }
    fetchUserProfile();
    fetchRooms();
    fetchBookings();
  }, [token, navigate]);

  const fetchUserProfile = async () => {
    try {
      const authToken = getAuthToken();
      if (!authToken) return;

      console.log('Fetching user profile with token:', authToken.substring(0, 20) + '...');
      
      const response = await fetch('http://localhost:8000/api/v1/auth/profile', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const profile = await response.json();
        setUserProfile(profile);
        console.log('User profile fetched successfully:', profile);
      } else if (response.status === 401) {
        console.error('Authentication failed - token expired or invalid');
        handleAuthError({ status: 401 });
      } else {
        console.error('Failed to fetch user profile:', response.status, response.statusText);
      }
    } catch (err) {
      console.error('Error fetching user profile:', err);
      handleAuthError(err);
    }
  };

  const fetchRooms = async () => {
    try {
      const authToken = getAuthToken();
      if (!authToken) return;

      console.log('Fetching rooms with token:', authToken.substring(0, 20) + '...');
      
      const response = await fetch('http://localhost:8000/api/v1/rooms/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setRooms(data);
        console.log('Rooms fetched successfully:', data.length, 'rooms');
      } else if (response.status === 401) {
        console.error('Authentication failed when fetching rooms');
        handleAuthError({ status: 401 });
      } else {
        console.error('Failed to fetch rooms:', response.status, response.statusText);
        setError('Failed to fetch rooms');
      }
    } catch (err) {
      console.error('Error fetching rooms:', err);
      setError('Error fetching rooms');
      handleAuthError(err);
    }
  };

  const fetchBookings = async () => {
    try {
      const authToken = getAuthToken();
      if (!authToken) return;

      console.log('Fetching bookings with token:', authToken.substring(0, 20) + '...');
      
      const response = await fetch('http://localhost:8000/api/v1/bookings/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setBookings(data);
        console.log('Bookings fetched successfully:', data.length, 'bookings');
      } else if (response.status === 401) {
        console.error('Authentication failed when fetching bookings');
        handleAuthError({ status: 401 });
      } else {
        console.error('Failed to fetch bookings:', response.status, response.statusText);
        setError('Failed to fetch bookings');
      }
    } catch (err) {
      console.error('Error fetching bookings:', err);
      setError('Error fetching bookings');
      handleAuthError(err);
    }
  };

  const handleRoomSelect = (room) => {
    setSelectedRoom(room);
    setShowBookingForm(true);
    setError('');
    setSuccess('');
  };

  const handleBookingSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Get fresh token before making the request
      const authToken = getAuthToken();
      if (!authToken) {
        setError('Authentication token not found. Please log in again.');
        setLoading(false);
        return;
      }

      console.log('Creating booking with token:', authToken.substring(0, 20) + '...');

      // Calculate week nights and weekend nights
      const arrivalDate = new Date(bookingData.arrival_date);
      const checkoutDate = new Date(bookingData.checkout_date);
      const totalNights = Math.ceil((checkoutDate - arrivalDate) / (1000 * 60 * 60 * 24));
      
      // Simple calculation: assume weekends are Saturday and Sunday
      let weekNights = 0;
      let weekendNights = 0;
      
      for (let i = 0; i < totalNights; i++) {
        const currentDate = new Date(arrivalDate);
        currentDate.setDate(arrivalDate.getDate() + i);
        const dayOfWeek = currentDate.getDay();
        
        if (dayOfWeek === 0 || dayOfWeek === 6) { // Sunday or Saturday
          weekendNights++;
        } else {
          weekNights++;
        }
      }

      const bookingPayload = {
        room_id: selectedRoom.room_id,
        arrival_date: bookingData.arrival_date,
        no_of_adults: bookingData.no_of_adults,
        no_of_children: bookingData.no_of_children,
        no_of_week_nights: weekNights,
        no_of_weekend_nights: weekendNights,
        type_of_meal_plan: bookingData.type_of_meal_plan,
        no_of_special_requests: bookingData.special_requests.filter(req => req.trim() !== '').length
      };

      console.log('Booking payload:', bookingPayload);

      const response = await fetch('http://localhost:8000/api/v1/bookings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(bookingPayload)
      });

      console.log('Booking response status:', response.status);
      console.log('Booking response headers:', Object.fromEntries(response.headers.entries()));

      if (response.ok) {
        const result = await response.json();
        console.log('Booking created successfully:', result);
        setSuccess('Booking created successfully!');
        setShowBookingForm(false);
        setSelectedRoom(null);
        setBookingData({
          arrival_date: '',
          checkout_date: '',
          no_of_adults: 1,
          no_of_children: 0,
          type_of_meal_plan: 1,
          special_requests: ['']
        });
        fetchBookings(); // Refresh bookings list
      } else if (response.status === 401) {
        console.error('Authentication failed when creating booking');
        setError('Your session has expired. Please log in again.');
        handleAuthError({ status: 401 });
      } else {
        const errorText = await response.text();
        console.error('Booking failed:', response.status, response.statusText, errorText);
        
        try {
          const errorData = JSON.parse(errorText);
          setError(errorData.detail || `Failed to create booking (${response.status})`);
        } catch (parseError) {
          setError(`Failed to create booking: ${response.status} ${response.statusText}`);
        }
      }
    } catch (err) {
      console.error('Error creating booking:', err);
      setError('Network error: Unable to create booking. Please check your connection.');
      handleAuthError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return;
    }

    try {
      const authToken = getAuthToken();
      if (!authToken) {
        setError('Authentication token not found. Please log in again.');
        return;
      }

      console.log('Cancelling booking with token:', authToken.substring(0, 20) + '...');

      const response = await fetch(`http://localhost:8000/api/v1/bookings/${bookingId}/cancel`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setSuccess('Booking cancelled successfully!');
        fetchBookings(); // Refresh bookings list
      } else if (response.status === 401) {
        console.error('Authentication failed when cancelling booking');
        setError('Your session has expired. Please log in again.');
        handleAuthError({ status: 401 });
      } else {
        console.error('Failed to cancel booking:', response.status, response.statusText);
        setError('Failed to cancel booking');
      }
    } catch (err) {
      console.error('Error cancelling booking:', err);
      setError('Error cancelling booking');
      handleAuthError(err);
    }
  };

  const addSpecialRequest = () => {
    setBookingData(prev => ({
      ...prev,
      special_requests: [...prev.special_requests, '']
    }));
  };

  const updateSpecialRequest = (index, value) => {
    setBookingData(prev => ({
      ...prev,
      special_requests: prev.special_requests.map((req, i) => 
        i === index ? value : req
      )
    }));
  };

  const removeSpecialRequest = (index) => {
    setBookingData(prev => ({
      ...prev,
      special_requests: prev.special_requests.filter((_, i) => i !== index)
    }));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Hotel Booking Dashboard</h1>
              {userProfile && (
                <div className="mt-1 text-sm text-gray-600">
                  <span className="font-medium">Welcome, {userProfile.full_name}!</span>
                  <span className="ml-2 text-gray-500">ID: {userProfile.user_id}</span>
                </div>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Success/Error Messages */}
        {success && (
          <div className="mb-6 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            {success}
          </div>
        )}
        {error && (
          <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Rooms Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Available Rooms</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {rooms.map((room) => (
              <div key={room.room_id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {roomMapping[room.room_code] || room.room_type}
                  </h3>
                  <p className="text-3xl font-bold text-blue-600 mb-2">
                    ${room.price}
                  </p>
                  <p className="text-sm text-gray-600 mb-4">
                    Available: {room.available_rooms} / {room.total_rooms}
                  </p>
                  <button
                    onClick={() => handleRoomSelect(room)}
                    disabled={room.available_rooms === 0}
                    className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
                      room.available_rooms === 0
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {room.available_rooms === 0 ? 'Sold Out' : 'Book Now'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Booking Form Modal */}
        {showBookingForm && selectedRoom && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-gray-900">
                  Book {roomMapping[selectedRoom.room_code] || selectedRoom.room_type}
                </h3>
                <button
                  onClick={() => setShowBookingForm(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleBookingSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Arrival Date
                    </label>
                    <input
                      type="date"
                      required
                      value={bookingData.arrival_date}
                      onChange={(e) => setBookingData(prev => ({ ...prev, arrival_date: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Checkout Date
                    </label>
                    <input
                      type="date"
                      required
                      value={bookingData.checkout_date}
                      onChange={(e) => setBookingData(prev => ({ ...prev, checkout_date: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Number of Adults
                    </label>
                    <input
                      type="number"
                      min="1"
                      required
                      value={bookingData.no_of_adults}
                      onChange={(e) => setBookingData(prev => ({ ...prev, no_of_adults: parseInt(e.target.value) }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Number of Children
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={bookingData.no_of_children}
                      onChange={(e) => setBookingData(prev => ({ ...prev, no_of_children: parseInt(e.target.value) }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Meal Plan
                  </label>
                  <select
                    value={bookingData.type_of_meal_plan}
                    onChange={(e) => setBookingData(prev => ({ ...prev, type_of_meal_plan: parseInt(e.target.value) }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value={1}>Veg</option>
                    <option value={2}>Non-veg</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Special Requests
                  </label>
                  {bookingData.special_requests.map((request, index) => (
                    <div key={index} className="flex gap-2 mb-2">
                      <input
                        type="text"
                        value={request}
                        onChange={(e) => updateSpecialRequest(index, e.target.value)}
                        placeholder="Enter special request"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      {bookingData.special_requests.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeSpecialRequest(index)}
                          className="px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                        >
                          Remove
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={addSpecialRequest}
                    className="mt-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                  >
                    Add Request
                  </button>
                </div>

                <div className="flex gap-4 pt-4">
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Creating Booking...' : 'Create Booking'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowBookingForm(false)}
                    className="flex-1 bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* My Bookings Section */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">My Bookings</h2>
          {bookings.length === 0 ? (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <p className="text-gray-600">No bookings found. Book a room to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {bookings.map((booking) => (
                <div key={booking.booking_id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <p className="text-sm font-medium text-gray-500">Booking ID</p>
                          <p className="text-lg font-semibold text-gray-900">#{booking.booking_id}</p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-500">Room Type</p>
                          <p className="text-lg font-semibold text-gray-900">
                            {roomMapping[booking.room_type_reserved] || booking.room_type_reserved}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-500">Status</p>
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            booking.status === 'confirmed' 
                              ? 'bg-green-100 text-green-800' 
                              : booking.status === 'cancelled'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {booking.status}
                          </span>
                        </div>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                        <div>
                          <p className="text-sm font-medium text-gray-500">Arrival Date</p>
                          <p className="text-gray-900">{new Date(booking.arrival_date).toLocaleDateString()}</p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-500">Total Price</p>
                          <p className="text-gray-900">${booking.avg_price_per_room}</p>
                        </div>
                      </div>
                    </div>
                    {booking.status === 'confirmed' && (
                      <button
                        onClick={() => handleCancelBooking(booking.booking_id)}
                        className="ml-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                      >
                        Cancel Booking
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClientDashboard;