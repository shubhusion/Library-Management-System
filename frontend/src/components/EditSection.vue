<template>
  <div class="container">
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
    </nav>
    <div class="edit-section-container">
      <div class="edit-section-card">
        <h2 class="edit-section-title">Edit Section</h2>
        <form @submit.prevent="updateSection" class="edit-section-form">
          <div class="form-group">
            <label for="edit-section-name">Section Name:</label>
            <input v-model="editedSection.section_name" @blur="validateField('section_name')" type="text" id="edit-section-name" required class="input-field">
            <span v-if="touched.section_name && !editedSection.section_name" class="error-message">Section name is required.</span>
          </div>
          <div class="form-group">
            <label for="edit-section-location">Description:</label>
            <input v-model="editedSection.description" @blur="validateField('description')" type="text" id="edit-section-location" required class="input-field">
            <span v-if="touched.description && !editedSection.description" class="error-message">Description is required.</span>
          </div>
          <button type="submit" @click.prevent="updateSection" class="btn btn-primary">Save Changes</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditSection',
  data() {
    return {
      editedSection: {
        section_id: null,
        section_name: '',
        description: '',
      },
      touched: {
        section_name: false,
        description: false
      }
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem('access_token');
    },
  },
  mounted() {
    this.editedSection.section_id = this.$route.params.section_id;
    this.fetchSectionDetails();
  },
  methods: {
    fetchSectionDetails() {
      const url = `http://127.0.0.1:5000/api/sections/${this.editedSection.section_id}`;
      axios.get(url, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        })
        .then(response => {
          this.editedSection = response.data;
        })
        .catch(error => {
          console.error('Error fetching section details:', error);
        });
    },
    updateSection() {

      const sectionId = this.$route.params.section_id;
      console.log(sectionId)

      if (!this.editedSection.section_name || !this.editedSection.description) {
        alert("Please fill in all required fields.");
        return;
      }

      const url = `http://127.0.0.1:5000/api/sections/${sectionId}`;
      axios.put(url, this.editedSection, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.accessToken}`
          }
        })
        .then(response => {
          if (response.status === 200) {
            alert("Section updated!");
            this.$router.push('/adminHomePage');
          } else {
            console.error('Error updating section');
          }
        })
        .catch(error => {
          console.error('Error updating section:', error);
        });
    },
    validateField(fieldName) {
      this.touched[fieldName] = true;
    }
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

.edit-section-container {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
}

.edit-section-card {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  max-width: 400px;
  width: 100%;
  backdrop-filter: blur(10px);
}

.edit-section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.edit-section-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
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

.btn-primary {
  width: 100%;
  height: 40px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.error-message {
  color: red;
  font-size: 14px;
  display: none;
}

.error-message.active {
  display: block;
}
</style>
