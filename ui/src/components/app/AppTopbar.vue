<template>
<!--  <div class="layout-topbar">

    <div class="col-12 mt-4">
      <Menubar :model="nestedMenuitems">
        &lt;!&ndash;					<template #end>
                    <span class="p-input-icon-left">
                      <i class="pi pi-search" />
                      <InputText type="text" placeholder="Search" />
                    </span>
                  </template>&ndash;&gt;
      </Menubar>
    </div>

  </div>-->
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

    <ul class="layout-topbar-menu hidden lg:flex origin-top">
      <li>
        <button class="p-link layout-topbar-button" @click="logout">
          <i class="pi pi-lock"></i>
          <span>Logout</span>
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import { useUsersStore } from "@/stores/user";

export default {
  data(){
    return {
       nestedMenuitems: [
					{
						label:'Customers',
						icon:'pi pi-fw pi-table',
						items:[
							{
								label:'New',
								icon:'pi pi-fw pi-user-plus',
								items:[
									{
										label:'Customer',
										icon:'pi pi-fw pi-plus'
									},
									{
										label:'Duplicate',
										icon:'pi pi-fw pi-copy'
									},

								]
							},
							{
								label:'Edit',
								icon:'pi pi-fw pi-user-edit'
							}
						]
					},
					{
						label:'Orders',
						icon:'pi pi-fw pi-shopping-cart',
						items:[
							{
								label:'View',
								icon:'pi pi-fw pi-list'
							},
							{
								label:'Search',
								icon:'pi pi-fw pi-search'
							},

						]
					},
					{
						label:'Shipments',
						icon:'pi pi-fw pi-envelope',
						items:[
							{
								label:'Tracker',
								icon:'pi pi-fw pi-compass'

							},
							{
								label:'Map',
								icon:'pi pi-fw pi-map-marker'

							},
							{
								label:'Manage',
								icon:'pi pi-fw pi-pencil'
							}
						]
					},
					{
						label:'Profile',
						icon:'pi pi-fw pi-user',
						items:[
							{
								label:'Settings',
								icon:'pi pi-fw pi-cog'
							},
							{
								label:'Billing',
								icon:'pi pi-fw pi-file'
							}
						]
					},
					{
						label:'Quit',
						icon:'pi pi-fw pi-sign-out'
					}
				],
    };
  },
  setup() {
    const userStore = useUsersStore();

    return {
      userStore,
    };
  },
  methods: {
    onMenuToggle(event) {
      this.$emit("menu-toggle", event);
    },
    logo() {
      return this.$appState.darkTheme
        ? "images/logo-white.png"
        : "images/logo.png";
    },
    logout() {
      this.userStore.logOut();
      this.$router.push("/");
    },
  },
  computed: {
    darkTheme() {
      return this.$appState.darkTheme;
    },
  },
};
</script>
