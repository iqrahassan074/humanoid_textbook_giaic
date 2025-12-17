import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Redirect } from 'react-router-dom';


const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const { register, isAuthenticated, error, clearError } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    clearError();

    try {
      const result = await register(formData);
      if (!result.success) {
        // Error is handled by the auth context
      }
    } catch (err) {
      console.error('Registration error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Redirect if already authenticated
  if (isAuthenticated) {
    return <Redirect to="/chapters" replace />;
  }

  return (
    <div className="login-container">
      <div className="textbook-container">
        <div className="container">
          <div className="row">
            <div className="col col--12 col--8-desktop col--offset-2-desktop">
              <h1>Create Account</h1>

              {error && (
                <div className="alert alert--danger" style={{ marginBottom: '1rem' }}>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="first_name" className="form-label">
                    First Name
                  </label>
                  <input
                    type="text"
                    id="first_name"
                    name="first_name"
                    className="form-input"
                    value={formData.first_name}
                    onChange={handleChange}
                    required
                    disabled={isLoading}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="last_name" className="form-label">
                    Last Name
                  </label>
                  <input
                    type="text"
                    id="last_name"
                    name="last_name"
                    className="form-input"
                    value={formData.last_name}
                    onChange={handleChange}
                    required
                    disabled={isLoading}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email" className="form-label">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="form-input"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    disabled={isLoading}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="password" className="form-label">
                    Password
                  </label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    className="form-input"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    disabled={isLoading}
                    minLength="6"
                  />
                  <small className="help-text">
                    Password must be at least 6 characters long
                  </small>
                </div>

                <button
                  type="submit"
                  className="form-button"
                  disabled={isLoading}
                >
                  {isLoading ? 'Creating Account...' : 'Register'}
                </button>
              </form>

              <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                <p>
                  Already have an account? <a href="/login">Login here</a>
                </p>
                <p>
                  <a href="/">Back to Home</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;