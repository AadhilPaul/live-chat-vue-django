<template>
  <div class="main">
    <w-card class="card">
      <div v-if="authenticated">
        <Authenticated></Authenticated>
      </div>
      <div v-else>
        <UnAunthenticated></UnAunthenticated>
      </div>
    </w-card>
  </div>
</template>

<script setup>
import { onMounted, ref, watchEffect } from "vue";
import Authenticated from "../components/Authenticated.vue";
import UnAunthenticated from "../components/UnAunthenticated.vue";

let authenticated = ref(false);

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
