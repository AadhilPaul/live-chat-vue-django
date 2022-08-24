<template>
  <p class="this-needs-to-be-here-idkwhy">asdf</p>
  <w-card class="card">
    <!-- <div v-for="i in members" v-bind:key="i" class="ma2" id="member-list">
      <p>{{ i.username }}</p>
      <hr/>
    </div> -->
    <w-menu right align-top>
      <template #activator="{ on }">
        <w-button v-on="on" class="mr3 members" icon="mdi mdi-account">
          Show menu on click
        </w-button>
      </template>
      <ul v-for="i in members" v-bind:key="i" class="ma2 member-list">
        <li class="name">
          {{ i.username }}
          <span v-if="user_id == host"
            ><w-button
              @click="kick(i.id, members.indexOf(i))"
              class="kick"
              bg-color="error"
              >Kick</w-button
            ></span
          >
        </li>
      </ul>
    </w-menu>

    <w-input
      class="mb3 msg"
      label-position="right"
      outline
      placeholder="Type a message here.."
    >
      <w-button class="ma1">Send</w-button>
    </w-input>
  </w-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.min.css";
import { ref } from "vue";

export default {
  name: "InRoom",
  props: ["members", "code", "host", "user_id"],
  setup(props) {
    const members = props.members;
    const cant_kick = ref(false);

    async function kick(id, index) {
      if (id == props.host) {
        cant_kick.value = true;
        this.$waveui.notify("You can't kick yourself from your own room.", "error", 0);
        return;
      }
      if (index == 0) props.members.shift();
      props.members.splice(index, index);
      try {
        const response = await fetch(`http://localhost:8000/rooms/room/kick/${id}/${props.code}/`, {
          method: "PUT",
          headers: {
            Authorization: `Token ${localStorage.getItem("auth_token")}`,
            "Content-Type": "application/json; charset=UTF-8",
          },
        });
      } catch(error) {
        console.log(error);
      }
    }

    const context = { members, kick };
    return context;
  },
};
</script>

<style scoped>
.this-needs-to-be-here-idkwhy {
  display: none;
}

.py12 {
  height: 100%;
}
.mtop {
  margin-top: 10rem;
}
.card {
  position: relative;
  margin: 30px 35em;
  background: #fcfcfc;
  padding-bottom: 15em;
}
.msg {
  position: absolute;
  bottom: 0px;
  width: 97%;
}

.members {
  position: absolute;
  right: 0px;
}

.member-list {
  list-style-type: none;
  margin: 30px 30px;
  background: #fcfcfc;
  position: relative;
}
.name {
  flex-grow: 1;
}
ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}
ul li {
  width: 15em;
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
.kick {
  position: absolute;
  right: 5px;
}
</style>
