<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';

const users = ref([]);
const loading = ref(false);

async function fetchUsers() {
  loading.value = true;
  const response = await axios.get('/api/users/');
  users.value = response.data;
  loading.value = false;
}

onBeforeMount(async () => {
  await fetchUsers();
});
</script>

<template>
  <div class="container-fluid">
    <div v-if="loading">Loading users...</div>
    <div v-else>
      <div v-for="user in users" class="user-item" :key="user.id">
        <span><b>Username:</b> {{ user.username }}</span>
        <span><b>First Name:</b> {{ user.first_name }}</span>
        <span><b>Last Name:</b> {{ user.last_name }}</span>
        <span><b>Email:</b> {{ user.email }}</span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.user-item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
