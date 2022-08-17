<template>
  <div class="main">
    <w-card class="card">
      <div v-if="authenticated">
        <div v-if="in_room">
          <InRoom :members="members"></InRoom>
        </div>
        <div v-else>
          <Authenticated></Authenticated>
        </div>
      </div>
      <div v-else>
        <UnAunthenticated></UnAunthenticated>
      </div>
    </w-card>
  </div>
</template>

<script>
import { onBeforeMount, ref } from "vue";
import Authenticated from "../components/Authenticated.vue";
import UnAunthenticated from "../components/UnAunthenticated.vue";
import InRoom from "../components/InRoom.vue";

export default {
  name: "HomeView",
  components: { Authenticated, UnAunthenticated, InRoom },
  setup() {
    let authenticated = ref(false);
    let in_room = ref(false);
    const members = ref();

    onBeforeMount(async () => {
      authenticated.value = "auth_token" in localStorage;

      try {
        const response = await fetch("http://localhost:8000/rooms/ifroom/", {
          method: "GET",
          headers: {
            Authorization: `Token ${localStorage.getItem("auth_token")}`,
            "Content-Type": "application/json; charset=UTF-8",
          },
        });
        if (response.status === 200) in_room.value = true;
        const return_data = await response.json();
        console.log(return_data);
        members.value = return_data["member"];
      } catch (error) {
        console.error(error);
      }
    });
    const context = { in_room, authenticated, members };
    return context;
  },
};
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
