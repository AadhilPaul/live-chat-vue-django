<template>
  <h3>Hleo, im under da water prop: {{ members }}</h3>
</template>

<script>
export default {
  name: "InRoom",
  props: ["members"],
  setup(props) {
    console.log(props.members);
  },
};
</script>

<style></style>
