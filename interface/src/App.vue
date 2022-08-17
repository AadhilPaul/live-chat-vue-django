<template>
  <w-app>
    <w-toolbar fixed bg-color="blue-light5" color="blue-dark3">
      <a class="title2" href="/">Live Chat</a>
      <div class="spacer"></div>
      <div v-if="authenticated">
        <w-button @click="logout" id="button" class="ma1" bg-color="primary" lg>
          Logout
        </w-button>
      </div>
      <div v-else>
        <w-button id="button" route="/signup" class="ma1" bg-color="primary" lg>
          Sign Up
        </w-button>
        <w-button
          id="button"
          route="/login"
          class="ma1"
          color="primary"
          outline
          lg
        >
          Log In
        </w-button>
      </div>
    </w-toolbar>
    <router-view />
  </w-app>
</template>

<script>
import { onMounted, ref } from "vue";

export default {
  name: "App",
  setup() {
    let authenticated = ref(false);

    onMounted(() => {
      if ("auth_token" in localStorage) authenticated.value = true;
    });

    async function logout() {
      console.log(localStorage.getItem("auth_token"));
      try {
        const response = await fetch(
          "http://localhost:8000/users/token/logout/",
          {
            method: "POST",
            headers: {
              Authorization: `Token ${localStorage.getItem("auth_token")}`,
              "Content-Type": "application/json; charset=UTF-8",
            },
          }
        );
        const return_data = await response.json();
      } catch (error) {
        console.log("ERROR: ", error);
      }

      localStorage.removeItem("auth_token");
      authenticated.value = false;
      window.location.reload();
    }

    const context = {authenticated, logout}
    return context;
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#button {
  font-size: 0.9rem;
}

.main {
  margin-top: 70px;
}

[v-cloak] {
  display: none;
}

a {
  color: rgb(32, 107, 205);
}
</style>
