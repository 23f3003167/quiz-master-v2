<template>
    <div class="container mt-4">
        <h2>Login Page</h2>
        <form @submit.prevent="login">
            <select v-model="role" class="form-control mb-2">
                <option value="user">User</option>
                <option value="admin">Admin</option>
            </select>
            <input v-model="email" placeholder="Email" class="form-control mb-2" />
            <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />
            <button class="btn btn-success">Login</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            email: '',
            password: '',
            role: 'user'
        };
    },
    methods: {
        login() {
            axios.post("http://localhost:5000/", {email: this.email, password: this.password, role: this.role})
            .then(res => {
                localStorage.setItem("token", res.data.token)
                alert("Logged in Successfully")
                this.$router.push(this.role==="admin" ? '/admin/subjects': '/user/dashboard')
            }).catch(() => alert("Login Failed"))
        }
    }
};
</script>