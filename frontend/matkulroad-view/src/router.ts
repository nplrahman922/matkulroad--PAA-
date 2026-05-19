import { createMemoryHistory,createRouter } from "vue-router";
import MainMenu from "@/MainMenu.vue";
import LoginAdmin from "@/LoginAdmin.vue";
import AdminDash from "@/AdminDash.vue";

const routes = [
{path : '/' , component :MainMenu},
{path : '/adminlogin', component : LoginAdmin},
{path : '/dashboard' , component : AdminDash}
]

export const router = createRouter({
history : createMemoryHistory(),
routes,
})