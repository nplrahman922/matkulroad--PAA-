import { createMemoryHistory,createRouter } from "vue-router";
import MainMenu from "@/MainMenu.vue";

const routes = [
{path : '/' , component :MainMenu}
]

export const router = createRouter({
history : createMemoryHistory(),
routes,
})