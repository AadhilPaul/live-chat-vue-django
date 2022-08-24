<template>
  <w-card class="card">
    <p class="title2">Join Or Create a Room</p>
    <w-divider class="my6"></w-divider>
    <w-grid columns="2" gap="4">
      <w-button lg bg-color="success">Create A Room</w-button>
      <w-button lg bg-color="error">Join A Room</w-button>
    </w-grid>
  </w-card>
</template>

<script>
export default {
  name: "Authenticated",
};
</script>

<style scoped>
.card {
  margin: 50px 35em;
  background: #fcfcfc;
  padding: 40px;
}
</style>
