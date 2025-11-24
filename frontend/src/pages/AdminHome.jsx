// frontend/src/pages/AdminHome.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import './AdminHome.css';   // 記得引入 CSS

const AdminHome = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/admin/users`);
      setUsers(response.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching users:", err);
      setError("Failed to load user data. Please make sure the Flask backend is running on port 5000.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="admin-page"><div className="loading">Loading...</div></div>;
  if (error) return (
    <div className="admin-page">
      <div className="error-box">Error: {error}</div>
    </div>
  );

  return (
    <div className="admin-page">
      <div className="admin-card">
        <h2 className="admin-title">Admin Dashboard - User List</h2>
        <p className="admin-subtitle">
          Total users: <span className="highlight">{users.length}</span>
        </p>

        <div className="table-wrapper">
          <table className="table custom-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Address</th>
                <th>Driver</th>
                <th>Participating</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>{user.address}</td>
                  <td>{user.is_driver ? '✅' : '❌'}</td>
                  <td>{user.is_participating ? '✅' : '❌'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminHome;
