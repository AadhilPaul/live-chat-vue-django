<template>
  <div class="mt20">
    <h1>Hello, This is the Home page</h1>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>

<style scoped>
.home {
  margin-top: 50px
}
</style>
