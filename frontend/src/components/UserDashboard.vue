<template>
  <div class="app">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo-container">
        <img src="@/assets/open-book.png" alt="ReadersGate Logo" class="logo-image" />
        <h1 class="logo">ReadersGate</h1>
      </div>
      <div class="nav-links">
        <router-link to="/dashboard" class="nav-link"><i class="fas fa-chart-line"></i> Dashboard</router-link>
        <router-link to="/managebooks" class="nav-link"><i class="fas fa-book"></i> Manage Books Request </router-link>
        <router-link to="/account" class="nav-link"><i class="fas fa-user"></i> Account</router-link>
        <router-link to="/userlogin" class="nav-link logout-link"><i class="fas fa-sign-out-alt"></i> Logout</router-link>
      </div>
    </nav>

    <!-- Your existing component content -->
    <div class="chart-wrapper">
      <div class="chart-container">
        <canvas ref="sectionDistributionChart"></canvas>
      </div>
      <div class="chart-container">
        <canvas ref="statusChart" width="400" height="300"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart } from 'chart.js/auto';

export default {
  data() {
    return {
      sectionDistributionData: [],
      chart: null
    };
  },
  mounted() {
    // Fetch data when component is mounted
    this.fetchSectionDistribution();
    this.fetchStatusCounts();
  },
  methods: {
    fetchSectionDistribution() {
      // Fetch data from the API
      axios.get('http://127.0.0.1:5000/api/analytics/section-distribution')
        .then(response => {
          // Update data
          this.sectionDistributionData = response.data;
          // Render chart with updated data
          this.renderSectionDistributionChart();
        })
        .catch(error => {
          console.error('Error fetching section distribution data:', error);
        });
    },
    renderSectionDistributionChart() {
      // Extract labels and data from the fetched data
      const labels = this.sectionDistributionData.map(item => item.section_name);
      const data = this.sectionDistributionData.map(item => item.book_count);
      // Get canvas context
      const ctx = this.$refs.sectionDistributionChart.getContext('2d');
      // Destroy previous chart instance if exists
      if (this.chart) {
        this.chart.destroy();
      }
      // Create new chart instance
      this.chart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'Book Distribution by Section',
            data: data,
            backgroundColor: [
              'rgba(255, 99, 132, 0.7)',
              'rgba(54, 162, 235, 0.7)',
              'rgba(255, 206, 86, 0.7)',
              'rgba(75, 192, 192, 0.7)',
              'rgba(153, 102, 255, 0.7)',
              'rgba(255, 159, 64, 0.7)' // Add more colors if needed
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Book Distribution by Section',
              font: {
                size: 18
              }
            }
          }
        }
      });
      // Log success message to console
      console.log('Chart rendered successfully!');
    },
    fetchStatusCounts() {
      axios.get('http://127.0.0.1:5000/api/book_requests/status_counts')
        .then(response => {
          const data = response.data;
          this.renderStatusChart(data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    renderStatusChart(data) {
      const ctx = this.$refs.statusChart.getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Issued', 'Denied', 'Pending'],
          datasets: [{
            label: 'Book Request Status',
            data: [data.issued_count, data.denied_count, data.pending_count],
            backgroundColor: [
              'rgba(54, 162, 235, 0.7)', // Issued
              'rgba(255, 99, 132, 0.7)', // Denied
              'rgba(255, 206, 86, 0.7)',  // Pending
            ]
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          },
          plugins: {
            title: {
              display: true,
              text: 'Book Request Status',
              font: {
                size: 18
              }
            },
            legend: {
              display: true,
              position: 'bottom'
            }
          }
        }
      });
    }
  }
}
</script>

<style scoped>
.app {
  font-family: 'Arial', sans-serif;
}

/* Navbar */
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

/* Chart styles */
.chart-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align items at the top */
  height: 100vh;
}

.chart-container {
  width: 45%; /* Adjust width to leave space between charts */
  max-width: 400px; /* Adjust maximum width */
  margin: 10px; /* Add margin between charts */
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  padding: 20px;
  height: 400px; /* Set a fixed height */
}

.canvas-container {
  width: 100%;
  height: 100%; /* Ensure canvas takes full height */
}

.chart-heading {
  font-size: 20px;
  margin-bottom: 10px;
  text-align: center;
}
</style>
