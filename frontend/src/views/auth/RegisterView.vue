<template>
    <div class="container mt-5">
        <h1 class="text-center mb-3">Welcome to Quiz Master</h1>
        <h2 class="text-center mb-4">User Registration</h2>

        <div v-if="errorMsg" class="alert alert-danger text-center">
            {{ errorMsg }}
        </div>

        <form @submit.prevent="register" class="p-4 border rounded shadow-sm w-50 mx-auto">
            <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input v-model="full_name" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="email" type="email" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Qualification</label>
                <input v-model="qualification" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Date of Birth</label>
                <input v-model="dob" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Password</label>
                <input v-model="password" type="password" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Confirm Password</label>
                <input v-model="confirmPassword" type="password" class="form-control" required />
            </div>

            <button class="btn btn-primary w-100">Register</button>
        </form>

        <div class="text-center mt-3">
            <p>Already Registered?</p>
            <router-link to="/" class="btn btn-secondary">Login</router-link>
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
            confirmPassword: '',
            full_name: '',
            qualification: '',
            dob: '',
            errorMsg: ''
        };
    },
    methods: {
        register() { 
            if (this.password !== this.confirmPassword) {
                this.errorMsg = "Password not matching."
                return;
            }
            axios.post("http://localhost:5000/register", {email: this.email, password: this.password, full_name: this.full_name, qualification: this.qualification, dob: this.dob})
            .then(()=>{
                alert("Registered successfully, Please log in.")
                this.$router.push("/")
            }).catch(()=> {
                this.errorMsg = "Registration Failed."
            })
        }
    }
};
</script>