<template>
    <div class="p-4">
      <nav class="bg-light p-3 d-flex justify-content-between mb-4">
            <div>
                <router-link to="/admin/dashboard" class="me-3">Home</router-link>
                <router-link to="/admin/users" class="me-3">Users</router-link>
                <router-link to="/admin/summary" class="me-3">Summary</router-link>
                <router-link to="/" class="text-danger">Logout</router-link>
            </div>
            <button @click="$router.push('/admin/search')" class="btn btn-primary">Search</button>
        </nav>

        <div class="container mt-5">
        <div class="card shadow p-4">
        <h2 class="text-center text-primary">Subject-wise Top Scores</h2>

        <div class="chart-container" style="position: relative; block-size: 300px; inline-size: 100%;">
          <canvas id="topScoresChart"></canvas>
        </div>

        <div class="text-center mt-3">
          <router-link to="/admin/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
    data() {
        return {
            token: localStorage.getItem("token"),
            chart: null,
            subjects: [],
            scores: [],
            users: []
        }
    },
    methods: {
        async fetch() {
            try {
                const res = await axios.get("http://localhost:5000/api/admin/summary", { headers: { Authorization: this.token } });

                const top_scores = res.data.top_scores;

                this.subjects = Object.keys(top_scores)
                this.scores = Object.values(top_scores).map(obj => obj.score)
                this.users = Object.values(top_scores).map(obj => obj.user)

                this.renderChart()
            } catch (err) {
                console.error("Error fetching summary data", err)
            }
        },
        renderChart() {
            const ctx = document.getElementById("topScoresChart").getContext("2d");
            if (this.chart) this.chart.destroy();
            this.chart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: this.subjects,
                    datasets: [{
                        label: "Top Scores",
                        data: this.scores,
                        backgroundColor: "rgba(75,192,192,0.4)",
                        borderColor: "rgba(75,192,192,1)",
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Scores'
                            },
                            ticks: {
                                stepSize: 1
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: "Subjects"
                            }
                        }
                    },
                    plugins: {
                        legend: {display:false},
                        tooltip: {
                            callbacks: {
                                label: (context) => `${this.users[context.dataIndex]} - ${context.raw}`
                            }
                        }
                    }
                }
            });
        }
    },
    mounted() {
        this.fetch();
    }
}
</script>