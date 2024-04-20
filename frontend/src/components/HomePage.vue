<template>
  <div class="Home">
    <div class="header">
      <h1>Welcome to ReadersGate!</h1>
      <p>Empowering Librarians, Enriching Readers</p>
    </div>
    <div class="buttons">
      <router-link to="/userlogin">
        <button class="login-button">Login</button>
      </router-link>
      <router-link to="/signup">
        <button class="signup-button">Signup</button>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
/* General Styles */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
}

/* Navbar Styles */
.navbar {
  background-color: darkcyan;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-family: 'Montserrat', sans-serif;
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  color: #fff;
}

/* Home Styles */
.Home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  background: linear-gradient(135deg, #007bff, #6c757d);
  color: #fff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header h1 {
  font-family: 'Montserrat', sans-serif;
  font-size: 36px;
  margin-bottom: 20px;
}

.header p {
  font-size: 20px;
  margin-bottom: 30px;
}

/* Button Styles */
.buttons {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.login-button,
.signup-button {
  padding: 12px 24px;
  font-size: 18px;
  background-color: #fff;
  color: #007bff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.login-button:hover,
.signup-button:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
