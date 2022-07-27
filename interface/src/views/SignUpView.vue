<template>
  <div class="signin">
    <w-card class="card">
      <p class="title2">Sign Up</p>
      <w-divider class="mb6"></w-divider>
      <w-form>
        <w-grid rows="2" gap="4">
          <w-grid columns="2" gap="2">
            <w-input required label="First Name"></w-input>
            <w-input required label="Last Name"></w-input>
          </w-grid>
          <w-input
            :validators="[validators.required]"
            required
            label="Username*"
          ></w-input>
          <w-input
            :validators="[validators.required]"
            required
            label="Email Address*"
          ></w-input>
          <w-input
            :validators="[validators.required]"
            required
            label="Password*"
          ></w-input>
          <w-input
            :validators="[validators.required]"
            required
            label="Confirm Password*"
          ></w-input>
        </w-grid>
        <div class="text-right mt6">
          <w-button type="submit" bg-color="primary"
            >Create an Account</w-button
          >
        </div>
      </w-form>
      <small>Already have an account? <a href="/login">Login</a></small>
    </w-card>
  </div>
</template>

<script>
export default {
  name: "SignUpView",
  components: {},
  data: () => ({
    valid: null,
    validators: {
      required: (value) => !!value || "This field is required",
    },
  }),
};
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
    color: gray
}
</style>
