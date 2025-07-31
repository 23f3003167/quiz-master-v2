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

    <h2>Admin Search</h2>
    <input v-model="searchTerm" placeholder="Enter keyword..." class="form-control mb-2" />
    <div class="form-check form-check-inline" v-for="opt in filters" :key="opt">
      <input type="checkbox" :value="opt" v-model="filterBy" class="form-check-input" />
      <label class="form-check-label text-capitalize">{{ opt }}</label>
    </div>
    <button @click="search" class="btn btn-primary mt-2">Search</button>

    <ul class="list-group mt-3">
      <li v-for="(result, index) in results" :key="index" class="list-group-item">
         <template v-if="result.type === 'user'">
          User: {{ result.name }} ({{ result.email }})
        </template>
        <template v-else-if="result.type === 'subject'">
          Subject: {{ result.name }}
        </template>
        <template v-else-if="result.type === 'quiz'">
          Quiz: {{ result.title }}
        </template>
        <template v-else-if="result.type === 'question'">
          Question: {{ result.question_statement }}
        </template>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            searchTerm: '',
            filterBy: [],
            results: [],
            filters: ['users', 'subjects', 'quizzes', 'questions'],
            token: localStorage.getItem('token')
        }
    },
    methods: {
        async search() {
          const res = await axios.post('http://localhost:5000/api/admin/search' ,{
            search_term: this.searchTerm,
            filter_by: this.filterBy,
      },
    {headers: {Authorization: this.token}});
      this.results = res.data;
    }
    }
}
</script>