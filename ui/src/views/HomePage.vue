<template>
  <Toast position="top-right" />
  <div class="grid">
    <div class="col-12">
      <div class="grid grid-nogutter text-800">
        <div
          class="col-12 md:col-6 p-6 text-center md:text-left flex align-items-center"
        >
          <section>
            <div>
              <span class="text-5xl font-bold mb-1"
                >Weather Crop Index Insurance</span
              >
            </div>

            <p class="mt-5">
              The Leading weather index insurance platform in South Africa
            </p>

            <div class="mt-6">
              <span class="text-2xl font-bold mb-1">Features</span>
            </div>

            <div class="flex flex-column mt-5">
              <p>
                <i class="pi pi-check-circle text-green-800 mr-2"></i>
                Blockchain Powered
              </p>
              <p>
                <i class="pi pi-check-circle text-green-800 mr-2"></i> Reliable
              </p>
              <p>
                <i class="pi pi-check-circle text-green-800 mr-2"></i> Low Cost
              </p>
            </div>

            <div>
              <Dialog
                header="Member Registration"
                v-model:visible="display"
                :breakpoints="{ '960px': '75vw' }"
                :style="{ width: '30vw' }"
                :modal="true"
              >
                <div class="p-fluid">
                  <div class="col-12">
                    <div class="p-inputgroup">
                      <span class="p-inputgroup-addon">
                        <i class="pi pi-user"></i>
                      </span>
                      <InputText
                        placeholder="First Name"
                        v-model="firstname"
                      />
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="p-inputgroup">
                      <span class="p-inputgroup-addon">
                        <i class="pi pi-user"></i>
                      </span>
                      <InputText
                        placeholder="Surname"
                        v-model="surname"
                      />
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="p-inputgroup">
                      <span class="p-inputgroup-addon">
                        <i class="pi pi-map"></i>
                      </span>
                      <InputText
                        placeholder="Farm Name"
                        v-model="farmname"
                      />
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="p-inputgroup">
                      <span class="p-inputgroup-addon">
                        <i class="pi pi-map-marker"></i>
                      </span>
                      <InputText
                        placeholder="Farm Address"
                        v-model="farmaddress"
                      />
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="p-inputgroup">
                      <span class="p-inputgroup-addon">
                        <i class="pi pi-inbox"></i>
                      </span>
                      <InputText
                        placeholder="Email"
                        type="email"
                        v-model="email"
                      />
                    </div>
                  </div>
                </div>

                <template #footer>
                  <Button
                    label="Register"
                    @click="register"
                    icon="pi pi-check"
                    class="p-button-outlined"
                  />
                </template>
              </Dialog>
              <Button
                class="mt-5"
                label="Become A Member"
                icon="pi pi-external-link"
                style="width: auto"
                @click="open"
              />

              <transition-group name="p-message" tag="div">
                <Message
                  v-for="msg of message"
                  :severity="msg.severity"
                  :key="msg.content"
                  >{{ msg.content }}</Message
                >
              </transition-group>
            </div>
          </section>
        </div>
        <div
          class="col-12 md:col-6 overflow-hidden flex align-items-center justify-content-center"
        >
          <img
            :src="heroImage()"
            alt="Image"
            class="md:h-25rem md:w-fit"
            style="width: 100%"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      display: false,
      firstname: null,
      surname: null,
      farmname: null,
      farmaddress: null,
      email: null,
      memberid: null,
      dataLoaded: false,
      message: [],
    };
  },
  methods: {
    heroImage() {
      return this.$appState.darkTheme ? "images/img_1.png" : "images/img_1.png";
    },

    open() {
      this.display = true;
    },
    close() {
      this.display = false;
    },
    successToast(s, d) {
      this.$toast.add({
        severity: "success",
        summary: s,
        detail: d,
        life: 4000,
      });
    },
    errorToast(s, d) {
      this.$toast.add({
        severity: "error",
        summary: s,
        detail: d,
        life: 3000,
      });
    },

    register() {
      axios
        .post("/register/", {
          firstname: this.firstname,
          surname: this.surname,
          farmname: this.farmname.toLowerCase(),
          farmaddress: this.farmaddress.toLowerCase(),
          email: this.email,
        })
        .then((res) => {
          this.memberid = res.data.memberid;
          this.dataLoaded = true;
          this.successToast(
            "Member Code",
            `Your Membership ID is ${res.data.memberid}`
          );
          this.message = [
            {
              severity: "success",
              detail: "Success ",
              content: `Your Membership ID is ${res.data.memberid}`,
            },
          ];
          this.close();
        })
        .catch((err) => {
          console.log(err.message);
          this.errorToast("Error", "Registration error");
        });
    },
  },
};
</script>

<style scoped></style>
