<template>
  <div class="login">
    <w-card class="card">
      <p class="title2">Log In</p>
      <w-divider class="mb6"></w-divider>
      <w-form >
        <w-grid rows="2" gap="4">
          <div @click="dissmiss_error">
            <w-alert v-if="invalid_credentials" error>
              Invalid Password or Username
            </w-alert>
          </div>
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
          <w-button @click="submit_data" type="submit" bg-color="primary">Log In</w-button>
        </div>
        <small>Don't have an account? <a href="/signup">Register</a></small>
      </w-form>
    </w-card>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
export default {
  name: "LoginView",
  setup() {
    function dissmiss_error() {
      invalid_credentials.value = false;
    }
    const invalid_credentials = ref(false);
    const router = useRouter();

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

      return value.length >= 8 || "Password must be at least 8 characters";
    }

    async function username_validation(value) {
      const username_regex = /^[a-zA-Z0-9$@.+_]+$/;

      valids.valid_username = username_regex.test(value);
      return (
        username_regex.test(value) ||
        "150 charactesr or fewer. Letters, digits and @/./+/_ only"
      );
    }

    function validate() {
      // check if they are empty except the optional ones
      for (let key in form._rawValue) {
        valids.no_blank = !!form._rawValue[key];
      }

      // check if all validations are true
      if (Object.values(valids).includes(false)) return false;
      return true;
    }

    async function submit_data() {
      if (validate()) {
        console.log("FORM: ", form._rawValue)
        const response = await fetch(
          "http://localhost:8000/users/token/login/",
          {
            method: "POST",
            headers: { "Content-Type": "application/json; charset=UTF-8" },
            body: JSON.stringify(form._rawValue),
          }
        );
        if (response.status === 400) {
          invalid_credentials.value = true;
          console.log(invalid_credentials.value);
        }
        const return_data = await response.json();
        if (return_data["auth_token"]) {
          localStorage.setItem("auth_token", return_data["auth_token"]);
          window.location.href = "/";
        }
      }
    }
    const context = {
      dissmiss_error,
      invalid_credentials,
      form,
      required,
      username_validation,
      password_validation,
      submit_data,
    };
    return context;
  },
};
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
