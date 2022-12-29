import { createRouter, createWebHistory } from "vue-router";
import App from "../App.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "app",
      component: App,
      children: [
        {
          path: "",
          name: "home",
          component: () => import("../views/HomePage.vue"),
          props: (route) => ({ title: route.query.q }),
        },
      ],
    },
  ],
});

export default router;
