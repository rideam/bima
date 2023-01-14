import { defineStore } from "pinia";
import axios from "axios";
import { useStorage } from "@vueuse/core";

export const useUsersStore = defineStore({
  id: "user",
  state: () => ({
    user: useStorage("user", null),
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    stateUser: (state) => state.user,
  },
  actions: {
    async register(form) {
      await axios.post("register", form);
      const auth = new FormData();
      auth.append("username", form.username);
      auth.append("password", form.password);
      await this.logIn(auth);
    },
    async logIn(user) {
      await axios.post("login", user);
      await this.viewMe();
    },
    async viewMe() {
      const { data } = await axios.get("profile");
      await this.setUser(JSON.stringify(data));
    },
    async logOut() {
      await this.setUser(null);
    },
    setUser(user) {
      this.user = user;
      // console.log(this.user);
    },
    getUser() {
      // return JSON.parse(this.user);
      return this.user;
    },
    // eslint-disable-next-line no-empty-pattern
    /*async deleteUser(id) {
      await axios.delete(`user/${id}`);
    },*/
  },
});
