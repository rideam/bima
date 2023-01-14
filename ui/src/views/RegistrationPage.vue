<template>
  <div
      class="surface-0 flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden"
  >
    <div class="grid justify-content-center p-2 lg:p-0" style="min-width: 80%">
      <div
          class="col-12 xl:col-6"
          style="
          border-radius: 56px;
          padding: 0.3rem;
          background: linear-gradient(
            180deg,
            var(--primary-color),
            rgba(33, 150, 243, 0) 30%
          );
        "
      >
        <div
            class="h-full w-full m-0 py-7 px-4"
            style="
            border-radius: 53px;
            background: linear-gradient(
              180deg,
              var(--surface-50) 38.9%,
              var(--surface-0)
            );
          "
        >
          <div class="text-center mb-5">
            <span class="text-600 text-2xl font-medium">Sign Up</span>
          </div>
          <form @submit.prevent="submit">
            <div class="w-full md:w-10 mx-auto">
              <label
                  for="firstname"
                  class="block text-xl text-900 font-medium mb-2"
              >Full name</label
              >
              <InputText
                  id="name"
                  v-model="name"
                  type="text"
                  class="w-full mb-3"
                  placeholder="Full Name"
                  style="padding: 1rem"
              />
              <label for="email" class="block text-xl text-900 font-medium mb-2"
              >Email</label
              >
              <InputText
                  id="email"
                  v-model="email"
                  type="text"
                  class="w-full mb-3"
                  placeholder="Email"
                  style="padding: 1rem"
              />

              <label
                  for="password1"
                  class="block text-xl text-900 font-medium mb-2"
              >Password</label
              >
              <Password
                  id="password1"
                  v-model="password"
                  placeholder="Password"
                  :toggleMask="true"
                  class="w-full mb-3"
                  inputClass="w-full"
                  inputStyle="padding:1rem"
              ></Password>

              <div class="flex align-items-center justify-content-between mb-5">
                <div class="flex align-items-center">
                  <Checkbox
                      id="rememberme1"
                      v-model="checked"
                      :binary="true"
                      class="mr-2"
                  ></Checkbox>
                  <label for="rememberme1">Remember me</label>
                </div>
                <div>
                  <Button
                      label="Login"
                      class="p-button-text p-button-rounded border-none font-light line-height-2 text-primary"
                      @click="navigate('/login')"
                  ></Button>
                  <Button
                      label="Forgot password?"
                      class="p-button-text p-button-rounded border-none font-light line-height-2 text-primary"
                      @click="navigate('/forgotpassword')"
                  ></Button>
                </div>
              </div>
              <Button
                  label="Register"
                  class="w-full p-3 text-xl"
                  type="submit"
              ></Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { mapActions } from "pinia";
import {useUsersStore} from "@/stores/user";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      checked: false,
    };
  },
  setup() {
    const userStore = useUsersStore();
    return {
      userStore,
    };
  },
  computed: {
    logoColor() {
      if (this.$appState.darkTheme) return "white";
      return "dark";
    },
  },
  methods: {
    navigate(path) {
      this.$router.push(path);
    },
    async submit() {
      const user = {
        fullname: this.name,
        username: this.email,
        password: this.password
      };
      // const user = new FormData();
      // user.append("fullname", this.name);
      // user.append("username", this.email);
      // user.append("password", this.password);
      // user.append("access_level_id", this.access_level_id);
      await this.userStore.register(user);
      await this.$router.push("/");
    },
  },
};
</script>
