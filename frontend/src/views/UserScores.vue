<template>
    <div class="container mt-4">
        <h2 class="text-center mb-4">Quiz Scores</h2>
        <div class="table-responsive">
        <table class="table table-bordered text-center">
            <thead class="table-primary">
                <tr>
                    <th>Quiz Title</th>
                    <th>Attempted on</th>
                    <th>No. of Questions</th>
                    <th>Scores</th>
                    <th>Time Taken</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(s, index) in scores" :key="index">
                    <td>{{ s.title }}</td>
                    <td>{{ s.attempted_on }}</td>
                    <td>{{ s.question_count }}</td>
                    <td>{{ s.total_scored }}</td>
                    <td>{{ s.completion_minutes }}m {{ s.completion_seconds }}</td>
                </tr>
                <tr v-if="scores.length==0">
                    <td colspan="5">No Quiz Attempts</td>
                </tr>
            </tbody>
        </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            scores: [],
            token: localStorage.getItem("token")
        }
    },
    methods: {
        fetch() {
            axios.get("http://localhost:5000/api/user/scores", {headers: {Authorisation: this.token}})
            .then(res => this.scores = res.data)
        }
    },
    mounted() {
        this.fetch()
    }
} 
</script>