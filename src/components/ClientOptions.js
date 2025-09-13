import React from 'react';
import { useNavigate } from 'react-router-dom';

const ClientOptions = () => {
  const navigate = useNavigate();

  const handleOptionSelect = (option) => {
    if (option === 'signup') {
      navigate('/client-signup');
    } else if (option === 'login') {
      navigate('/client-login');
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
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
            Back to Role Selection
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Client Portal
          </h1>
          <p className="text-gray-600">
            Choose an option to continue
          </p>
        </div>

        {/* Options */}
        <div className="space-y-4 animate-slide-up">
          <button
            onClick={() => handleOptionSelect('signup')}
            className="w-full btn-primary text-lg py-4"
          >
            <div className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
              Sign Up
            </div>
          </button>

          <button
            onClick={() => handleOptionSelect('login')}
            className="w-full btn-secondary text-lg py-4"
          >
            <div className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              Login
            </div>
          </button>
        </div>

        {/* Info */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg animate-fade-in">
          <div className="flex items-start">
            <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h4 className="text-sm font-medium text-blue-900">New to our platform?</h4>
              <p className="text-sm text-blue-700 mt-1">
                Sign up to create your account and start booking rooms.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClientOptions;
