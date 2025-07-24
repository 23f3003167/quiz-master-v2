<template>
    <div>
        <h2>Subjects</h2>
        <form @submit.prevent="add">
            <input v-model="name" placeholder="Name" class="formal-control mb-2" />
            <textarea v-model="description" placeholder="Description" class="formal-control mb-2" />
            <button class="btn btn-primary">Add</button>
        </form>

        <div class="mt-4" v-for="s in subjects" :key="s.id">
            <h5>{{ s.name }}<small>{{ s.description }}</small></h5>
            <button class="btn btn-sm btn-warning" @click="edit(s)">
                Edit Subject
            </button>
            <button class="btn btn-sm btn-danger" @click="delete(s.id)">
                Delete Subject
            </button>
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
            axios.get("/api/admin/subjects",{
                headers: {Authorization: this.token}
            }).then(res => this.subjects = res.data)
        },
        add() {
            axios.post("/api/admin/subjects",{
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
                axios.put(`/api/admin/subjects/${subj.id}`,{
                name: name,
                description: description
            }, {headers: {Authorization: this.token}})
                .then(() => this.fetch())
            }
        },
        delete(id) {
            axios.delete(`/api/admin/subjects/${id}`,{
                headers: {Authorization: this.token}
            }).then(() => this.fetch())
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>