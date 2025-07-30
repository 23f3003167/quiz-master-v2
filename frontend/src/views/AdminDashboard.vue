<template>
    <div>
        <button @click="triggerExport" class="btn btn-outline-success">Download Users Data</button>
        <p v-if="msg">{{ message }}</p>
    </div>
</template>

<script>
import axios from "axios"
export default {
    data() {
        return {msg: '', token: localStorage.getItem("token")}
    },
    methods: {
        async triggerExport() {
            try {
            const res = await axios.get('http://localhost:5000/api/admin/export-users-data', {headers: {Authorization: this.token}})
            this.msg = res.data.message
        } catch (error) {
            console.error(error)
            this.msg = error.response?.data?.message || "Something went wrong"
            }
        }
    }
}
</script>