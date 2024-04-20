<template>
  <div class="app">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
      <div class="nav-links">
        <router-link to="/dashboard" class="nav-link"><i class="fas fa-chart-line"></i> Dashboard</router-link>
        <router-link to="/managebooks" class="nav-link"><i class="fas fa-book"></i> Manage Books Request </router-link>
        <router-link to="/account" class="nav-link"><i class="fas fa-user"></i> Account</router-link>
        <router-link to="/userlogin" class="nav-link logout-link"><i class="fas fa-sign-out-alt"></i> Logout</router-link>
      </div>
    </nav>

    <!-- Book Requests Section -->
    <div class="container">
      <div class="section-container">
        <h2>Book Requests</h2>
        <table class="book-request-table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Book ID</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in bookRequests" :key="request.id">
              <td>{{ request.user_id }}</td>
              <td>{{ request.book_id }}</td>
              <td>{{ request.status }}</td>
              <td>
                <button @click="acceptRequest(request.id)" class="action-button accept-button">
                  <i class="fas fa-check"></i> Accept
                </button>
                <button @click="denyRequest(request.id)" class="action-button deny-button">
                  <i class="fas fa-times"></i> Deny
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      bookRequests: [],
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem('access_token');
    },
  },
  mounted() {
    this.fetchBookRequests();
  },
  methods: {
    fetchBookRequests() {
      axios.get('http://127.0.0.1:5000/api/request', {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
        },
      })
        .then(response => {
          this.bookRequests = response.data;
        })
        .catch(error => {
          console.error('Error fetching book requests:', error);
        });
    },
    acceptRequest(requestId) {
      console.log('Accepting request with ID:', requestId);
      axios.post(`http://127.0.0.1:5000/api/request/approve/${requestId}`, {}, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
        },
      })
        .then(response => {
          // Handle success, maybe show a message or update UI
          console.log(response.status)
          console.log('Request accepted successfully');
          // Optionally, you can also update the local state to reflect the change immediately
          const index = this.bookRequests.findIndex(request => request.id === requestId);
          if (index !== -1) {
            this.bookRequests[index].status = 'approved';
          }
        })
        .catch(error => {
          console.error('Error accepting book request:', error);
        });
    },
    denyRequest(requestId) {
      console.log('Denying request with ID:', requestId);
      axios.post(`http://127.0.0.1:5000/api/request/deny/${requestId}`, {}, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
        },
      })
        .then(response => {
          // Handle success, maybe show a message or update UI
          console.log(response.status);
          console.log('Request denied successfully');
          // Optionally, you can also update the local state to reflect the change immediately
          const index = this.bookRequests.findIndex(request => request.id === requestId);
          if (index !== -1) {
            this.bookRequests[index].status = 'denied';
          }
        })
        .catch(error => {
          console.error('Error denying book request:', error);
        });
    },
  },
};
</script>


<style scoped>
/* Navbar styles */
.navbar {
  background-color: #007bff;
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
}

.logo-image {
  height: 40px;
  margin-right: 10px;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.nav-link i {
  margin-right: 5px;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.logout-link {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Book Request table styles */
.book-request-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9f9f9;
}

.book-request-table th,
.book-request-table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.book-request-table th {
  background-color: #007bff;
  color: white;
  font-weight: bold;
  text-align: left;
}

.book-request-table td {
  background-color: #fff;
}

/* Accept and deny button styles */
.accept-button, .deny-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.accept-button:hover, .deny-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.accept-button {
  color: #28a745; /* Green color for accept button */
}

.deny-button {
  color: #dc3545; /* Red color for deny button */
}
</style>
