import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SubjectView from '../views/SubjectView.vue'
import ChapterView from '../views/ChapterView.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/admin/subjects',
    name: 'Subjects',
    component: SubjectView
  },
  {
    path: '/admin/subjects/:id/chapters',
    name: 'Chapters',
    component: ChapterView,
    props: route => ({subject_id: route.params.id})
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
