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
        <div class="container mt-5">
        <div class="card shadow p-4">
            <h1 class="text-center text-primary">{{ quiz.title }}</h1>
            <h4 id="timer" class="text-center text-danger fw-bold">{{ timeText }}</h4>

            <form @submit.prevent="submitQuiz" class="mt-4">
                <div v-for="(q, index) in questions" :key="q.id" class="mb-4">
                    <p class="fw-semibold">{{ index+1 }}.{{ q.question_statement }}</p>
                    <div v-for="n in 4" :key="n" class="form-check">
                        <input
                            class="form-check-input"
                            type="radio"
                            :name="'question_' + q.id"
                            :value="n"
                            v-model="answers[q.id]"
                            required
                        />
                        <label class="form-check-label">{{ q['option_' + n] }}</label>
                    </div>
                </div>

                <div class="d-flex justify-content-between mt-4">
                    <router-link to="/user/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
                    <button type="submit" class="btn btn-success">Submit Quiz</button>
                </div>
            </form>
        </div>
    </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            quiz: {},
            questions: [],
            answers: {},
            timeRemaining: 0,
            timeText: '',
            startTime: null,
            token: localStorage.getItem("token"),
            timer: null
        }
    },
    methods: {
        fetchQuestions() {
            const quiz_id = this.$route.params.id
            axios.get(`http://localhost:5000/api/user/quizzes/${quiz_id}/questions`, {headers: {Authorization: this.token}})
            .then(res => {
                console.log("Quiz Data:", res.data.quiz)
                console.log("Questions:", res.data.questions)
                this.quiz = res.data.quiz,
                this.questions = res.data.questions,
                this.startTime = new Date().toISOString()
                const [min, sec] = this.quiz.time_duration.split(":").map(Number)
                this.timeRemaining = (min * 60) + sec
                this.startTimer()
            })
            .catch(err => {
                console.error("Error fetching quiz questions", err)
            })
        },
        startTimer() {
            this.timer = setInterval(() => {
                const min = Math.floor(this.timeRemaining/60).toString().padStart(2,'0')
                const sec = (this.timeRemaining%60).toString().padStart(2,'0')
                this.timeText = `Time Remaining: ${min}:${sec}`
                if (this.timeRemaining <= 0) {
                    clearInterval(this.timer)
                    this.submitQuiz()
                }
                this.timeRemaining--;
            }, 1000)
        },
        submitQuiz() {
            clearInterval(this.timer)
            const quiz_id = this.$route.params.id
            const payload = {
                start_time: this.startTime,
                answers: Object.keys(this.answers).map(qid => ({
                    question_id: parseInt(qid),
                    selected: parseInt(this.answers[qid])
                }))
            }
            axios.post(`http://localhost:5000/api/user/quizzes/${quiz_id}/submit`, payload , {headers: {Authorization: this.token}})
            .then(res => {
                alert(`${res.data.message}\nScore: ${res.data.score}\nTime: ${res.data.time}`)
                this.$router.push("/user/dashboard")
            })
        }
    },
    mounted() {
        console.log("AttemptQuiz.vue mounted")
        this.fetchQuestions()
    }
}
</script>