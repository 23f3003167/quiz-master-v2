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

        <div class="container mt-4">
            <h1 class="mb-4 text-center">Manage Quizzes</h1>

            <div class="row">
                <div class="col-md-6 mb-4" v-for="q in quizzes" :key="q.id">
                    <div class="card p-3 shadow-sm">
                        <h5 class="card-title">{{ q.title }}</h5>
                        <p><strong>Date:</strong> {{ q.date_of_quiz }}</p>
                        <p><strong>Duration:</strong> {{ q.time_duration }} min</p>
                        <p><strong>Remarks:</strong> {{ q.remarks || 'No remarks' }}</p>
                        <div class="d-flex justify-content-between">
                            <button @click="viewQuestions(q.id)" class="btn btn-sm btn-success">View</button>
                            <button @click="edit(q)" class="btn btn-sm btn-warning">Edit</button>
                            <button @click="del(q.id)" class="btn btn-sm btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>

            <hr>

            <div class="text-center mb-4">
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addQuizModal">
                Add Quiz
                </button>
            </div>

            <div class="modal fade" id="addQuizModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title">Add Quiz</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                     <form @submit.prevent="add">
                        <div class="mb-3">
                            <label class="form-label">Title</label>
                            <input v-model="title" type="text" placeholder="Title" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Date of Quiz</label>
                            <input v-model="date_of_quiz" type="date" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Time Duration (min)</label>
                            <input v-model="time_duration" type="number" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Remarks</label>
                            <textarea v-model="remarks" placeholder="Remarks" class="form-control" rows="3"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100" data-bs-dismiss="modal">Add Quiz</button>
                    </form>
                    </div>
                </div>
            </div>
        </div>

        <div class="text-center mt-4">
            <router-link to="/admin/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
        </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
export default {
    props: ['chapter_id'],
    data() {
        return {
            quizzes: [],
            title: '',
            date_of_quiz: '',
            time_duration: '',
            remarks: '',
            token: localStorage.getItem("token")
        }
    },
    methods: {
        fetch() {
            axios.get(`http://localhost:5000/api/admin/${this.chapter_id}/quizzes`, {headers: {Authorization: this.token}})
            .then(res => this.quizzes = res.data)
        },
        add() {
            axios.post(`http://localhost:5000/api/admin/${this.chapter_id}/quizzes`, {title: this.title, date_of_quiz: this.date_of_quiz, time_duration: this.time_duration, remarks: this.remarks}, {headers: {Authorization: this.token}})
            .then(() => {
                this.title=''
                this.date_of_quiz=''
                this.time_duration=''
                this.remarks=''
                this.fetch()
            })
        },
        edit(q) {
            const title = prompt('New Title', q.title)
            const date_of_quiz = prompt('New Data of Quiz', q.date_of_quiz)
            const time_duration = prompt('New Time Duration', q.time_duration)
            const remarks = prompt('New Remarks', q.remarks)
            axios.put(`http://localhost:5000/api/admin/quizzes/${q.id}`, {title: title, date_of_quiz: date_of_quiz, time_duration: time_duration, remarks: remarks}, {headers: {Authorization: this.token}})
            .then(() => {this.fetch()})
        },
        del(id) {
            if (confirm("Are you sure you want to delete this quiz?")) {
                axios.delete(`http://localhost:5000/api/admin/quizzes/${id}`, {headers: {Authorization: this.token}})
                .then(() => {this.fetch()})
            }
        },
        viewQuestions(quizId) {
            this.$router.push(`/admin/quizzes/${quizId}/questions`);
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>