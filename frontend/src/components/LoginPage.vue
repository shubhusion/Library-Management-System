<template>
  <div class="container">
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
    </nav>
    <div class="login-container">
      <div class="login-card">
        <h1 class="login-title">Login</h1>
        <div class="login-form">
          <input
            type="text"
            v-model="username"
            placeholder="Username"
            class="input-field"
          />
          <span class="error-message">{{ usernameError }}</span>
          <input
            type="password"
            v-model="password"
            placeholder="Password"
            class="input-field"
          />
          <span class="error-message">{{ passwordError }}</span>
          <button @click="login" class="login-button">
            <i class="fas fa-sign-in-alt"></i> Login
          </button>
          <p class="signup-text">
            New user?
            <router-link to="/signup" class="signup-link">Sign up</router-link>
          </p>
          <span class="error-message">{{ errorMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      usernameError: '',
      passwordError: '',
    };
  },
  methods: {
    login() {
      this.errorMessage = '';
      this.usernameError = '';
      this.passwordError = '';

      if (!this.username.trim()) {
        this.usernameError = 'Username is required';
      }
      if (!this.password.trim()) {
        this.passwordError = 'Password is required';
      }

      if (this.usernameError || this.passwordError) {
        return;
      }

      const data = {
        username: this.username,
        password: this.password,
      };

      axios.post('http://127.0.0.1:5000/api/login', data)
        .then(response => {
          if (response.status === 200) {
            return response.data;
          } else {
            console.log(response)
            throw new Error('Login error');
          }
        })
        .then(data => {
          console.log(data);
          if (data.tokens && data.tokens.access) {
            localStorage.setItem('access_token', data.tokens.access);
            localStorage.setItem('username', this.username);
            localStorage.setItem("user_id",this.id)

            axios.get('http://127.0.0.1:5000/api/whoami', {
              headers: {
                Authorization: `Bearer ${data.tokens.access}`,
              },
            })
              .then(response => {
                if (response.status === 200) {
                  return response.data;
                } else {
                  throw new Error('Failed to fetch user info');
                }
              })
              .then(userInfo => {
                console.log(userInfo);
                localStorage.setItem("user_id",userInfo.id)
                if (userInfo.role_id === 'librarian') {
                  this.$router.push('/adminHomePage');
                } else {
                  this.$router.push('/userhome');
                }
              })
              .catch(error => {
                console.error('Failed to fetch user info:', error);
                this.errorMessage = 'Failed to fetch user info';
              });
          } else {
            console.error('Access token not found in response');
            this.errorMessage = 'Access token not found';
          }
        })
        .catch(error => {
          console.error('Login error:', error);
          this.errorMessage = 'Login failed. Please try again.';
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

.login-container {
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

.login-button i {
  margin-right: 10px;
}

.signup-text {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.signup-link {
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.3s ease;
}

.signup-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.error-message {
  color: red;
  font-size: 14px;
}
</style>
