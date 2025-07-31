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

        <div class="container mt-5">
            <div class="card shadow p-4">
                <h1 class="text-center text-primary">All Registered Users</h1>

                <div class="table-responsive mt-4">
                    <table class="table table-bordered table-striped text-center">
                        <thead>
                            <tr>
                                <th>Full Name</th>
                                <th>Email</th>
                                <th>Qualification</th>
                                <th>Date of Birth</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in users" :key="user.id">
                                <td>{{ user.full_name }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ user.qualification }}</td>
                                <td>{{ user.dob }}</td>
                            </tr>
                            <tr v-if="users.length === 0">
                                <td colspan="4" class="text-center">No users found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="text-center mt-4">
                    <router-link to="/admin/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            users: [],
            token: localStorage.getItem("token")
        }
    },
    methods: {
        fetch() {
            axios.get("http://localhost:5000/api/admin/users", {headers: {Authorization: this.token}})
            .then(res => this.users = res.data)
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>
