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

        <h1>Welcome, Admin</h1>

        <div class="container mt-4">
            <div class="row">
                <div class="col-md-6 mb-4" v-for="subject in subjectData" :key="subject.id">
                    <div class="card p-3 shadow-sm">
                        <h5 class="card-title">{{ subject.name }}</h5>
                        <table class="table table-bordered mt-2">
                            <thead>
                                <tr>
                                    <th>Chapters</th>
                                    <th>No. of Quizzes</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="chapter in subject.chapters" :key="chapter.id">
                                    <td>{{ chapter.name }}</td>
                                    <td>{{ chapter.quiz_count }}</td>
                                    <td>
                                        <button @click="goToManageQuizzes(chapter.id)" class="btn btn-primary">Manage</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="d-flex justify-content-end">
                            <button @click="goToManageChapters(subject.id)" class="btn btn-primary mt-2">Manage Chapters</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center mt-4">
                <button @click="goToManageSubjects" class="btn btn-primary">Manage Subjects</button>
            </div>

            <div class="text-center mt-4">
                <button @click="triggerExport" class="btn btn-outline-success">Download Users Data</button>
                <p class="mt-2 text-success">{{ msg }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
export default {
    data() {
        return {msg: '', token: localStorage.getItem("token"), subjectData: []}
    },
    methods: {
        fetch() {
            axios.get('http://localhost:5000/api/admin/dashboard-data', {headers: {Authorization: this.token}})
            .then(res => {
                this.subjectData = res.data.subjects
            }).catch(err => {
                console.error(err)
            })
        },
        goToManageSubjects() {
            this.$router.push('/admin/subjects')
        },
        goToManageChapters(subjectId) {
            this.$router.push({path: `/admin/subjects/${subjectId}/chapters`})
        },
        goToManageQuizzes(chapterId) {
            this.$router.push({path: `/admin/chapters/${chapterId}/quizzes`})
        },
        async triggerExport() {
            try {
            const res = await axios.get('http://localhost:5000/api/admin/export-users-data', {headers: {Authorization: this.token}})
            this.msg = res.data.message
        } catch (error) {
            console.error(error)
            this.msg = error.response?.data?.message || "Something went wrong"
        }
    }
    },
    mounted() {
        this.fetch();
    }
}
</script>