const API_BASE_URL = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {

  // 1. Handle Sign Up Form Submission
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const full_name = document.getElementById('signupName').value.trim();
      const email = document.getElementById('signupEmail').value.trim();
      const password = document.getElementById('signupPassword').value;
      const role = document.getElementById('signupRole').value;

      try {
        const res = await fetch(`${API_BASE_URL}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ full_name, email, password, role })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Registration failed');

        // Save active session tokens
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('user_name', data.full_name);

        alert('Account created successfully! Directing to dashboard...');

        // Route to matching role dashboard
        redirectToRoleDashboard(data.role);

      } catch (err) {
        alert(err.message || 'Server connection error');
      }
    });
  }

  // 2. Handle Login Form Submission
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('loginEmail').value.trim();
      const password = document.getElementById('loginPassword').value;

      try {
        const res = await fetch(`${API_BASE_URL}/token`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Incorrect email or password');

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('user_name', data.full_name);

        alert(`Welcome back, ${data.full_name}! Accessing dashboard...`);

        redirectToRoleDashboard(data.role);

      } catch (err) {
        alert(err.message || 'Server connection error');
      }
    });
  }
});

// Helper Function for Role Redirects
function redirectToRoleDashboard(role) {
  const userRole = (role || '').toUpperCase();
  if (userRole === 'TEACHER') window.location.href = 'teacher-dashboard.html';
  else if (userRole === 'PARENT') window.location.href = 'parent-dashboard.html';
  else if (userRole === 'ADMIN') window.location.href = 'admin-dashboard.html';
  else window.location.href = 'student-dashboard.html';
}