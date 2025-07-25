<template>
    <div class="container mt-4">
        <h2>Chapters</h2>
        <form @submit.prevent="add">
            <input v-model="name" placeholder="Name" class="formal-control mb-2" />
            <textarea v-model="description" placeholder="Description" class="formal-control mb-2" />
            <button class="btn btn-primary">Add</button>
        </form>

        <div class="mt-4" v-for="c in chapters" :key="c.id">
            <h5>{{ c.name }}<small>{{ c.description }}</small></h5>
            <button class="btn btn-sm btn-warning" @click="edit(c)">
                Edit
            </button>
            <button class="btn btn-sm btn-danger" @click="del(c.id)">
                Delete
            </button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    props: ['subject_id'],
    data() {
        return {
            chapters: [],
            name: '',
            description: '',
            token: localStorage.getItem("token")
        }
    },
    methods: {
        fetch() {
            axios.get(`http://localhost:5000/api/admin/${this.subject_id}/chapters`, {headers: {Authorization: this.token}})
            .then(res => this.chapters = res.data)
        },
        add() {
            axios.post(`http://localhost:5000/api/admin/${this.subject_id}/chapters`, {name:this.name, description:this.description}, {headers: {Authorization: this.token}})
            .then(() => {
                this.name=''
                this.description=''
                this.fetch()
            })
        },
        edit(chapter) {
            const name = prompt("New name", chapter.name)
            const description = prompt("New description", chapter.description)
            if (name && description) {
                axios.put(`http://localhost:5000/api/admin/chapters/${chapter.id}`, {name: name, description: description}, {headers: {Authorization: this.token}})
                .then(() => {this.fetch()})
            }
        },
        del(id) {
            axios.delete(`http://localhost:5000/api/admin/chapters/${id}`, {headers: {Authorization: this.token}})
            .then(() => {this.fetch()})
        }
    },
    mounted() {
        this.fetch()
    }
}
</script>