<template>
  <div class="container">
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
    </nav>
    <div class="edit-book-container">
      <div class="login-card">
        <h1 class="login-title">Edit Book</h1>
        <div class="login-form">
          <label for="bookName" class="edit-label">Book Name:</label>
          <input type="text" id="bookName" v-model="bookName" required class="input-field">

          <label for="path" class="edit-label">Path:</label>
          <input type="text" id="path" v-model="path" required class="input-field">

          <label for="author" class="edit-label">Author:</label>
          <input type="text" id="author" v-model="author" required class="input-field">

          <label for="sectionId" class="edit-label">Section ID:</label>
          <input type="number" id="sectionId" v-model="sectionId" required class="input-field">

          <button type="submit" @click="updateBook" class="login-button">
            Update Book
          </button>
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
      bookName: '',
      path: '',
      author: '',
      sectionId: 0,
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem('access_token');
    },
  },
  mounted() {
    // Fetch book details when the component is mounted
    this.fetchBookDetails();
  },
  methods: {
    fetchBookDetails() {
      const bookId = this.$route.params.book_id;
      const apiUrl = `http://127.0.0.1:5000/api/books/${bookId}`;

      axios.get(apiUrl, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          const bookDetails = response.data;
          this.bookName = bookDetails.book_name;
          this.path = bookDetails.path;
          this.author = bookDetails.author;
          this.sectionId = bookDetails.section_id;
        })
        .catch((error) => {
          console.error('Error fetching book details:', error);
        });
    },
    updateBook() {
      const bookId = this.$route.params.book_id;
      const apiUrl = `http://127.0.0.1:5000/api/books/${bookId}`;

      const requestData = {
        book_name: this.bookName,
        path: this.path,
        author: this.author,
        section_id: this.sectionId,
      };

      console.log('Request data:', requestData);
      axios
        .put(apiUrl, requestData, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          console.log('Book updated successfully:', response.data);
          alert('Book Updated!');
          this.$router.push('/adminHomePage');
        })
        .catch((error) => {
          console.error('Error updating book:', error);
        });
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-image: url('https://source.unsplash.com/random/1920x1080/?books,library');
  background-size: cover;
  background-position: center;
}

.navbar {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: rgba(0, 123, 255, 0.8);
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.logo-container:hover {
  background-color: rgba(0, 123, 255, 0.9);
}

.logo-image {
  height: 40px;
  margin-right: 10px;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.edit-book-container {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
}

.login-card {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  max-width: 400px;
  width: 100%;
  backdrop-filter: blur(10px);
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-field {
  width: 100%;
  height: 40px;
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 4px rgba(0, 123, 255, 0.3), 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 1);
}

.login-button {
  width: 100%;
  height: 40px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.error-message {
  color: red;
  font-size: 14px;
}
</style>
