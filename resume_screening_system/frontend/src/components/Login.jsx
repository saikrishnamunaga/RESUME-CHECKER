import React, { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';

const API_BASE = '/api/v1/auth';

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        window.location.href = '/dashboard';
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const res = await fetch(`${API_BASE}/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: credentialResponse.credential }),
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        window.location.href = '/dashboard';
      } else {
        setError('Google login failed');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        
        <form onSubmit={handleEmailLogin} className="mb-6">
          <div className="mb-4">
            <input
              type="email"
              name="email"
              placeholder="your@gmail.com"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-3 border rounded-lg"
              required
            />
          </div>
          <div className="mb-6">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-3 border rounded-lg"
              required
            />
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600 mb-4">
            Login
          </button>
        </form>

        <div className="text-center">
          <p className="mb-4">Or continue with</p>
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => setError('Google login failed')}
          />
        </div>
        
        {error && <p className="mt-4 text-red-500 text-center">{error}</p>}
        <p className="mt-4 text-center">
          No account? <a href="/register" className="text-blue-500 font-semibold">Register</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
