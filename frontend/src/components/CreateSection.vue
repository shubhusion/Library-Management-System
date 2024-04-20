<template>
  <div class="container">
    <div class="venue-form-container">
      <h2 class="form-title">Create New Section</h2>
      <form @submit.prevent="submitVenue" class="venue-form">
        <div class="form-group">
          <label for="sectionName" class="form-label">Section Name:</label>
          <input
            type="text"
            id="sectionName"
            v-model="sectionData.section_name"
            class="form-input"
            placeholder="Enter section name"
            required
          />
        </div>
        <div class="form-group">
          <label for="description" class="form-label">Description:</label>
          <textarea
            id="description"
            v-model="sectionData.description"
            class="form-input"
            placeholder="Enter description"
            rows="3"
            required
          ></textarea>
        </div>
        <button type="submit" class="submit-button">
          <span class="button-text">Submit</span>
          <span class="button-icon">
            <i class="fas fa-paper-plane"></i>
          </span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "SectionForm",
  data() {
    return {
      sectionData: {
        section_name: "",
        description: "",
      },
    };
  },
  computed: {
    accessToken() {
      return localStorage.getItem("access_token");
    },
  },
  methods: {
    async submitVenue() {
      if (!this.sectionData.section_name.trim() || !this.sectionData.description.trim()) {
        alert("Please fill out all fields.");
        return;
      }
      
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/sections", this.sectionData, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.accessToken}`,
          },
        });
        console.log("Section created:", response.data);
        alert("Section Created!");
        this.$router.push("/adminHomePage");
      } catch (error) {
        console.error("Error creating section:", error);
        // Log the error message to the console
        console.error("API Error Message:", error.message);
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f8f8;
}

.venue-form-container {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.form-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 28px;
  color: #333;
}

.venue-form {
  display: grid;
  gap: 20px;
}

.form-group {
  display: grid;
  gap: 8px;
}

.form-label {
  font-weight: bold;
  color: #555;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  color: #333;
  background-color: #fff;
  transition: border-color 0.3s ease;
  box-sizing: border-box; /* Added line */
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
}

.form-input::placeholder {
  color: #aaa;
}

.submit-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}

.button-text {
  margin-right: 8px;
}

.button-icon {
  font-size: 14px;
}
</style>
