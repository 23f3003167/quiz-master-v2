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

        <div class="container mt-4">
            <h1 class="mb-4 text-center">Manage Subjects</h1>

            <div class="row">
                <div class="col-md-6 mb-4" v-for="s in subjects" :key="s.id">
                    <div class="card p-3 shadow-sm">
                        <h5 class="card-title">{{ s.name }}</h5>
                        <p class="card-text">{{ s.description }}</p>
                        <div class="d-flex justify-content-between">
                            <button @click="viewChapters(s.id)" class="btn btn-sm btn-success">View</button>
                            <button @click="edit(s)" class="btn btn-sm btn-warning">Edit</button>
                            <button @click="del(s.id)" class="btn btn-sm btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>

            <hr>

            <div class="text-center mb-4">
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSubjectModal">
                Add Subject
                </button>
            </div>

            <div class="modal fade" id="addSubjectModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title">Add Subject</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                     <form @submit.prevent="add">
                        <div class="mb-3">
                            <label class="form-label">Subject Name</label>
                            <input v-model="name" placeholder="Name" class="form-control mb-2" />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea v-model="description" placeholder="Description" class="form-control" rows="3"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100" data-bs-dismiss="modal">Add Subject</button>
                    </form>
                    </div>
                </div>
            </div>
        </div>

        <div class="text-center mt-4">
            <router-link to="/admin/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
        </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            subjects: [],
            name: '',
            description: '',
            token: localStorage.getItem('token'),
        }
    },
    methods: {
        fetch(){
            axios.get("http://localhost:5000/api/admin/subjects",{
                headers: {Authorization: this.token}
            }).then(res => this.subjects = res.data)
        },
        add() {
            axios.post("http://localhost:5000/api/admin/subjects",{
                name: this.name,
                description: this.description
            }, { headers: {Authorization: this.token}})
            .then(() => {
                this.name=''
                this.description=''
                this.fetch()
            })
        },
        edit(subj) {
            const name = prompt("New name", subj.name)
            const description = prompt("New Description", subj.description)
            if (name && description) {
                axios.put(`http://localhost:5000/api/admin/subjects/${subj.id}`,{
                name: name,
                description: description
            }, {headers: {Authorization: this.token}})
                .then(() => this.fetch())
            }
        },
        del(id) {
            if (confirm("Are you sure you want to delete this subject?")) {
                axios.delete(`http://localhost:5000/api/admin/subjects/${id}`,{
                    headers: {Authorization: this.token}
                }).then(() => this.fetch())
            }
        },
        viewChapters(subjectId) {
            this.$router.push(`/admin/subjects/${subjectId}/chapters`);
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>