import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RoleSelection = () => {
  const [selectedRole, setSelectedRole] = useState(null);
  const navigate = useNavigate();

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    
    // Add a small delay for animation
    setTimeout(() => {
      if (role === 'client') {
        navigate('/client-options');
      } else if (role === 'admin') {
        navigate('/admin-login');
      }
    }, 300);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-4xl w-full">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Hotel Booking System
          </h1>
          <p className="text-xl text-gray-600">
            Choose your role to continue
          </p>
        </div>

        {/* Role Selection Cards */}
        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          {/* Client Card */}
          <div
            className={`role-card ${selectedRole === 'client' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('client')}
          >
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-3">
                Client
              </h3>
              <p className="text-gray-600 mb-6">
                Book rooms and manage your reservations
              </p>
              <div className="text-primary-600 font-medium">
                Click to continue →
              </div>
            </div>
          </div>

          {/* Admin Card */}
          <div
            className={`role-card ${selectedRole === 'admin' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('admin')}
          >
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-3">
                Admin
              </h3>
              <p className="text-gray-600 mb-6">
                Manage hotel operations and bookings
              </p>
              <div className="text-primary-600 font-medium">
                Click to continue →
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 animate-fade-in">
          <p className="text-gray-500">
            Professional Hotel Management Platform
          </p>
        </div>
      </div>
    </div>
  );
};

export default RoleSelection;
