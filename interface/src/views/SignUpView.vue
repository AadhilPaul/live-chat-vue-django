<template>
  <div class="signin">
    <w-card class="card">
      <p class="title2">Sign Up</p>
      <w-divider class="mb6"></w-divider>
      <w-form @submit="submitData">
        <w-grid rows="2" gap="4">
          <w-grid columns="2" gap="2">
            <w-input
              v-model="form.first_name"
              required
              label="First Name (Optional)"
            ></w-input>
            <w-input
              v-model="form.last_name"
              required
              label="Last Name (Optional)"
            ></w-input>
          </w-grid>
          <w-input
            v-model="form.username"
            autoFocus
            required
            label="Username*"
            :validators="[required, username_validation]"
          ></w-input>
          <w-input
            v-model="form.email"
            type="email"
            required
            label="Email Address*"
            :validators="[required, email_validation]"
          ></w-input>
          <w-input
            v-model="form.password"
            type="password"
            required
            label="Password*"
            :validators="[required, password_validation]"
          ></w-input>
          <ul class="caption">
            <li>Password cannot be too common</li>
            <li>Password must have at least 8 characters</li>
            <li>Password cannot be entirely numeric</li>
          </ul>
          <w-input
            v-model="form.re_password"
            type="password"
            required
            label="Confirm Password*"
            :validators="[required, matching_passwords]"
          ></w-input>
        </w-grid>
        <div class="text-right mt6">
          <w-button type="submit"> Create an Account </w-button>
        </div>
      </w-form>
      <small>Already have an account? <a href="/login">Login</a></small>
    </w-card>
  </div>
</template>

<script setup>
import { ref } from "vue";

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  password: "",
  re_password: "",
});

let valids = {
  no_blank: true,
  valid_username: true,
  valid_email: true,
  valid_password: true,
  matching_password: true,
};

function required(value) {
  return !!value || "This field is required.";
}

// username validation (can't  have spaces)
async function username_validation(value) {
  const username_regex = /^[a-zA-Z0-9$@.+_]+$/;

  valids.valid_username = username_regex.test(value);
  const response = await fetch("http://localhost:8000/users/users/");
  const return_data = await response.json();
  for (let key in return_data) {
    for (let _ in return_data[key]) {
      // i used an underscore because we never need to use that variable again.
      if (value === return_data[key]["username"]) {
        valids.valid_username = false;
        return "A User with this username already exists";
      }
    }
  }
  if (!username_regex.test(value)) {
    valids.valid_username = username_regex.test(value);
    return "150 characters or fewer. Letters, digits and @/./+/_ only.";
  }
}

async function password_validation(value) {
  const only_num = /^[0-9]+$/;
  if (only_num.test(value)) {
    return "Passwords can't be entirely numeric";
  }
  if (!only_num.test(value) && value.length > 8) {
    const response = await fetch(
      "http://localhost:8000/users/password_validator/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json; charset=UTF-8" },
        body: JSON.stringify(form._rawValue),
      }
    );

    const return_data = await response.json();
    if (return_data["similar"]) {
      valids.valid_password = false;
      return return_data["similar"];
    }
    if (return_data["password"]) {
      valids.valid_password = false;
      return return_data["password"][0];
    }
    valids.valid_password = true;
  }
  if (!(value.length > 8)) {
    valids.valid_password = value.length > 8;
    return "Password must be at least 8 characters";
  }
}

// password and confirm passwords are same
function matching_passwords(value) {
  valids.matching_password =
    form._rawValue["password"] === form._rawValue["re_password"];
  return (
    form._rawValue["password"] === form._rawValue["re_password"] ||
    "Passwords are not matching"
  );
}

// email validation.
async function email_validation(value) {
  const email_regex =
    /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

  valids.valid_email = email_regex.test(value);
  const response = await fetch("http://localhost:8000/users/users/");
  const return_data = await response.json();
  for (let key in return_data) {
    for (let _ in return_data[key]) {
      // i used an underscore because we never need to use that variable again.
      if (value === return_data[key]["email"]) {
        valids.valid_email = false;
        return "A User with this email already exists";
      }
    }
  }

  if (!email_regex.test(value)) {
    valids.valid_email = email_regex.test(value);
    return "Must be a valid email address";
  }
}

// see if all inputs are valid.
function validate() {
  console.log("keys, ", Object.values(valids));
  console.log("FORM", form._rawValue);

  // check if they are empty except the optional ones
  for (let key in form._rawValue) {
    if (!form._rawValue[key]) valids.no_blank = false;
    if (key === "first_name" || key === "last_name") valids.no_blank = true;
  }

  // check if all validations are true
  if (Object.values(valids).includes(false)) return false;
  return true;
}

async function submitData() {
  console.log("validation: ", validate());
  if (validate()) {
    const response = await fetch("http://localhost:8000/users/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=UTF-8" },
      body: JSON.stringify(form._rawValue),
    });

    const return_data = await response.json();

    console.log(return_data);
  }
}
</script>

<style>
.signin {
  margin-top: 3rem;
}
.card {
  margin: 50px 30em;
  background: #fcfcfc;
  padding: 40px;
}
a {
  color: rgb(32, 107, 205);
  text-decoration: none;
}
small {
  color: gray;
}
</style>
