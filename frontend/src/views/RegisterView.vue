<template>
    <div class="container mt-4">
        <h2>Registration Page</h2>
        <form @submit.prevent="register">
            <input v-model="email" type="email" placeholder="Email" class="form-control mb-2" />
            <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />
            <input v-model="full_name" placeholder="Full Name" class="form-control mb-2" />
            <input v-model="qualification" placeholder="Qualification" class="form-control mb-2" />
            <input v-model="dob" type="date" class="form-control mb-2" />
            <button class="btn btn-primary">Register</button>
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
            full_name: '',
            qualification: '',
            dob: ''
        };
    },
    methods: {
        register() {
            axios.post("http://localhost:5000/register", {email: this.email, password: this.password, full_name: this.full_name, qualification: this.qualification, dob: this.dob})
            .then(()=>{
                alert("Registered successfully, Please log in.")
                this.$router.push("/")
            }).catch(()=> alert("Registerd Failed"))
        }
    }
};
</script>