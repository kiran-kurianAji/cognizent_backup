import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ClientSignup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    phone: '',
    city: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [generatedUserId, setGeneratedUserId] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required field validation
    if (!formData.fullName.trim()) newErrors.fullName = 'Full name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.password.trim()) newErrors.password = 'Password is required';
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
    if (!formData.city.trim()) newErrors.city = 'City is required';

    // Email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (formData.email && !emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password length validation
    if (formData.password && formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const signupPayload = {
        full_name: formData.fullName,
        email: formData.email,
        password: formData.password,
        phone: formData.phone,
        city: formData.city,
        role: 'client'
      };

      console.log('Signup payload:', signupPayload);

      const response = await fetch('http://localhost:8000/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(signupPayload)
      });

      console.log('Signup response status:', response.status);
      console.log('Signup response headers:', Object.fromEntries(response.headers.entries()));

      if (response.ok) {
        const data = await response.json();
        console.log('Signup success data:', data);
        
        // Store authentication token
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userRole', 'client');
        
        // Store generated user_id and show success message
        setGeneratedUserId(data.data.user_id);
        setShowSuccess(true);
        
        // Auto-redirect after 3 seconds
        setTimeout(() => {
          navigate('/client-dashboard');
        }, 3000);
      } else {
        const errorText = await response.text();
        console.error('Signup failed:', response.status, response.statusText, errorText);
        
        try {
          const errorData = JSON.parse(errorText);
          alert(errorData.detail || 'Signup failed. Please try again.');
        } catch (parseError) {
          alert(`Signup failed: ${response.status} ${response.statusText}`);
        }
      }
      
    } catch (error) {
      console.error('Signup error:', error);
      alert('Signup failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/client-options');
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <button
            onClick={handleBack}
            className="text-primary-600 hover:text-primary-700 mb-4 flex items-center justify-center mx-auto"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Options
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Create Account
          </h1>
          <p className="text-gray-600">
            Fill in your details to get started
          </p>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="card animate-slide-up bg-green-50 border border-green-200">
            <div className="text-center">
              <div className="text-green-600 text-6xl mb-4">✅</div>
              <h2 className="text-2xl font-bold text-green-800 mb-2">Account Created Successfully!</h2>
              <p className="text-green-700 mb-4">Your account has been created and you're now logged in.</p>
              
              <div className="bg-white rounded-lg p-4 mb-4 border border-green-300">
                <p className="text-sm text-gray-600 mb-2">Your generated User ID:</p>
                <p className="text-xl font-mono font-bold text-green-800 bg-green-100 px-4 py-2 rounded">
                  {generatedUserId}
                </p>
                <p className="text-xs text-gray-500 mt-2">
                  Save this User ID - you'll need it to log in next time
                </p>
              </div>
              
              <p className="text-sm text-gray-600">
                Redirecting to dashboard in 3 seconds...
              </p>
            </div>
          </div>
        )}

        {/* Form */}
        {!showSuccess && (
          <div className="card animate-slide-up">
            <form onSubmit={handleSubmit} className="space-y-6">

            {/* Full Name */}
            <div>
              <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                type="text"
                id="fullName"
                name="fullName"
                value={formData.fullName}
                onChange={handleInputChange}
                className={`input-field ${errors.fullName ? 'input-error' : ''}`}
                placeholder="Enter your full name"
              />
              {errors.fullName && <p className="mt-1 text-sm text-red-600">{errors.fullName}</p>}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className={`input-field ${errors.email ? 'input-error' : ''}`}
                placeholder="Enter your email"
              />
              {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password *
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className={`input-field ${errors.password ? 'input-error' : ''}`}
                placeholder="Enter your password"
              />
              {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password}</p>}
            </div>

            {/* Phone */}
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                Phone Number *
              </label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                className={`input-field ${errors.phone ? 'input-error' : ''}`}
                placeholder="Enter your phone number"
              />
              {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone}</p>}
            </div>

            {/* City */}
            <div>
              <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                className={`input-field ${errors.city ? 'input-error' : ''}`}
                placeholder="Enter your city"
              />
              {errors.city && <p className="mt-1 text-sm text-red-600">{errors.city}</p>}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating Account...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
            </form>

            {/* Login Link */}
            <div className="mt-6 text-center">
              <p className="text-gray-600">
                Already have an account?{' '}
                <button
                  onClick={() => navigate('/client-login')}
                  className="text-primary-600 hover:text-primary-700 font-medium"
                >
                  Sign in here
                </button>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientSignup;
