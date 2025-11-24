// frontend/src/pages/AdminHome.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import './AdminHome.css';

const AdminHome = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // For inline editing
  const [editingUserId, setEditingUserId] = useState(null);
  const [editForm, setEditForm] = useState({
    name: '',
    email: '',
    address: '',
    is_driver: false,
    is_participating: false,
  });

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
      console.error('Error fetching users:', err);
      setError(
        'Failed to load user data. Please make sure the Flask backend is running on port 5000.'
      );
    } finally {
      setLoading(false);
    }
  };

  // When clicking "Edit", switch the row into edit mode
  const handleEditClick = (user) => {
    setEditingUserId(user.id);
    setEditForm({
      name: user.name || '',
      email: user.email || '',
      address: user.address || '',
      is_driver: user.is_driver,
      is_participating: user.is_participating,
    });
  };

  // When clicking "Cancel", exit edit mode
  const handleCancelEdit = () => {
    setEditingUserId(null);
    setEditForm({
      name: '',
      email: '',
      address: '',
      is_driver: false,
      is_participating: false,
    });
  };

  // Update local edit form state
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setEditForm((prev) => ({
      ...prev,
      [name]: checked,
    }));
  };

  // Save edited data to backend
  const handleSave = async (userId) => {
    try {
      const payload = {
        name: editForm.name,
        email: editForm.email,
        address: editForm.address,
        is_driver: editForm.is_driver,
        is_participating: editForm.is_participating,
      };

      await axios.put(`${API_BASE_URL}/admin/users/${userId}`, payload);

      // Option 1: refetch from backend to keep data consistent
      await fetchUsers();

      // Exit edit mode
      setEditingUserId(null);
    } catch (err) {
      console.error('Error updating user:', err);
      setError('Failed to update user. Please try again.');
    }
  };

  // Render logic
  if (loading)
    return (
      <div className="admin-page">
        <div className="loading">Loading...</div>
      </div>
    );

  if (error)
    return (
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
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => {
                const isEditing = editingUserId === user.id;

                return (
                  <tr key={user.id}>
                    <td>{user.id}</td>

                    {/* Name */}
                    <td>
                      {isEditing ? (
                        <input
                          type="text"
                          name="name"
                          value={editForm.name}
                          onChange={handleInputChange}
                          className="edit-input"
                        />
                      ) : (
                        user.name
                      )}
                    </td>

                    {/* Email */}
                    <td>
                      {isEditing ? (
                        <input
                          type="email"
                          name="email"
                          value={editForm.email}
                          onChange={handleInputChange}
                          className="edit-input"
                        />
                      ) : (
                        user.email
                      )}
                    </td>

                    {/* Address */}
                    <td>
                      {isEditing ? (
                        <input
                          type="text"
                          name="address"
                          value={editForm.address}
                          onChange={handleInputChange}
                          className="edit-input"
                        />
                      ) : (
                        user.address
                      )}
                    </td>

                    {/* Driver */}
                    <td style={{ textAlign: 'center' }}>
                      {isEditing ? (
                        <input
                          type="checkbox"
                          name="is_driver"
                          checked={editForm.is_driver}
                          onChange={handleCheckboxChange}
                        />
                      ) : user.is_driver ? (
                        '✅'
                      ) : (
                        '❌'
                      )}
                    </td>

                    {/* Participating */}
                    <td style={{ textAlign: 'center' }}>
                      {isEditing ? (
                        <input
                          type="checkbox"
                          name="is_participating"
                          checked={editForm.is_participating}
                          onChange={handleCheckboxChange}
                        />
                      ) : user.is_participating ? (
                        '✅'
                      ) : (
                        '❌'
                      )}
                    </td>

                    {/* Actions */}
                    <td>
                      {isEditing ? (
                        <>
                          <button
                            className="btn btn-sm btn-primary me-2"
                            onClick={() => handleSave(user.id)}
                          >
                            Save
                          </button>
                          <button
                            className="btn btn-sm btn-secondary"
                            onClick={handleCancelEdit}
                          >
                            Cancel
                          </button>
                        </>
                      ) : (
                        <button
                          className="btn btn-sm btn-outline-light"
                          onClick={() => handleEditClick(user)}
                        >
                          Edit
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminHome;
