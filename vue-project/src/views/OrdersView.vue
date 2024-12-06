<script setup>
import { computed, ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';
import _ from 'lodash';
import { storeToRefs } from 'pinia';
import useUserProfileStore from "@/stores/userProfileStore";

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser } = storeToRefs(userProfileStore);

const ordersToAdd = ref({});
const ordersToEdit = ref({});

const customers = ref([]);
const orders = ref([]);
const users = ref([]);
const orderStats = ref({});

const loading = ref(false);
const selectedUserId = ref('');
const selectedStatus = ref('');

const ordersById = computed(() => {
  return _.keyBy(orders.value, (x) => x.id);
});

async function fetchUsers() {
  try {
    const response = await axios.get('/api/user/all/');
    users.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке пользователей:", error);
  }
}

async function fetchCustomers() {
  const r = await axios.get('/api/customers/');
  customers.value = r.data;
}

async function fetchOrders() {
  loading.value = true;
  let url = '/api/orders/';
  const params = [];

  if (is_superuser.value && selectedUserId.value) {
    params.push(`user_id=${selectedUserId.value}`);
  }
  if (selectedStatus.value) {
    params.push(`status=${selectedStatus.value}`);
  }

  if (params.length > 0) {
    url += `?${params.join('&')}`;
  }

  const r = await axios.get(url);
  orders.value = r.data;
  loading.value = false;
}


async function fetchOrdersStats() {
  try {
    const response = await axios.get('/api/orders/stats/');
    orderStats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики продуктов:", error);
  }
}

async function onOrdersAdd() {
  const data = { ...ordersToAdd.value };
  delete data.user;
  await axios.post('/api/orders/', data);
  await fetchOrders();
}

async function onRemoveClick(order) {
  await axios.delete(`/api/orders/${order.id}/`);
  await fetchOrders();
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
  const data = { ...ordersToEdit.value };
  delete data.user;
  await axios.put(`/api/orders/${ordersToEdit.value.id}/`, data);
  await fetchOrders();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchUsers();
  await fetchCustomers();
  await fetchOrders();
  await fetchOrdersStats();
  if (is_superuser.value) {
    await fetchUsers();
  }
});
</script>

<template>
  <div v-if="is_superuser" class="form-floating mb-3">
    <select class="form-select" v-model="selectedUserId" @change="fetchOrders">
      <option value="">Все пользователи</option>
      <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
    </select>
    <label for="floatingSelect">Фильтр по пользователю</label>
  </div>

  <div class="form-floating mb-3">
    <select class="form-select" v-model="selectedStatus" @change="fetchOrders">
      <option value="">Все статусы</option>
      <option v-for="(label, value) in STATUS_CHOICES" :key="value" :value="value">
        {{ label }}
      </option>
    </select>
    <label for="statusFilter">Фильтр по статусу</label>
  </div>
  
  <div class="stats-container">
    <h3>Статистика заказов</h3>
    <ul>
      <li>Общее количество заказов: {{ orderStats.count }}</li>
      <li>Средняя сумма заказа: {{ orderStats.avg_sum }}</li>
      <li>Максимальная сумма заказа: {{ orderStats.max_sum }}</li>
      <li>Минимальная сумма заказа: {{ orderStats.min_sum }}</li>
    </ul>
  </div>

  <div
    class="modal fade"
    id="editOrderModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование заказа</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating mb-3">
                <input type="text" class="form-control" v-model="ordersToEdit.address" required />
                <label for="floatingInput">Адрес</label>
              </div>
              <div class="form-floating mb-3">
                <input type="number" class="form-control" v-model="ordersToEdit.sum" required />
                <label for="floatingInput">Сумма</label>
              </div>
              <div class="form-floating mb-3">
                <select class="form-select" v-model="ordersToEdit.status" required>
                  <option disabled value="">Выберите статус</option>
                  <option v-for="(label, value) in STATUS_CHOICES" :value="value">{{ label }}</option>
                </select>
                <label for="floatingSelect">Статус</label>
              </div>
            </div>
            <div class="col-auto" v-if="is_superuser">
              <div class="form-floating mb-3">
                <select class="form-select" v-model="ordersToEdit.user_id" required>
                  <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
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
              <option v-for="(label, value) in STATUS_CHOICES" :value="value">{{ label }}</option>
            </select>
            <label for="floatingSelect">Статус</label>
          </div>
        </div>
        <!-- <div class="col-auto" v-if="is_superuser">
          <div class="form-floating mb-3" style="margin-top: 10px">
            <select class="form-select" v-model="ordersToAdd.user_id" required>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Покупатель</label>
          </div>
        </div> -->
        <div class="col-auto" style="margin-top: 10px" >
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in orders" class="order_item" :key="item.id">
      <span v-if="is_superuser"><b>Покупатель:</b> {{ item.user.username }}</span>
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
  border: 4px solid #d1d1d1;
  border-radius: 8px;
  background-color: #d9c006b6;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto auto auto;
  gap: 16px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-container {
  margin-bottom: 20px;
  border-radius: 8px;
  padding: 10px;
  background-color: #debb3ad4;
  border: 4px solid #ccc;
}

.stats-container h3 {
  margin-top: 0;
}
</style>
