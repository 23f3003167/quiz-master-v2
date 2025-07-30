<template>
    <div class="container mt-5">
        <div class="card shadow p-4">
            <h2>{{quiz.title}}</h2>
            <h4 id="timer" class="text-center text-danger fw-bold">{{ timeText }}</h4>

            <form @submit.prevent="submitQuiz">
                <div v-for="(q, index) in questions" :key="q.id" class="mb-4">
                    <p class="fw-semibold">{{ index+1 }}.{{ q.question_statement }}</p>
                    <div v-for="option in 4" :key="option" class="form-check">
                        <input class="form-check-input" type="radio" :name="'question_'+q.id" :value="option" v-model="answers[q.id]" />
                        <label class="form-check-label">{{ q['option_'+opt] }}</label>
                    </div>
                </div>

                <div class="d-flex justify-content-between mt-4">
                    <router-link to="/user" class="btn btn-secondary">Back to Dashboard</router-link>
                    <button type="submit" class="btn btn-success">Submit Quiz</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            quiz: [],
            questions: [],
            answers: {},
            timeLeft: 0,
            timeText: '',
            token: localStorage.getItem("token")
        }
    },
    methods: {
        fetchQuestions() {
            const quiz_id = this.$route.params.id
            axios.get(`http://localhost:5000/api/user/quizzes/${quiz_id}/questions`, {headers: {Authorization: this.token}})
            .then(res => {
                this.quiz = res.data.quiz,
                this.questions = res.data.questions,
                this.timeLeft = parseInt(this.quiz.time_duration) * 60
                this.startTimer()
            })
        },
        startTimer() {
            let interval = setInterval(() => {
                const min = Math.floor(this.timeLeft/60).toString.padStart(2,'0')
                const sec = (this.timeLeft%60).toString.padStart(2,'0')
                this.timeText = `Time Remaining: ${min}:${sec}`
                if (this.timeLeft <= 0) {
                    clearInterval(interval)
                    this.submitQuiz()
                }
                this.timeLeft--;
            }, 1000)
        },
        submitQuiz() {
            const quiz_id = this.$route.params.id
            axios.get(`http://localhost:5000/api/user/quizzes/${quiz_id}/submit`, this.answers, {headers: {Authorization: this.token}})
            .then(res => {
                alert(res.data.message)
                this.$router.push("/user/dashboard")
            })
        }
    },
    mounted() {
        this.fetchQuestions()
    }
}
</script>