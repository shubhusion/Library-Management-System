import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue'
import LoginForm from '../components/LoginPage.vue'
import SignUp from '../components/UserSignup.vue'
import NavBar from '../components/UserHomePage.vue'
import UserAccount from '../components/Account.vue'
import UserDashboard from '../components/UserDashboard.vue'
import UserBooking from '../components/UserBookings.vue'
// import BookShow from '../components/BookShow.vue'
import AdminHomePage from '../components/AdminHomePage.vue'
import SectionForm from '../components/CreateSection.vue'
import EditSection from '../components/EditSection.vue'
// import VenueShows from '../components/VenueShows.vue'
import CreateBook from '../components/CreateBook.vue'
import EditBook from '../components/EditBook.vue'
import RequestBook from '../components/RequestBook.vue'
import UserFeedback from '../components/UserFeedback.vue'
import DownloadBook from '../components/DownloadBook.vue';

const routes = [
    {path: '/', component: HomePage},

    {path: '/userlogin', component: LoginForm},

    {path: '/signup', component: SignUp},

    {path: '/navbar', component: NavBar},

    {path: '/userhome', component: NavBar},

    {path: '/account', component: UserAccount},

    {path: '/dashboard', component: UserDashboard},

    {path: '/userbooking/:user_id', component: UserBooking},

    {path: '/adminHomePage', component: AdminHomePage},

    {path: '/sectionform', component: SectionForm},

    {path:'/editsection/:section_id', component: EditSection},

    {path:'/createbook/:book_id', component: CreateBook},
    
    {path:'/editbook/:book_id', component: EditBook},

    {path:'/managebooks' , component: RequestBook},

    {path:'/feedback/users/:user_id/books/:book_id/feedbacks' , component: UserFeedback},

    {path:'/userbooking/download/:book_id', component: DownloadBook}

];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;