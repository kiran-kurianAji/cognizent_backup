import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RoleSelection from './components/RoleSelection';
import ClientOptions from './components/ClientOptions';
import ClientSignup from './components/ClientSignup';
import ClientLogin from './components/ClientLogin';
import AdminLogin from './components/AdminLogin';
import ClientDashboard from './components/ClientDashboard';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-100">
        <Routes>
          <Route path="/" element={<RoleSelection />} />
          <Route path="/client-options" element={<ClientOptions />} />
          <Route path="/client-signup" element={<ClientSignup />} />
          <Route path="/client-login" element={<ClientLogin />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route path="/client-dashboard" element={<ClientDashboard />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
