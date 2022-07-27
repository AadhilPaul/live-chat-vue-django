<template>
  <div class="signin">
    <w-card class="card">
      <p class="title2">Log In</p>
      <w-divider class="mb6"></w-divider>
      <w-form>
        <w-grid rows="2" gap="4">
          <w-input
            :validators="[validators.required]"
            required
            label="Username*"
          ></w-input>
          <w-input
            :validators="[validators.required]"
            required
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

<script>
export default {
  name: "LoginView",
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
</style>
