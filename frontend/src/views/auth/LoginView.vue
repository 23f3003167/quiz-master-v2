<template>
    <div class="container mt-5">
        <h1 class="text-center mb-3">Welcome to Quiz Master</h1>
        <h2 class="text-center mb-4">Login</h2>

        <div v-if="errorMsg" class="alert alert-danger text-center">
            {{ errorMsg }}
        </div>

        <form @submit.prevent="login" class="p-4 border rounded shadow-sm w-50 mx-auto">
            <div class="mb-3">
                <label class="form-label">Role</label>
                <select v-model="role" class="form-select" required>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                </select>
            </div>

            <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" v-model="email" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" v-model="password" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>
        <div class="text-center mt-3">
            <p>Don't have an account?</p>
            <router-link to="/register" class="btn btn-secondary">Register</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            email: '',
            password: '',
            role: 'user',
            errorMsg: ''
        };
    },
    methods: {
        login() {
            axios.post("http://localhost:5000/", {email: this.email, password: this.password, role: this.role})
            .then(res => {
                localStorage.setItem("token", res.data.token)
                this.$router.push(this.role==="admin" ? '/admin/dashboard': '/user/dashboard')
            }).catch(() => {
                this.errorMsg = "Invalid Credentials."
            })
        }
    }
};
</script>