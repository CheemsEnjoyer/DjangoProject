<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';

const clientToAdd = ref({ name: '', order: null });
const clientToEdit = ref({});

async function fetchClients() {
  loading.value = true;
  const r = await axios.get('/api/capybuyra');
  console.log(r.data);
  client.value = r.data;
  loading.value = false;
}

async function onLoadClick() {
  fetchClients();
}

async function onClientAdd() {
  await axios.post('/api/capybuyra/', {
    ...clientToAdd.value,
  });
  await fetchClients();
}

async function onRemoveClick(client) {
  await axios.delete(`/api/capybuyra/${client.id}/`);
  await fetchClients(); // переподтягиваю
}

async function onClientEditClick(client) {
  clientToEdit.value = { ...client };
}

async function onUpdateClient() {
  await axios.put(`/api/capybuyra/${clientToEdit.value.id}/`, {
    ...clientToEdit.value,
  });
  await fetchClients();
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
});
</script>

<template>
  <form @submit.prevent.stop="onClientAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="clientToAdd.name" required />
          <label for="floatingInput">Фио</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <select class="form-select" v-model="clientToAdd.order" required>
            <option :value="o.id" v-for="o in Object.values(orders)">{{ o.address }}</option>
          </select>
          <label for="floatingInput">Группа</label>
        </div>
      </div>
      <div class="col-auto">
        <button @click="onClientAdd" class="btn btn-primary">Добавить</button>
      </div>
    </div>

    <div v-for="item in clients" class="client-item">
      <div>{{ item.fio }}</div>
      <div>{{ orders[item.order]?.title }}</div>
      <button class="btn btn-success" @click="onClientEditClick(item)" data-bs-toggle="modal" data-bs-target="#editClientModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <div class="modal fade" id="editClientModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="clientToEdit.name" />
                  <label for="floatingInput">Фио</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="clientToEdit.order">
                    <option :value="o.id" v-for="o in Object.values(orders)">{{ o.address }}</option>
                  </select>
                  <label for="floatingInput">Группа</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateClient">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<style scoped></style>
