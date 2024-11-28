import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider } from './contexts/AuthContext';

// Authentication Components
import Login from './components/Authentication/Login';
import Register from './components/Authentication/Register';

// Space Management Components
import SpaceList from './components/Spaces/SpaceList';
import SpaceForm from './components/Spaces/SpaceForm';

// Booking Components
import BookingDashboard from './components/Bookings/BookingDashboard';
import BookingForm from './components/Bookings/BookingForm';
import BookingCalendar from './components/Bookings/BookingCalendar';

// Admin Components
import AdminDashboard from './components/Admin/AdminDashboard';
import BookingApprovals from './components/Admin/BookingApprovals';

// Notification Components
import NotificationCenter from './components/Notifications/NotificationCenter';

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <LanguageProvider>
          <Router>
            <div className="app">
              <nav>
                {/* Navigation Menu */}
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/book-space">Book Space</Link>
                <Link to="/admin">Admin Panel</Link>
                <NotificationCenter />
              </nav>

              <Switch>
                <Route path="/login" component={Login} />
                <Route path="/register" component={Register} />
                <Route path="/dashboard" component={BookingDashboard} />
                <Route path="/book-space" component={BookingForm} />
                <Route path="/spaces" component={SpaceList} />
                <Route path="/admin" component={AdminDashboard}>
                  <Route path="approvals" component={BookingApprovals} />
                  <Route path="spaces" component={SpaceForm} />
                </Route>
              </Switch>
            </div>
          </Router>
        </LanguageProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
