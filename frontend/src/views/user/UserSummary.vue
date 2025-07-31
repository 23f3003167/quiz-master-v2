<template>
     <div class="p-4">
        <nav class="bg-light p-3 d-flex justify-content-between mb-4">
            <div>
                <router-link to="/user/dashboard" class="me-3">Home</router-link>
                <router-link to="/user/scores" class="me-3">Scores</router-link>
                <router-link to="/user/summary" class="me-3">Summary</router-link>
                <router-link to="/" class="text-danger">Logout</router-link>
            </div>
            <button @click="$router.push('/user/search')" class="btn btn-primary">Search</button>
        </nav>
    <div class="card shadow p-4">
      <h2 class="text-center text-primary">Your Quiz Performance</h2>
      <div class="chart-container" style="position: relative; height: 300px;">
        <canvas id="quizChart"></canvas>
      </div>
      <div class="text-center mt-3">
        <router-link to="/user/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
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
            chart: null
        }
    },
    methods: {
        async fetch() {
            const res = await axios.get("http://localhost:5000/api/user/summary", { headers: {Authorization: this.token}})

            const {quiz_titles, scores_list} = res.data;

            if (this.chart) this.chart.destroy();

            const ctx = document.getElementById("quizChart").getContext("2d")
            this.chart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: quiz_titles,
                    datasets: [{
                        label: "Quiz Scores",
                        data: scores_list,
                        backgroundColor: "rgba(54,162,235,0.7)",
                        borderColor: "rgba(54,162,235,1)",
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
                                text: "Score"
                            },
                            ticks: {stepSize: 1}
                        },
                        x: {
                            title: {
                                display: true,
                                text: "Quiz Titles"
                            }
                        }
                    },
                    plugins: {
                        legend: {display: false}
                    }
                }
            })
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>