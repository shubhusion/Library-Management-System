<template>
  <nav class="navbar">
    <div class="logo-container">
      <h1 class="logo">ReadersGate</h1>
    </div>
    <div class="nav-links">
      <router-link :to="homeLink" class="nav-link">Home</router-link>
      <router-link to="/account" class="nav-link" :class="{ 'active': $route.path === '/account' }">Account</router-link>
      <router-link to="/userlogin" class="nav-link">Logout</router-link>
    </div>
  </nav>

  <div class="page-content">
    <h2 class="section-heading">Account Details</h2>
    <div v-if="loading" class="loading-message">Loading user data...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-else class="account-details">
      <p v-if="username"><strong>Username: </strong>{{ username }}</p>
      <p v-if="email"><strong>Email: </strong>{{ email }}</p>
      <p v-if="role_id"><strong>Role: </strong>{{ role_id }}</p>
      <p v-else class="no-data">No user data available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserAccount',
  data() {
    return {
      username: '',
      email: '',
      role_id: '',
      loading: true,
      errorMessage: '',
    };
  },
  computed: {
    homeLink() {
      // Check if user role is librarian
      if (this.role_id === 'librarian') {
        return '/adminHomePage';
      } else {
        return '/userhome';
      }
    }
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const Token = localStorage.getItem('access_token');
        const response = await fetch('http://127.0.0.1:5000/api/whoami', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${Token}`,
          },
        });
        console.log(response);
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`${response.status}: ${errorData.message || 'Failed to fetch user data'}`);
        }
        const data = await response.json();
        console.log('Response data:', data);
        this.username = data.username;
        this.email = data.email;
        this.role_id = data.role_id;
      } catch (error) {
        console.error('Error fetching user data:', error);
        this.errorMessage = error.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* General Styles */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

body {
  font-family: 'Poppins', sans-serif;
  background-color: #f5f5f5;
}

/* Navbar Styles */
.navbar {
  background: linear-gradient(90deg, #007bff, #0056b3);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: white;
  font-weight: 500;
  font-size: 16px;
  margin: 0 12px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.active {
  background-color: rgba(255, 255, 255, 0.3);
}

/* Content Area Styles */
.page-content {
  padding: 32px;
  text-align: center;
}

.section-heading {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #0056b3;
}

.loading-message,
.error-message,
.no-data {
  font-size: 16px;
  font-weight: 500;
}

.loading-message {
  color: #007bff;
}

.error-message {
  color: #ff4d4d;
}

.no-data {
  color: #999;
}

.account-details {
  background-color: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.account-details p {
  font-size: 16px;
  margin: 8px 0;
}

.account-details p strong {
  color: #0056b3;
  font-weight: 600;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 16px;
  }

  .logo-container {
    margin-bottom: 16px;
  }

  .nav-links {
    margin-top: 16px;
  }

  .nav-link {
    margin: 8px;
  }

  .page-content {
    padding: 16px;
  }
}
</style>