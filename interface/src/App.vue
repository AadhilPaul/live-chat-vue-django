<template>
  <w-app>
    <w-toolbar fixed bg-color="blue-light5" color="blue-dark3">
      <div class="title2">Title</div>
      <div class="spacer"></div>
      <w-button id="button" route="/signup" class="ma1" bg-color="primary" lg>
        Sign Up
      </w-button>
      <w-button id="button" route="/login" class="ma1" color="primary" outline lg>
        Log In
      </w-button>
    </w-toolbar>
    <router-view />
  </w-app>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#button {
  font-size: 0.9rem;
}
</style>
