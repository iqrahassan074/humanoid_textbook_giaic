import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Redirect } from 'react-router-dom';


const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login, isAuthenticated, error, clearError } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    clearError();

    try {
      const result = await login(email, password);
      if (!result.success) {
        // Error is handled by the auth context
      }
    } catch (err) {
      console.error('Login error:', err);
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
              <h1>Login</h1>

              {error && (
                <div className="alert alert--danger" style={{ marginBottom: '1rem' }}>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="email" className="form-label">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    className="form-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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
                    className="form-input"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={isLoading}
                  />
                </div>

                <button
                  type="submit"
                  className="form-button"
                  disabled={isLoading}
                >
                  {isLoading ? 'Logging in...' : 'Login'}
                </button>
              </form>

              <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                <p>
                  Don't have an account? <a href="/register">Register here</a>
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

export default LoginPage;


