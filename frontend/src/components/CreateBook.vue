<template>
  <div class="container">
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
    </nav>
    <div class="form-container">
      <div class="form-card">
        <h2 class="form-title">Create New Book</h2>
        <form @submit.prevent="createBook" class="book-form">
          <div class="form-group">
            <label for="bookName">Book Name:</label>
            <input type="text" id="bookName" v-model="newBookData.book_name" class="input-field" />
            <span class="error-message" v-if="bookNameError">{{ bookNameError }}</span>
          </div>
          <div class="form-group">
            <label for="author">Author:</label>
            <input type="text" id="author" v-model="newBookData.author" class="input-field" />
            <span class="error-message" v-if="authorError">{{ authorError }}</span>
          </div>
          <div class="form-group">
            <label for="path">Book Path:</label>
            <input type="text" id="path" v-model="newBookData.path" class="input-field" />
            <span class="error-message" v-if="pathError">{{ pathError }}</span>
          </div>
          <button type="submit" class="btn-create-book">
            Create Book
          </button>
          <span class="error-message" v-if="errorMessage">{{ errorMessage }}</span>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "CreateBook",
  data() {
    return {
      newBookData: {
        book_name: "",
        author: "",
        path: "",
        section_id: null,
      },
      errorMessage: "",
      bookNameError: "",
      authorError: "",
      pathError: "",
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem("access_token");
    },
  },
  mounted() {
    this.newBookData.section_id = this.$route.params.book_id;
  },
  methods: {
    createBook() {
      this.resetErrors();

      if (!this.newBookData.book_name.trim()) {
        this.bookNameError = "Book Name is required";
      }
      if (!this.newBookData.author.trim()) {
        this.authorError = "Author is required";
      }
      if (!this.newBookData.path.trim()) {
        this.pathError = "Book Path is required";
      }

      if (this.hasErrors()) {
        return;
      }

      const bookData = {
        book_name: this.newBookData.book_name,
        author: this.newBookData.author,
        path: this.newBookData.path,
        section_id: this.newBookData.section_id,
      };
      axios
        .post("http://127.0.0.1:5000/api/books", bookData, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          if (response.status === 201) {
            alert('Book created successfully!');
            this.$router.push('/adminHomePage');
          } else {
            console.error("Failed to create book");
          }
        })
        .catch((error) => {
          console.error("Error creating book:", error.response);
          this.errorMessage = "Error creating book";
        });
    },
    resetErrors() {
      this.errorMessage = "";
      this.bookNameError = "";
      this.authorError = "";
      this.pathError = "";
    },
    hasErrors() {
      return (
        this.bookNameError ||
        this.authorError ||
        this.pathError
      );
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.navbar {
  background-color: #007bff;
  padding: 10px;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-image {
  height: 40px;
  margin-right: 10px;
}

.logo {
  font-size: 24px;
  color: #fff;
}

.form-container {
  margin-top: 40px; /* Increase margin top for more space */
}

.form-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 30px; /* Increase padding for more space */
  width: 400px; /* Set a fixed width */
}

.form-title {
  font-size: 24px; /* Increase font size for title */
  font-weight: bold;
  margin-bottom: 30px; /* Increase margin bottom for spacing */
}

.form-group {
  margin-bottom: 20px; /* Increase margin bottom for spacing */
}

.label {
  font-weight: bold;
}

.input-field {
  width: calc(100% - 20px); /* Reduce input field width */
  height: 30px; /* Reduce input field height */
  padding: 5px; /* Reduce padding for input fields */
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-create-book {
  width: 100%;
  height: 40px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-create-book:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  font-size: 14px;
}
</style>
