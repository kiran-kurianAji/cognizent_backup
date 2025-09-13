# Hotel Booking System - Frontend

A modern, professional React frontend for the Hotel Booking Cancellation Prediction System.

## 🎯 **Features**

### **Role-Based Authentication Flow**
- **Role Selection**: Choose between Client or Admin
- **Client Path**: Sign Up or Login options
- **Admin Path**: Direct login with Admin ID + Password
- **Smooth Navigation**: Intuitive flow between screens

### **Client Features**
- **Simplified Signup**: Only 6 essential fields
- **Easy Login**: User ID + Password
- **Client Dashboard**: Book rooms, view reservations, manage profile
- **Form Validation**: Real-time validation with error messages

### **Admin Features**
- **Admin Login**: Admin ID + Password authentication
- **Admin Dashboard**: Manage rooms, bookings, and ML predictions
- **Statistics Overview**: Room count, bookings, cancellations, revenue
- **Management Tools**: Room management, booking monitoring

## 🎨 **Design System**

### **Color Scheme**
- **Primary**: Blue (#3b82f6) - Professional and trustworthy
- **Background**: Light gray gradient - Clean and modern
- **Cards**: White with subtle shadows - Clean separation

### **Animations**
- **Fade In**: Smooth page transitions
- **Slide Up**: Form animations
- **Hover Effects**: Subtle scale and shadow changes
- **Loading States**: Spinner animations for form submissions

### **Typography**
- **Headings**: Bold, clear hierarchy
- **Body Text**: Readable gray tones
- **Form Labels**: Medium weight for clarity

## 🛠 **Technical Stack**

- **React 18**: Modern functional components with hooks
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **Custom Components**: Reusable, modular design

## 📁 **Project Structure**

```
src/
├── components/
│   ├── RoleSelection.js      # Initial role selection screen
│   ├── ClientOptions.js      # Client signup/login options
│   ├── ClientSignup.js       # Client registration form
│   ├── ClientLogin.js        # Client login form
│   ├── AdminLogin.js         # Admin login form
│   ├── ClientDashboard.js    # Client dashboard
│   └── AdminDashboard.js     # Admin dashboard
├── App.js                    # Main app with routing
├── index.js                  # React entry point
└── index.css                 # Global styles and Tailwind
```

## 🚀 **Getting Started**

### **Installation**
```bash
npm install
```

### **Development**
```bash
npm start
```

### **Build for Production**
```bash
npm run build
```

## 🔌 **Backend Integration**

### **API Endpoints Ready**
- **Authentication**: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/admin-login`
- **Rooms**: `/api/v1/rooms/` (CRUD operations)
- **Bookings**: `/api/v1/bookings/` (Create, read, update, cancel)
- **ML Predictions**: `/api/v1/bookings/predict-cancellation`

### **Integration Points**
- **Form Submissions**: Replace mock API calls with actual fetch requests
- **Authentication**: Store JWT tokens in localStorage
- **Error Handling**: Implement proper error handling for API responses
- **Loading States**: Connect loading states to actual API calls

## 📱 **User Experience**

### **Client Journey**
1. **Role Selection** → Choose "Client"
2. **Options** → Choose "Sign Up" or "Login"
3. **Form** → Fill out simple form (6 fields for signup, 2 for login)
4. **Dashboard** → Access booking features

### **Admin Journey**
1. **Role Selection** → Choose "Admin"
2. **Login** → Enter Admin ID + Password
3. **Dashboard** → Access management features

## ✅ **Form Validation**

### **Client Signup**
- **User ID**: Required
- **Full Name**: Required
- **Email**: Required, valid format
- **Password**: Required, minimum 8 characters
- **Phone**: Required
- **City**: Required

### **Login Forms**
- **User ID/Admin ID**: Required
- **Password**: Required

## 🎯 **Ready for Production**

- **Responsive Design**: Works on desktop and tablet
- **Professional Styling**: Corporate-ready appearance
- **Smooth Animations**: Subtle, elegant transitions
- **Form Validation**: Real-time error feedback
- **Loading States**: User feedback during operations
- **Error Handling**: Graceful error management

## 🔄 **Next Steps**

1. **Connect to Backend**: Replace mock API calls
2. **Add Real Data**: Connect to actual hotel data
3. **Implement Features**: Add room booking, management features
4. **Testing**: Add unit and integration tests
5. **Deployment**: Deploy to production environment

## 📞 **Support**

This frontend is designed to work seamlessly with the FastAPI backend. All API integration points are clearly marked with TODO comments for easy implementation.
