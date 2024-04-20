<template>
  <div class="app">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
      <div class="nav-links">
        <div class="search-container">
          <input v-model="searchQuery" type="text" placeholder="Search sections or books" class="search-input" />
          <select v-model="searchCriteria" class="search-criteria">
            <option value="section">Section</option>
            <option value="author">Author</option>
            <option value="book">Book</option>
          </select>
          <button @click="searchItems" class="search-button"><i class="fas fa-search"></i></button>
        </div>
        <router-link to="/account" class="nav-link"><i class="fas fa-user"></i> Account</router-link>
        <router-link :to="'/userbooking/' + getUserId()" class="nav-link"><i class="fas fa-book"></i> My Books</router-link>
        <router-link to="/userlogin" class="nav-link logout-link"><i class="fas fa-sign-out-alt"></i> Logout</router-link>
      </div>
    </nav>

    <!-- Section and Books Display -->
    <div class="container">
      <div v-if="searchResults.length > 0" class="search-results-container">
        <h2>Search Results</h2>
        <div v-if="searchResults.some(result => result.books && result.books.length > 0)" class="section-container">
          <div v-for="result in searchResults" :key="result.id" class="section">
            <div class="section-header">
              <h3>{{ result.section_name || result.book_name }}</h3>
            </div>
            <div v-if="result.books" class="book-container">
              <table class="book-table">
                <thead>
                  <tr>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(book, bIndex) in result.books" :key="book.book_id" :class="{ 'book-last': bIndex === result.books.length - 1 }">
                    <td>{{ book.book_name }}</td>
                    <td>{{ book.author }}</td>
                    <td>
                      <button v-if="!book.isRequested" @click="requestAccess(book.book_id, result.id, bIndex)" class="action-button">
                        <i class="fas fa-file"></i> Request Access
                      </button>
                      <span v-else>Book Already Requested</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div v-else class="no-results">No books found</div>
      </div>
      <div v-else class="section-container">
        <div v-for="(section, index) in sections" :key="section.id" class="section" :class="{ 'section-last': index === sections.length - 1 }">
          <div class="section-header">
            <h3><i class="fas fa-folder"></i> {{ section.section_name }}</h3>
          </div>
          <div class="book-container">
            <table class="book-table">
              <thead>
                <tr>
                  <th>Book Name</th>
                  <th>Author</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(book, bIndex) in section.books" :key="book.book_id" :class="{ 'book-last': bIndex === section.books.length - 1 }">
                  <td>{{ book.book_name }}</td>
                  <td>{{ book.author }}</td>
                  <td>
                    <button v-if="!book.isRequested" @click="requestAccess(book.book_id, section.id, bIndex)" class="action-button">
                      <i class="fas fa-file"></i> Request Access
                    </button>
                    <span v-else>Book Already Requested</span>
                  </td>
                </tr>
              </tbody>
            </table>
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
      sections: [],
      searchQuery: '',
      searchCriteria: 'section',
      searchResults: [],
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem('access_token');
    },
  },
  mounted() {
    this.fetchSections();
  },
  methods: {
    getUserId() {
      return localStorage.getItem('user_id');
    },
    getUserRequestLimit() {
      return 5;
    },
    fetchSections() {
      axios.get('http://127.0.0.1:5000/api/sections', {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
        },
      })
        .then(response => {
          this.sections = response.data;
          this.sections.forEach(section => {
            this.fetchBooksForSection(section.id);
          });
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    fetchBooksForSection(section_id) {
      axios.get(`http://127.0.0.1:5000/api/sections/${section_id}/books`, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
        },
      })
        .then(response => {
          const section = this.sections.find(s => s.id === section_id);
          if (section) {
            const userId = this.getUserId();
            const requestCountKey = `request_count_${userId}`;
            const requestedBookIds = JSON.parse(localStorage.getItem(requestCountKey) || '[]');

            section.books = response.data.map(book => ({
              ...book,
              isRequested: requestedBookIds.includes(book.book_id),
            }));
          }
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    requestAccess(book_id, section_id, bookIndex) {
      if (this.hasReachedRequestLimit()) {
        alert('You have reached the maximum limit for book request accesses.');
        return;
      }

      axios.post(`http://127.0.0.1:5000/api/request/make/${book_id}`, null, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
        },
      })
        .then(response => {
          console.log(response.status);
          console.log(response.data);
          console.log('Access requested for book with ID:', book_id);
          this.incrementRequestCount(book_id);
          this.sections.find(section => section.id === section_id).books[bookIndex].isRequested = true;
        })
        .catch(error => {
          console.error('Error requesting access for book:', error);
          if (error.response && error.response.data) {
            alert(`Error: ${error.response.data.message}`);
          } else {
            alert('An error occurred while requesting access to the book.');
          }
        });
    },
    hasReachedRequestLimit() {
      return this.getRequestCount().length >= this.getUserRequestLimit();
    },
    getRequestCount() {
      const userId = this.getUserId();
      const requestCountKey = `request_count_${userId}`;
      return JSON.parse(localStorage.getItem(requestCountKey) || '[]');
    },
    incrementRequestCount(book_id) {
      const userId = this.getUserId();
      const requestCountKey = `request_count_${userId}`;
      const requestedBookIds = this.getRequestCount();
      requestedBookIds.push(book_id);
      localStorage.setItem(requestCountKey, JSON.stringify(requestedBookIds));
    },
    searchItems() {
      const searchQuery = this.searchQuery.trim().toLowerCase();
      if (!searchQuery) {
        this.searchResults = [];
        return;
      }

      this.searchResults = [];

      this.sections.forEach(section => {
        let matches = [];
        if (this.searchCriteria === 'section') {
          if (section.section_name.toLowerCase().includes(searchQuery)) {
            matches.push(section);
          }
        } else if (this.searchCriteria === 'author') {
          const authorMatches = section.books.filter(book => book.author.toLowerCase().includes(searchQuery));
          if (authorMatches.length > 0) {
            matches.push({
              ...section,
              books: authorMatches,
            });
          }
        } else if (this.searchCriteria === 'book') {
          const bookMatches = section.books.filter(book => book.book_name.toLowerCase().includes(searchQuery));
          if (bookMatches.length > 0) {
            matches.push({
              ...section,
              books: bookMatches,
            });
          }
        }

        if (matches.length > 0) {
          this.searchResults.push(...matches);
        }
      });

      if (this.searchResults.length === 0) {
        this.searchResults.push({
          id: 'no-results',
          section_name: 'No books found',
          books: [],
        });
      }
    },
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

/* Search container styles */
.search-container {
  display: flex;
  align-items: center;
  margin-left: 20px;
  margin-right: 20px; /* Add margin to the right */
}

.search-input {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
}

.search-criteria {
  margin-left: 8px;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
}

.search-button {
  background-color: #fff;
  color: #007bff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  margin-left: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

/* Container styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Section styles */
.section-container {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.section {
  margin-bottom: 20px;
}

.section-last {
  margin-bottom: 0;
}

.section h3 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.section .section-header h3 {
  margin: 0;
}

.section .section-actions .action-button {
  margin-left: 10px;
}

/* Book styles */
.book-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9f9f9;
}

.book-table th,
.book-table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.book-table th {
  background-color: #007bff;
  color: white;
  font-weight: bold;
  text-align: left;
}

.book-table td {
  background-color: #fff;
}

.book-last {
  margin-bottom: 0;
}

/* Action button styles */
.action-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

/* Create button styles */
.create-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 16px;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

.create-button:hover {
  background-color: #0056b3;
}
</style>