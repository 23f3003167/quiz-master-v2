import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/auth/LoginView.vue'
import UserView from '../views/admin/UsersView.vue'
import SubjectView from '../views/admin/SubjectView.vue'
import ChapterView from '../views/admin/ChapterView.vue'
import QuizView from '@/views/admin/QuizView.vue'
import QuestionView from '@/views/admin/QuestionView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import UserDashboard from '@/views/user/UserDashboard.vue'
import AttemptQuiz from '@/views/user/AttemptQuiz.vue'
import UserScores from '@/views/user/UserScores.vue'
import UserSummary from '@/views/user/UserSummary.vue'
import UserSearch from '@/views/user/UserSearch.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import AdminSearch from '@/views/admin/AdminSearch.vue'
import AdminSummary from '@/views/admin/AdminSummary.vue'

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/admin/users',
    name: 'Users',
    component: UserView
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
  },
  {
    path: '/admin/chapters/:id/quizzes',
    name: 'Quizzes',
    component: QuizView,
    props: route => ({chapter_id: route.params.id})
  },
  {
    path: '/admin/quizzes/:id/questions',
    name: 'Questions',
    component: QuestionView,
    props: route => ({quiz_id: route.params.id})
  },
  {
    path: '/admin/dashboard',
    name: 'Admin Dashboard',
    component: AdminDashboard
  },
  {
    path: '/admin/search',
    name: 'Admin Search',
    component: AdminSearch
  },
  {
    path: '/admin/summary',
    name: 'Admin Summary',
    component: AdminSummary
  },
  {
    path: '/user/quizzes/:id/attempt',
    name: 'Attempt Quiz',
    component: AttemptQuiz
  },
  {
    path: '/user/dashboard',
    name: 'User Dashboard',
    component: UserDashboard
  },
  {
    path: '/user/scores',
    name: 'User Scores',
    component: UserScores
  },
  {
    path: '/user/summary',
    name: 'User Summary',
    component: UserSummary
  },
  {
    path: '/user/search',
    name: 'User Search',
    component: UserSearch
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
