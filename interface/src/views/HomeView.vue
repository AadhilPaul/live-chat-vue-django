<template>
  <div class="main">
    <w-card class="card">
      <div v-if="authenticated">
        <p class="title2">Join Or Create a Room</p>
        <w-divider class="my6"></w-divider>
        <w-grid columns="2" gap="4">
          <w-button bg-color="success">Create A Room</w-button>
          <w-button bg-color="error">Join A Room</w-button>
        </w-grid>
      </div>
      <div v-else>
        <p class="title2">Log In to Create or Join a Room</p>
        <br/>
        <small><a href="/login">Login with username and password?</a></small>
      </div>
    </w-card>
  </div>
</template>

<script setup>
// @ is an alias to /src
import { onMounted, ref, watchEffect } from "vue";

let authenticated = ref(false);

watchEffect(() => {
  const auth_token = localStorage.getItem("auth_token");
  authenticated.value = "auth_token" in localStorage;
  console.log("watchEffect hook: ", authenticated.value);
});

onMounted(() => {
  authenticated.value = "auth_token" in localStorage;
  console.log(authenticated.value);
});
</script>

<style scoped>
.card {
  margin: 50px 35em;
  background: #fcfcfc;
  padding: 40px;
}

a:hover {
  text-decoration: underline;
}
</style>
