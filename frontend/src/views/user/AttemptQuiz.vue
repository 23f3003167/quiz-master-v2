<template>
  <div class="container mt-5">
    <div v-if="quiz && questions.length" class="card shadow p-4">
      <h2 class="text-center text-primary">{{ quiz.title }}</h2>
      <h4 class="text-center text-danger fw-bold">{{ timerText }}</h4>

      <form @submit.prevent="submitQuiz">
        <div v-for="(q, index) in questions" :key="q.id" class="mb-4">
          <p class="fw-semibold">{{ index + 1 }}. {{ q.statement }}</p>
          <div v-for="(opt, idx) in q.options" :key="idx" class="form-check">
            <input
              type="radio"
              class="form-check-input"
              :name="'question_' + q.id"
              :value="idx + 1"
              v-model="userAnswers[q.id]"
              required
            />
            <label class="form-check-label">{{ opt }}</label>
          </div>
        </div>

        <div class="d-flex justify-content-between mt-4">
          <router-link to="/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
          <button class="btn btn-success" type="submit">Submit Quiz</button>
        </div>
      </form>
    </div>
    <div v-else>
      <p>Loading quiz...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AttemptQuiz",
  data() {
    return {
      quiz: null,
      startTime: null,
      questions: [],
      userAnswers: {},
      timer: 0,
      timerText: "",
      interval: null,
      token: localStorage.getItem("token")
    };
  },
  methods: {
    async fetchQuiz() {
      try {
        const res = await axios.get(`http://localhost:5000/user/quizzes/${this.$route.params.id}/attempt`, {
          headers: {
            Authorization: this.token
          }
        });
        this.quiz = res.data.quiz;
        this.questions = res.data.questions;
        this.timer = parseInt(this.quiz.time_duration) * 60;
        this.startTime = new Date().toISOString();
        this.startTimer();
      } catch (err) {
        console.error("Quiz fetch error:", err.response?.data || err.message);
        alert("Quiz could not be loaded. Check console for details.");
      }
    },
    startTimer() {
      this.interval = setInterval(() => {
        const min = Math.floor(this.timer / 60).toString().padStart(2, "0");
        const sec = (this.timer % 60).toString().padStart(2, "0");
        this.timerText = `Time Remaining: ${min}:${sec}`;
        if (this.timer <= 0) {
          clearInterval(this.interval);
          this.submitQuiz();
        }
        this.timer--;
      }, 1000);
    },
    async submitQuiz() {
      clearInterval(this.interval);
      try {
        const res = await axios.post(`http://localhost:5000/user/quizzes/${this.$route.params.id}/attempt`, {
          answers: this.userAnswers,
          start_time: this.startTime
        }, {
          headers: {
            Authorization: this.token
          }
        });
        alert(
          `Submitted! Score: ${res.data.score}/${res.data.total} in ${res.data.minutes}m ${res.data.seconds}s`
        );
        this.$router.push("/user/dashboard");
      } catch (err) {
        console.error("Submit error:", err.response?.data || err.message);
        alert("Submission failed.");
      }
    }
  },
  mounted() {
    this.fetchQuiz();
  }
};
</script>