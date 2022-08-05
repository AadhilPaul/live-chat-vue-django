<template>
  <div class="login">
    <w-card class="card">
      <p class="title2">Log In</p>
      <w-divider class="mb6"></w-divider>
      <w-form @submit="submitData">
        <w-grid rows="2" gap="4">
          <w-input
            :validators="[required, username_validation]"
            v-model="form.username"
            required
            label="Username*"
          ></w-input>
          <w-input
            :validators="[required, password_validation]"
            v-model="form.password"
            required
            type="password"
            label="Password*"
          ></w-input>
          <a class="caption" href="#">Forgot Password?</a>
        </w-grid>
        <div class="text-right mt6">
          <w-button type="submit" bg-color="primary">Log In</w-button>
        </div>
        <small>Don't have an account? <a href="/signup">Register</a></small>
      </w-form>
    </w-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";



const form = ref({
  username: "",
  password: "",
});

let valids = {
  no_blank: true,
  valid_username: true,
  valid_password: true,
};

function required(value) {
  return !!value || "This field is required";
}

async function password_validation(value) {
  valids.valid_password = value.length >= 8;

  if (value.length >= 8) {
    const response = await fetch("http://localhost:8000/users/token/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=UTF-8" },
      body: JSON.stringify(form._rawValue),
    });

    const return_data = await response.json();
    valids.valid_password = !return_data.hasOwnProperty("non_field_errors");
    if (return_data["non_field_errors"]) {
      return "Wrong Password!";
    }
  }
  return value.length >= 8 || "Password must be at least 8 characters";
}

async function username_validation(value) {
  const username_regex = /^[a-zA-Z0-9$@.+_]+$/;

  valids.valid_username = username_regex.test(value);
  const response = await fetch("http://localhost:8000/users/users/");
  const return_data = await response.json();
  const list_of_usernames = [];
  for (let key in return_data)
    list_of_usernames.push(return_data[key]["username"]);

  // see if value is in the list of usernames
  if (!list_of_usernames.includes(value)) {
    valids.valid_username = false;
    return "Invalid Username";
  }
  if (!username_regex.test(value)) {
    valids.valid_username = username_regex.test(value);
    return "150 characters or fewer. Letters, digits and @/./+/_ only.";
  }
}

function validate() {
  console.log("keys, ", Object.values(valids));
  console.log("FORM", form._rawValue);

  // check if they are empty except the optional ones
  for (let key in form._rawValue) {
    valids.no_blank = !!form._rawValue[key];
    console.log(!!form._rawValue[key]);
  }

  // check if all validations are true
  if (Object.values(valids).includes(false)) return false;
  return true;
}

async function submitData() {
  console.log("validation: ", validate());
  if (validate()) {
    const response = await fetch("http://localhost:8000/users/token/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=UTF-8" },
      body: JSON.stringify(form._rawValue),
    });

    const return_data = await response.json();
    if (return_data["auth_token"]) {
      localStorage.setItem("auth_token", return_data["auth_token"]);
      window.location.href = "/"
    }
  }
}
</script>

<style scoped>
.login {
  margin-top: 3em;
}
.card {
  margin: 50px 35em;
  background: #fcfcfc;
  padding: 40px;
}

a {
  color: rgb(32, 107, 205);
}
small {
  color: gray;
}
</style>
