<template>
  <p class="this-needs-to-be-here-idkwhy"></p>
  <w-card class="card" :title="code" title-class="blue-light5--bg">
    <w-menu left align-top>
      <template #activator="{ on }">
        <w-button
          v-on="on"
          class="mr3 edit"
          icon="mdi mdi-cog-outline"
        ></w-button>
      </template>
      <w-form @submit="change_code">
        <w-input
          label-position="right"
          v-model="new_code"
          outline
          placeholder="Change room code..."
          :validators="[code_length_validation, not_duplicate]"
        >
          <w-button type="submit" class="ma1">Submit</w-button>
        </w-input>
      </w-form>
    </w-menu>
    <w-button @click="leave_room()" icon="mdi mdi-exit-to-app"></w-button>
    <w-menu right align-top>
      <template #activator="{ on }">
        <w-button
          v-on="on"
          class="mr3 members"
          icon="mdi mdi-account-outline"
        ></w-button>
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
      <w-button type="submit" class="ma1">Send</w-button>
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
    const new_code = ref("");
    let valids = {
      length: true,
      not_duplicate: true,
    };

    async function not_duplicate(value) {
      if (value.length >= 6) { // no need for try/catch, just a get request
        const response = await fetch("http://localhost:8000/rooms/");
        const return_data = await response.json();
        for (let key in return_data) {
          for (let _ in return_data[key]) {
            if (value === return_data[key]["code"]) {
              valids.not_duplicate = false;
              return "This Code already exists.";
            }

            valids.not_duplicate = !(value === return_data[key]["code"]);
          }
        }
      }
    }

    async function leave_room() {
      try {
        const response = await fetch(
          `http://localhost:8000/rooms/room/leave/${props.code}/`,
          {
            method: "PUT",
            headers: {
              Authorization: `Token ${localStorage.getItem("auth_token")}`,
              "Content-Type": "application/json; charset=UTF-8",
            },
          }
        );
      } catch (error) {
        console.log(error);
      }
      window.location.reload('/')
    }

    function code_length_validation(value) {
      valids.length = value.length >= 6;
      return value.length >= 6 || "Code must be at least 6 characters";
    }

    function validate() {
      console.log("keys, ", Object.values(valids));
      console.log("FORM", new_code._rawValue);
      if (Object.values(valids).includes(false)) return false;
      return true;
    }

    async function change_code() {
      console.log("validation: ", validate());
      if (validate()) {
        try {
          const response = await fetch(
            `http://localhost:8000/rooms/room/update/${props.code}/`,
            {
              method: "PUT",
              headers: {
                Authorization: `Token ${localStorage.getItem("auth_token")}`,
                "Content-Type": "application/json; charset=UTF-8",
              },
              body: JSON.stringify({ code: new_code._rawValue }),
            }
          );
          if (response.status == 200) window.location.reload();
          const return_data = await response.json();
        } catch (error) {
          console.log(error);
        }
      }
    }

    async function kick(id, index) {
      if (id == props.host) {
        this.$waveui.notify(
          "You can't kick yourself from your own room.",
          "error",
          0
        );
        return;
      }
      if (index == 0) props.members.shift();
      props.members.splice(index, index);
      try {
        const response = await fetch(
          `http://localhost:8000/rooms/room/kick/${id}/${props.code}/`,
          {
            method: "PUT",
            headers: {
              Authorization: `Token ${localStorage.getItem("auth_token")}`,
              "Content-Type": "application/json; charset=UTF-8",
            },
          }
        );
      } catch (error) {
        console.log(error);
      }
    }

    const context = {
      leave_room,
      members,
      kick,
      not_duplicate,
      code_length_validation,
      new_code,
      change_code,
    };
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

.edit {
  position: absolute;
  right: 2.5em;
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
