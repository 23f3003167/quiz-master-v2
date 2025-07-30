<template>
    <div class="container mt-4">
        <h2 class="text-center">Welcome to User Dashboard</h2>

        <div class="d-flex justify-content-center my-3">
            <button class="btn btn-outline-primary mx-2" @click="filter('today')">Today</button>
            <button class="btn btn-outline-warning mx-2" @click="filter('upcoming')">Upcoming</button>
            <button class="btn btn-outline-danger mx-2" @click="filter('expired')">Expired</button>
            <button class="btn btn-outline-secondary mx-2" @click="filter('all')">All</button>
        </div>

        <table class="table table-bordered text-center">
            <thead class="table-primary">
                <tr>
                    <th>Title</th>
                    <th>Subject</th>
                    <th>Chapter</th>
                    <th>Date</th>
                    <th>Questions</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="q in filteredquizzes" :key="q.id">
                    <td>{{ q.title }}</td>
                    <td>{{ q.subject }}</td>
                    <td>{{ q.chapter }}</td>
                    <td>{{ q.date_of_quiz }}</td>
                    <td>{{ q.question_count }}</td>
                    <td>
                        <button class="btn btn-sm btn-info" @click="openModal(quiz)">View</button>
                        <button v-if="q.status==='today'" class="btn btn-sm btn-success" @click="attempt(q.id)">Attempt</button>
                        <span v-else-if="q.status === 'upcoming'" class="text-warning">Upcoming</span>
                        <span v-else class="text-danger">Expired</span>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="modal fade" id="quizModal" tabindex="-1" aria-labelledby="quizModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="quizModalLabel">Quiz Info</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Title:</strong>{{ modalQuiz.title }}</p>
                        <p><strong>Subject:</strong>{{ modalQuiz.subject }}</p>
                        <p><strong>Chaoter:</strong>{{ modalQuiz.chapter }}</p>
                        <p><strong>Date:</strong>{{ modalQuiz.date_of_quiz }}</p>
                        <p><strong>Questions:</strong>{{ modalQuiz.question_count }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'
import {Modal} from 'bootstrap'

export default {
    data() {
        return {
            quizzes: [],
            filteredquizzes: [],
            token: localStorage.getItem("token"),
            modalQuiz: {},
        }
    },
    methods: {
        fetchQuizzes() {
            axios.get("http://localhost:5000/api/user/quizzes", {headers: {Authorization: this.token}})
            .then(res => {
                const today = new Date().toISOString().split("T")[0]
                this.quizzes = res.data.map(q => {
                    const status = q.date_of_quiz === today ? "today": q.date_of_quiz > today ? "upcoming" : "expired"
                    return {...q, status}
                })
                this.filteredquizzes = this.quizzes;
            })
        },
        filter(status) {
            if (status==="all") this.filteredquizzes = this.quizzes
            else this.filteredquizzes = this.quizzes.filter(q => q.status === status)
        },
        openModal(quiz) {
            this.modalQuiz = quiz
            new Modal(document.getElementById("quizModal")).show()
        },
        attempt(id) {
            this.$router.push(`/user/quizzes/${id}/attempt`)
        }
    },
    mounted() {
        this.fetchQuizzes()
    }
}
</script>