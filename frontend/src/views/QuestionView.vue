<template>
    <div class="container mt-4">
        <form @submit.prevent="add">
            <input v-model="question_statement" placeholder="Question Statement" class="formal-control mb-2" />
            <input v-model="option_1" placeholder="Option 1" class="formal-control mb-2" />
            <input v-model="option_2" placeholder="Option 2" class="formal-control mb-2" />
            <input v-model="option_3" placeholder="Option 3" class="formal-control mb-2" />
            <input v-model="option_4" placeholder="Option 4" class="formal-control mb-2" />
            <input v-model="correct_option" placeholder="Correct Option (1-4)" class="formal-control mb-2" />
            <button class="btn btn-success">Add</button>

        </form>

        <div class="mt-4" v-for="q in questions" :key="q.id">
            <h5>{{ q.question_statement }}</h5>
            <small> {{ q.option_1 }} | {{ q.option_2 }} | {{ q.option_3 }} | {{ q.option_4 }} </small>
            <h5> Correct Option is {{ q.correct_option}}</h5>
            <button class="btn btn-sm btn-warning" @click="edit(q)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="del(q.id)">Delete</button>
        </div> 
    </div>
</template>

<script>
import axios from 'axios'
export default {
    props: ['quiz_id'],
    data() {
        return {
            questions: [],
            question_statement: '',
            option_1: '',
            option_2: '',
            option_3: '',
            option_4: '',
            correct_option: '',
            token: localStorage.getItem("token")
        }
    },
    methods: {
        fetch() {
            axios.get(`http://localhost:5000/api/admin/${this.quiz_id}/questions`, {headers: {Authorization: this.token}})
            .then(res => this.questions = res.data)
        },
        add() {
            axios.post(`http://localhost:5000/api/admin/${this.quiz_id}/questions`, {question_statement: this.question_statement, option_1: this.option_1, option_2: this.option_2, option_3: this.option_3, option_4: this.option_4, correct_option: this.correct_option}, {headers: {Authorization: this.token}})
            .then(() => {
                this.question_statement=''
                this.option_1=''
                this.option_2=''
                this.option_3=''
                this.option_4=''
                this.correct_option=''
                this.fetch()
            })
        },
        edit(q) {
            const question_statement = prompt('New Question Statement', q.question_statement)
            const option_1 = prompt(['New Option 1', q.option_1])
            const option_2 = prompt(['New Option 2', q.option_2])
            const option_3 = prompt(['New Option 3', q.option_3])
            const option_4 = prompt(['New Option 4', q.option_4])
            const correct_option = prompt("Correct Option (1-4)", q.correct_option)
            axios.put(`http://localhost:5000/api/admin/questions/${q.id}`, {question_statement: question_statement, option_1: option_1, option_2: option_2, option_3: option_3, option_4: option_4, correct_option: correct_option}, {headers: {Authorization: this.token}})
            .then(() => {this.fetch()})
        },
        del(id) {
            axios.delete(`http://localhost:5000/api/admin/questions/${id}`, {headers: {Authorization: this.token}})
            .then(() => {this.fetch()})
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>