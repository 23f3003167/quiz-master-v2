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
            <h1 class="mb-4 text-center">Manage Questions</h1>

            <div class="row">
                <div class="col-md-6 mb-4" v-for="q in questions" :key="q.id">
                    <div class="card p-3 shadow-sm">
                        <h5 class="card-title">{{ q.question_statement }}</h5>
                        <p><strong>Option 1:</strong> {{ q.option_1 }}</p>
                        <p><strong>Option 2:</strong> {{ q.option_2 }}</p>
                        <p><strong>Option 3:</strong> {{ q.option_3 }}</p>
                        <p><strong>Option 4:</strong> {{ q.option_4 }}</p>
                        <p><strong>Correct Option:</strong> {{ q.correct_option }}</p>
                        <div class="d-flex justify-content-between">
                            <button @click="edit(q)" class="btn btn-sm btn-warning">Edit</button>
                            <button @click="del(q.id)" class="btn btn-sm btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>

            <hr>

            <div class="text-center mb-4">
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addQuestionModal">
                Add Question
                </button>
            </div>

            <div class="modal fade" id="addQuestionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title">Add Question</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                    <form @submit.prevent="add">
                        <div class="mb-3">
                            <label class="form-label">Question Statement</label>
                            <input v-model="question_statement" type="text" placeholder="Question Statement" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Option 1</label>
                            <input v-model="option_1" type="text" placeholder="Option 1" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Option 2</label>
                            <input v-model="option_2" type="text" placeholder="Option 2" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Option 3</label>
                            <input v-model="option_3" type="text" placeholder="Option 3" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Option 4</label>
                            <input v-model="option_4" type="text" placeholder="Option 4" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Correct Option (1-4):</label>
                            <input v-model="correct_option" type="number" min="1" max="4" placeholder="Correct Option" class="form-control mb-2" />
                        </div>
                        <button type="submit" class="btn btn-primary w-100" data-bs-dismiss="modal">Add Question</button>
                    </form>
                    </div>
                </div>
            </div>
        </div>

        <div class="text-center mt-4">
            <router-link :to="`/admin/dashboard`" class="btn btn-secondary">Back to Dashboard</router-link>
        </div>
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
            if (confirm("Are you sure you want to delete this question?")) {
                axios.delete(`http://localhost:5000/api/admin/questions/${id}`, {headers: {Authorization: this.token}})
                .then(() => {this.fetch()})
            }
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>