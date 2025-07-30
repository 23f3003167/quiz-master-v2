<template>
    <div class="container mt-4">
        <h2>Quizzes</h2>
        <form @submit.prevent="add">
            <input v-model="title" placeholder="Title" class="form-control mb-2" />
            <input v-model="date_of_quiz" type="date" class="form-control mb-2" />
            <input v-model="time_duration" placeholder="MM:SS" class="form-control mb-2" />
            <textarea v-model="remarks" placeholder="Remarks" class="form-control mb-2" />
            <button class="btn btn-primary">Add</button>
        </form>

        <div class="mt-4" v-for="q in quizzes" :key="q.id">
            <h5>{{ q.title }}</h5>
            <small> {{ q.date_of_quiz }} | {{ q.time_duration }} | {{ q.remarks }}</small>
            <button class="btn btn-sm btn-warning" @click="edit(q)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="del(q.id)">Delete</button>
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
            axios.delete(`http://localhost:5000/api/admin/quizzes/${id}`, {headers: {Authorization: this.token}})
            .then(() => {this.fetch()})
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>