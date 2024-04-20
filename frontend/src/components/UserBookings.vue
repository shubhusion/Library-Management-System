<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
      <div class="nav-links">
        <router-link to="/userhome" class="nav-link"><i class="fas fa-home"></i> Home</router-link>
        <router-link to="/userbooking" class="nav-link active"><i class="fas fa-book"></i> My Books</router-link>
      </div>
    </nav>

    <!-- Bookings Display -->
    <div class="container">
      <div class="section-container">
        <h2>My Books</h2>
        <div>
          <table v-if="userBooks.length > 0" class="book-table">
            <thead>
              <tr>
                <th>Book ID</th>
                <th>Issued Date</th>
                <th>Expiry Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(userBook, index) in userBooks" :key="index">
                <td>{{ userBook.book_id }}</td>
                <td>{{ userBook.issued_date }}</td>
                <td>{{ userBook.expiry_date }}</td>
                <td>
                  <button @click="viewBook(userBook.book_id)" class="action-button view-button">
                    <i class="fas fa-eye"></i> View
                  </button>
                  <button @click="revokeAccess(userBook.book_id)" class="action-button revoke-button">
                    <i class="fas fa-ban"></i> Revoke Access
                  </button>
                  <button @click="provideFeedback(userBook.book_id)" class="action-button feedback-button">
                    <i class="fas fa-comment"></i> Provide Feedback
                  </button>
                  <button @click="downloadBook(userBook.book_id)" class="action-button download-button">
                    <i class="fas fa-download"></i> Download Book
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else>
            No Books...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      userBooks: [],
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem('access_token');
    },
    userId() {
      return localStorage.getItem('user_id');
    }
  },
  mounted() {
    this.fetchUserBooks();
  },
  methods: {
    async fetchUserBooks() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/users/${this.userId}/books`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        });
        this.userBooks = response.data;
      } catch (error) {
        console.error("Error fetching user books:", error);
      }
    },
    async viewBook(book_id) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/books/${book_id}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        });
        const book = response.data;
        if (book && book.path) {
          const bookPath = book.path.startsWith('http') ? book.path : `http://${book.path}`;
          window.open(bookPath, '_blank');
        } else {
          console.error('Book path not found.');
        }
      } catch (error) {
        console.error('Error fetching book details:', error.message);
      }
    },
    async revokeAccess(book_id) {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/users/${this.userId}/books/${book_id}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        });
        this.userBooks = this.userBooks.filter(book => book.book_id !== book_id);
      } catch (error) {
        console.error('Error revoking access to book:', error);
      }
    },
    provideFeedback(book_id) {
      const user_id = this.userId;
      this.$router.push(`/feedback/users/${user_id}/books/${book_id}/feedbacks`);
    },
    async downloadBook(book_id) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/books/${book_id}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        });
        const book = response.data;
        if (!book) {
          console.error('Book not found in userBooks data.');
          return;
        }
        // Display alert for payment
        const confirmPayment = confirm("This book requires payment. Do you want to proceed with the payment?");
        if (confirmPayment) {
          if (book.path && typeof book.path === 'string') {
            window.open(book.path, '_blank');
          } else {
            console.error('Invalid book path.');
          }
        } else {
          console.log('Payment canceled.');
        }
      } catch (error) {
        console.error('Error fetching book details:', error.message);
      }
    }
  },
};
</script>

<style scoped>
/* Global styles */
body {
  margin: 0;
  font-family: 'Roboto', sans-serif;
  background-color: #f5f5f5;
}

/* Navbar styles */
.navbar {
  background-color: #007bff;
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-image {
  width: 40px;
  margin-right: 10px;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin-right: 20px;
  font-size: 18px;
}

.nav-link.active {
  font-weight: bold;
}

/* Container styles */
.container {
  padding: 20px;
}

.section-container {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Table styles */
.book-table {
  width: 100%;
  border-collapse: collapse;
}

.book-table th,
.book-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.book-table th {
  background-color: #f2f2f2;
}

/* Button styles */
.action-button {
  border: none;
  padding: 8px 12px;
  margin-right: 5px;
  cursor: pointer;
  border-radius: 3px;
}

.view-button {
  background-color: #007bff;
  color: white;
}

.revoke-button {
  background-color: #dc3545;
  color: white;
}

.feedback-button {
  background-color: #28a745;
  color: white;
}

.download-button {
  background-color: #ffc107;
  color: white;
}

/* Responsive styles */
@media (max-width: 768px) {
  .nav-links {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-link {
    margin-right: 0;
    margin-bottom: 10px;
  }
}
</style>
