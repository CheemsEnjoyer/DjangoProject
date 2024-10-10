<script setup>
import { computed, ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';
import _ from 'lodash';

const ordersToAdd = ref({});
const ordersToEdit = ref({});

const customers = ref([]);
const orders = ref([]);
const users = ref([]);

const loading = ref(false);

const ordersById = computed(() => {
  return _.keyBy(orders.value, (x) => x.id);
});

async function fetchUsers() {
  const r = await axios.get('/api/users/');
  users.value = r.data;
}

async function fetchCustomers() {
  const r = await axios.get('/api/customers/');
  customers.value = r.data;
}

async function fetchOrders() {
  loading.value = true;
  const r = await axios.get('/api/orders/');
  orders.value = r.data;
  loading.value = false;
}

async function onOrdersAdd() {
  await axios.post('/api/orders/', {
    ...ordersToAdd.value,
  });
  await fetchOrders();
}

async function onRemoveClick(order) {
  await axios.delete(`/api/orders/${order.id}/`);
  await fetchOrders(); // переподтягиваю
}

async function onOrderEditClick(order) {
  ordersToEdit.value = { ...order };
}

const STATUS_CHOICES = {
  ordered: 'Оформлен',
  assembling: 'Собирается',
  in_transit: 'В пути',
  arrived: 'Прибыл в пункт доставки',
  picked_up: 'Забран',
};

function getStatusDescription(status) {
  return STATUS_CHOICES[status];
}

async function onUpdateOrder() {
  await axios.put(`/api/orders/${ordersToEdit.value.id}/`, {
    ...ordersToEdit.value,
  });
  await fetchOrders();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchUsers();
  await fetchCustomers();
  await fetchOrders();
});
</script>

<template>
  <div
    class="modal fade"
    id="editOrderModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Заказы</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="ordersToEdit.address" required />
                <label for="floatingInput">Адрес</label>
              </div>
              <div class="form-floating">
                <input type="number" class="form-control" v-model="ordersToEdit.sum" required />
                <label for="floatingInput">Сумма</label>
              </div>
              <div class="form-floating">
                <select class="form-select" v-model="ordersToEdit.status" required>
                  <option disabled value="">Выберите статус</option>
                  <option value="ordered">Оформлен</option>
                  <option value="assembling">Собирается</option>
                  <option value="in_transit">В пути</option>
                  <option value="arrived">Прибыл в пункт доставки</option>
                  <option value="picked_up">Забран</option>
                </select>
                <label for="floatingSelect">Статус</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="ordersToEdit.user_id" required>
                  <option v-for="u in users" :value="u.id">{{ u.username }}</option>
                </select>
                <label for="floatingInput">Покупатель</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button
            type="button"
            class="btn btn-primary"
            @click="onUpdateOrder"
            data-bs-dismiss="modal">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent.stop="onOrdersAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating mb-3" style="margin-top: 10px">
            <input type="text" class="form-control" v-model="ordersToAdd.address" required />
            <label for="floatingInput">Адрес</label>
          </div>
          <div class="form-floating mb-3">
            <input type="number" class="form-control" v-model="ordersToAdd.sum" required />
            <label for="floatingInput">Сумма</label>
          </div>
          <div class="form-floating mb-3">
            <select class="form-select" v-model="ordersToAdd.status" required>
              <option disabled value="">Выберите статус</option>
              <option value="ordered">Оформлен</option>
              <option value="assembling">Собирается</option>
              <option value="in_transit">В пути</option>
              <option value="arrived">Прибыл в пункт доставки</option>
              <option value="picked_up">Забран</option>
            </select>
            <label for="floatingSelect">Статус</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-floating mb-3" style="margin-top: 10px">
            <select class="form-select" v-model="ordersToAdd.user_id" required>
              <option v-for="u in users" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Покупатель</label>
          </div>
        </div>
        <div class="col-auto" style="margin-top: 10px">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>
    <div v-for="item in orders" class="order_item" :key="item.id">
      <span><b>Покупатель:</b> {{ item.user.username }}</span>
      <span><b>Адрес:</b> {{ item.address }}</span>
      <span><b>Сумма:</b> {{ item.sum }}</span>
      <span><b>Статус:</b> {{ getStatusDescription(item.status) }}</span>
      <button
        class="btn btn-info"
        @click="onOrderEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editOrderModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.order_item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto auto;
  gap: 16px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
