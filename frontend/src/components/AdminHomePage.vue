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
            <option value="all">All</option>
            <option value="section">Section</option>
            <option value="author">Author</option>
            <option value="book">Book</option>
          </select>
          <button @click="searchItems" class="search-button"><i class="fas fa-search"></i></button>
        </div>
        <router-link to="/dashboard" class="nav-link"><i class="fas fa-chart-line"></i> Dashboard</router-link>
        <router-link to="/managebooks" class="nav-link"><i class="fas fa-book"></i> Manage Books Request </router-link>
        <router-link to="/account" class="nav-link"><i class="fas fa-user"></i> Account</router-link>
        <router-link to="/userlogin" class="nav-link logout-link"><i class="fas fa-sign-out-alt"></i>
          Logout</router-link>
      </div>
    </nav>

    <!-- Section CRUD -->
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
                    <th>Book Id</th>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in result.books" :key="book.book_id">
                    <td>{{ book.book_id }}</td>
                    <td>{{ book.book_name }}</td>
                    <td>{{ book.author }}</td>
                    <td>
                      <div class="action-buttons">
                        <!-- View Book Button -->
                        <button @click="viewBook(book.book_id)" class="action-button view-button">
                          <i class="fas fa-eye"></i> View
                        </button>
                        <!-- Delete Book Button -->
                        <button @click="deleteBook(book.book_id)" class="action-button delete-button">
                          <i class="fas fa-trash-alt"></i> Delete
                        </button>
                        <!-- Edit Book Button -->
                        <button @click="editBook(book.book_id)" class="action-button edit-button">
                          <i class="fas fa-edit"></i> Edit
                        </button>
                      </div>
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
        <div v-for="section in sections" :key="section.id" class="section">
          <div class="section-header">
            <h3>{{ section.section_name }}</h3>
            <div class="section-actions">
              <!-- Edit Section Button -->
              <button @click="editSection(section.id)" class="action-button edit-button">
                <i class="fas fa-edit"></i> Edit
              </button>
              <!-- Delete Section Button -->
              <button @click="deleteSection(section.id)" class="action-button delete-button">
                <i class="fas fa-trash-alt"></i> Delete
              </button>
            </div>
          </div>
          <div class="book-container">
            <table class="book-table">
              <thead>
                <tr>
                  <th>Book Id</th>
                  <th>Book Name</th>
                  <th>Author</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in section.books" :key="book.book_id">
                  <td>{{ book.book_id }}</td>
                  <td>{{ book.book_name }}</td>
                  <td>{{ book.author }}</td>
                  <td>
                    <div class="action-buttons">
                      <!-- View Book Button -->
                      <button @click="viewBook(book.book_id)" class="action-button view-button">
                        <i class="fas fa-eye"></i> View
                      </button>
                      <!-- Delete Book Button -->
                      <button @click="deleteBook(book.book_id)" class="action-button delete-button">
                        <i class="fas fa-trash-alt"></i> Delete
                      </button>
                      <!-- Edit Book Button -->
                      <button @click="editBook(book.book_id)" class="action-button edit-button">
                        <i class="fas fa-edit"></i> Edit
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <br>
            <!-- Add Book Button -->
            <button @click="goToBookForm(section.id)" class="create-button">
              <i class="fas fa-plus-circle"></i> Add Book
            </button>
          </div>
        </div>
      </div>
      <br>
      <div class="section-actions">
        <!-- Add Section Button -->
        <button @click="goToSectionForm" class="create-button">
          <i class="fas fa-plus-circle"></i> Add Section
        </button>
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
      searchResults: [],
      searchCriteria: 'all'
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
            section.books = response.data;
          }
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    deleteSection(section_id) {
      if (confirm("Are you sure you want to delete this section?")) {
        axios.delete(`http://127.0.0.1:5000/api/sections/${section_id}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
          },
        })
          .then(response => {
            if (response.status === 200) {
              this.sections = this.sections.filter(section => section.id !== section_id);
              console.log('Section Deleted Successfully', 200);
            } else {
              console.error('Error deleting section');
            }
          })
          .catch(error => {
            console.error('Error deleting section:', error);
          });
      }
    },
    editSection(section_id) {
      this.$router.push(`/editsection/${section_id}`);
    },
    deleteBook(book_id) {
      if (confirm("Are you sure you want to delete this book?")) {
        axios.delete(`http://127.0.0.1:5000/api/books/${book_id}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
          },
        })
          .then(response => {
            if (response.status === 200) {
              this.sections.forEach(section => {
                section.books = section.books.filter(book => book.book_id !== book_id);
              });
              console.log('Book Deleted Successfully', 200);
            } else {
              console.error('Error deleting book');
            }
          })
          .catch(error => {
            console.error('Error deleting book:', error);
          });
      }
    },
    editBook(book_id) {
      this.$router.push(`/editbook/${book_id}`);
    },
    goToBookForm(section_id) {
      this.$router.push(`/createbook/${section_id}`);
    },
    goToSectionForm() {
      this.$router.push('/sectionform');
    },
    viewBook(book_id) {
      const book = this.findBookById(book_id);
      if (book && book.path) {
        const bookPath = book.path.startsWith('http') ? book.path : `http://${book.path}`;
        window.open(bookPath, '_blank');
      } else {
        console.error('Book path not found.');
      }
    },
    findBookById(book_id) {
      for (const section of this.sections) {
        const foundBook = section.books.find(book => book.book_id === book_id);
        if (foundBook) {
          return foundBook;
        }
      }
      return null;
    },
    searchItems() {
      const searchQuery = this.searchQuery.trim().toLowerCase();
      const criteria = this.searchCriteria;

      if (!searchQuery) {
        // If the search query is empty, reset the searchResults and display all sections
        this.searchResults = [];
        return;
      }

      this.searchResults = [];

      // Iterate over each section
      this.sections.forEach(section => {
        let matches = [];

        if (criteria === 'all' || criteria === 'section') {
          const sectionMatch = section.section_name.toLowerCase().includes(searchQuery);
          if (sectionMatch) matches.push(section);
        }

        if (criteria === 'all' || criteria === 'book') {
          const bookMatches = section.books.filter(book => {
            const bookNameMatch = book.book_name.toLowerCase().includes(searchQuery);
            const authorMatch = book.author.toLowerCase().includes(searchQuery);
            return bookNameMatch || authorMatch;
          });

          if (bookMatches.length > 0) {
            matches.push({
              ...section,
              books: bookMatches
            });
          }
        }

        if (criteria === 'all' || criteria === 'author') {
          const authorMatches = section.books.filter(book => book.author.toLowerCase().includes(searchQuery));
          if (authorMatches.length > 0) {
            matches.push({
              ...section,
              books: authorMatches
            });
          }
        }

        if (matches.length > 0) {
          this.searchResults.push(...matches);
        }
      });

      // If there are no search results, display the "No books found" message
      if (this.searchResults.length === 0) {
        this.searchResults.push({
          id: 'no-results',
          section_name: 'No books found',
          books: []
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
  margin-right: 20px;
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


/* Search container styles */
.search-container {
  display: flex;
  align-items: center;
  margin-left: 20px;
  margin-right: 20px;
}

.search-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  flex: 1;
  margin-right: 15px;
}

.search-criteria {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
  background-color: #fff;
}

.search-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  margin-left: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #0056b3;
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
