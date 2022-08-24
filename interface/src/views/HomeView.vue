<template>
  <div class="main">
    <div v-if="authenticated">
      <div v-if="in_room">
        <InRoom :members="members" :code="code" :host="host" :user_id="user_id"></InRoom>
      </div>
      <div v-else>
        <Authenticated></Authenticated>
      </div>
    </div>
    <div v-else>
      <UnAunthenticated></UnAunthenticated>
    </div>
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
    const code = ref("");
    const host = ref("");
    const user_id = ref("");

    onBeforeMount(async () => {
      authenticated.value = "auth_token" in localStorage;

      try {
        const response = await fetch("http://localhost:8000/users/user/detail/", {
          method: "GET",
          headers: {
            Authorization: `Token ${localStorage.getItem("auth_token")}`,
            "Content-Type": "application/json; charset=UTF-8",
          },
        });
        const return_data = await response.json();
        user_id.value = return_data['id']
      } catch(error) {
        console.log(error)
      }

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
        code.value = return_data["code"];
        members.value = return_data["member"];
        host.value = return_data["host"];
      } catch (error) {
        console.error(error);
      }
    });
    const context = { in_room, authenticated, members, code, host, user_id };
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
