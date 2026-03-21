<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <n-message-provider>
    <RouterView />
  </n-message-provider>
</template>

<style>
#app {
  min-height: 100vh;
  background-color: var(--bg-secondary);
}
</style>
