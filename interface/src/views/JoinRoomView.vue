<template>
  <w-card class="card" title="Rooms" title-class="blue-light5--bg">
    <ul v-for="i in rooms" v-bind:key="i" class="ma2 member-list">
      <li>
        {{ i.code }}
        <span
          ><w-button
            @click="join_room(i.code)"
            class="join"
            bg-color="success"
            >Join</w-button
          ></span
        >
      </li>
    </ul>
  </w-card>
</template>

<script>
import { onBeforeMount, ref } from "vue";
import { useRouter } from 'vue-router';

export default {
  name: "JoinRoom",

  setup() {
    const rooms = ref([]);
    const router = useRouter();

    onBeforeMount(async () => {
      try {
        const response = await fetch("http://localhost:8000/rooms/");
        const return_data = await response.json();

        for (let key in return_data) {
          rooms.value.push(return_data[key]);
          console.log(return_data[key]);
        }
        console.log(return_data);
      } catch (error) {
        console.log(error);
      }
    });

    async function join_room(code) {
      try {
        const resposne = await fetch(
          `http://localhost:8000/rooms/room/join/${code}/`,
          {
            method: "PUT",
            headers: {
              Authorization: `Token ${localStorage.getItem("auth_token")}`,
              "Content-Type": "application/json; charset=UTF-8",
            },
          }
        );
        const return_data = await response.json();
        console.log(return_data);
      } catch (error) {
        console.log(error);
      }
      router.push('/')
    }

    return { rooms, join_room };
  },
};
</script>

<style scoped>
.card {
  position: relative;
  margin: 70px 35em;
  background: #fcfcfc;
  padding-bottom: 15em;
}
ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}
ul li {
  padding: 8px;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: block;
  position: relative;
  font-size: 1em;
}

ul li:hover {
  background-color: #eee;
}

.join {
  position: absolute;
  right: 5px;
}
</style>
