<template>
    <div class="container mt-4">
        <h2>Registered Users</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Full Name</th>
                    <th>Email</th>
                    <th>Qualification</th>
                    <th>Date of Birth</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="u in users" :key="u.id">
                    <td>{{ u.full_name }}</td>
                    <td>{{ u.email }}</td>
                    <td>{{ u.qualification }}</td>
                    <td>{{ u.dob }}</td>
                </tr>
            </tbody>
        </table>
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
