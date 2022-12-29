<template>
  <div class="layout-topbar">
    <button
      class="p-link layout-menu-button layout-topbar-button"
      @click="onMenuToggle"
    >
      <i class="pi pi-th-large"></i>
    </button>

    <router-link to="/" class="layout-topbar-logo">
      <span>Bima Insure</span>
      <!--      <img alt="Logo" :src="logo()" />-->
    </router-link>
  </div>
</template>

<script>
export default {
  methods: {
    onMenuToggle(event) {
      this.$emit("menu-toggle", event);
    },
    logo() {
      return this.$appState.darkTheme
        ? "images/logo-white.png"
        : "images/logo.png";
    },
  },
  computed: {
    darkTheme() {
      return this.$appState.darkTheme;
    },
  },
};
</script>
