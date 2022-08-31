<template>
  <w-card class="card">
    <p class="title2">Join Or Create a Room</p>
    <w-divider class="my6"></w-divider>
    <w-grid columns="2" gap="4">
      <w-button @click="create_room()" lg bg-color="success">Create A Room</w-button>
      <w-button route="/joinroom" lg bg-color="error">Join A Room</w-button>
    </w-grid>
  </w-card>
</template>

<script>
export default {
  name: "Authenticated",
  setup() {
    async function create_room() {
      try {
        const response = await fetch(
          "http://localhost:8000/rooms/room/create/",
          {
            method: "POST",
            headers: {
              Authorization: `Token ${localStorage.getItem("auth_token")}`,
              "Content-Type": "application/json; charset=UTF-8",
            },
          }
        );
      } catch (error) {
        console.log(error);
      }
      window.location.reload("/");
    }

    return { create_room };
  },
};
</script>

<style scoped>
.card {
  margin: 50px 35em;
  background: #fcfcfc;
  padding: 40px;
}
</style>
