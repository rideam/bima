import { createRouter, createWebHistory } from "vue-router";
import App from "../App.vue";
import { useUsersStore } from "@/stores/user";

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
          // props: (route) => ({ title: route.query.q }),
        },
        {
          path: "/empty",
          name: "empty",
          component: () => import("../views/EmptyPage.vue"),
          meta: { requiresAuth: true },
        },
      ],
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginPage.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegistrationPage.vue"),
    },
  ],
});

router.beforeEach((to, _, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (useUsersStore().isAuthenticated) {
      next();
      return;
    }
    next("/login");
  } else {
    next();
  }
});

export default router;
