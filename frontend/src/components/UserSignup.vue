<template>
  <div class="container">
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
    </nav>
    <div class="signup-container">
      <div class="signup-card">
        <h1 class="signup-title">Sign Up</h1>
        <div class="form">
          <input
            type="text"
            v-model="username"
            :class="{ 'input-field': true, 'is-invalid': !isUsernameValid }"
            placeholder="Username"
            @input="validateUsername"
          />
          <span v-if="!isUsernameValid" class="error-message">username must be 5 characters long</span>
          <input
            type="text"
            v-model="email"
            :class="{ 'input-field': true, 'is-invalid': !isEmailValid }"
            placeholder="Email"
            @input="validateEmail"
          />
          <span v-if="!isEmailValid" class="error-message">Please enter a valid email address</span>
          <input
            type="password"
            v-model="password"
            :class="{ 'input-field': true, 'is-invalid': !isPasswordValid }"
            placeholder="Password"
            @input="validatePassword"
          />
          <span v-if="!isPasswordValid" class="error-message">Password must be at least 8 characters long</span>
          <button @click="signup" class="signup-button">Sign Up</button>
          <p class="login-text">
            Existing user?
            <router-link to="/userlogin" class="login-link">Log In</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role_id: 'user',
      isUsernameValid: true,
      isEmailValid: true,
      isPasswordValid: true,
    };
  },
  methods: {
    signup() {
      if (this.isUsernameValid && this.isEmailValid && this.isPasswordValid) {
        const userData = {
          username: this.username,
          email: this.email,
          password: this.password,
          role_id: this.role_id,
        };

        axios.post('http://127.0.0.1:5000/api/register', userData)
          .then(response => {
            if (response.status !== 200) {
              throw new Error('Network response was not ok');
            }
            alert('Sign Up Successful');
            this.$router.push('/userlogin');
          })
          .catch(error => {
            console.error('Sign Up Error', error);
            alert(error);
          });
      } else {
        alert('Please fill in all fields correctly.');
      }
    },
    validateUsername() {
      this.isUsernameValid = this.username.length >= 5;
    },
    validateEmail() {
      this.isEmailValid = /\S+@\S+\.\S+/.test(this.email);
    },
    validatePassword() {
      this.isPasswordValid = this.password.length >= 8;
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

.signup-container {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
}

.signup-card {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  max-width: 400px;
  width: 100%;
  backdrop-filter: blur(10px);
}

.signup-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form {
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

.signup-button {
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

.signup-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.login-text {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.login-link {
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.is-invalid {
  border-color: #dc3545;
}

.error-message {
  color: #dc3545;
  font-size: 12px;
  margin-top: 4px;
}
</style>
