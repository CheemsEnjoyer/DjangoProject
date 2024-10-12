<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';

const customersToAdd = ref({});
const customersToEdit = ref({});

const customers = ref([]);
const users = ref([]);
const loading = ref(false);

async function fetchCustomers() {
  loading.value = true;
  const r = await axios.get('/api/customers/');
  customers.value = r.data;
  loading.value = false;
}

async function fetchUsers() {
  const r = await axios.get('/api/users/');
  users.value = r.data;
}

async function onCustomersAdd() {
  await axios.post('/api/customers/', {
    ...customersToAdd.value,
  });
  await fetchCustomers();
}

async function onRemoveClick(customer) {
  await axios.delete(`/api/customers/${customer.id}/`);
  await fetchCustomers();
}

async function onCustomerEditClick(customer) {
  customersToEdit.value = { ...customer };
}

async function onUpdateCustomer() {
  await axios.put(`/api/customers/${customersToEdit.value.id}/`, {
    ...customersToEdit.value,
  });
  await fetchCustomers();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchCustomers();
  await fetchUsers();
});
</script>

<template>
  <div
    class="modal fade"
    id="editCustomerModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование клиента</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss            ="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-3">
            <select class="form-select" v-model="customersToEdit.user_id" required>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingSelect">Пользователь</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button
            type="button"
            class="btn btn-primary"
            @click="onUpdateCustomer"
            data-bs-dismiss="modal">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent.stop="onCustomersAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating mb-3">
            <select class="form-select" v-model="customersToAdd.user_id" required>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingSelect">Пользователь</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить клиента</button>
        </div>
      </div>
    </form>

    <div v-for="item in customers" class="customer-item" :key="item.id">
      <span><b>Пользователь:</b> {{ item.user.username }}</span>
      <button
        class="btn btn-info"
        @click="onCustomerEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editCustomerModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.customer-item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
