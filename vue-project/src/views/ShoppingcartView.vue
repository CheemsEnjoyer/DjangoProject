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

const selectedUserId = ref('');

const shoppingcartsToAdd = ref({});
const shoppingcartsToEdit = ref({});

const customers = ref([]);
const shoppingcarts = ref([]);
const users = ref([]);

const loading = ref(false);

const shoppingcartsById = computed(() => {
  return _.keyBy(shoppingcarts.value, (x) => x.id);
});

async function fetchUsers() {
  try {
    const response = await axios.get('/api/user/all/');
    users.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке пользователей:", error);
  }
}

async function fetchShoppingcarts() {
  loading.value = true;
  let url = '/api/shoppingcarts/';
  if (is_superuser.value && selectedUserId.value) {
    url += `?user_id=${selectedUserId.value}`;
  }
  const r = await axios.get(url);
  shoppingcarts.value = r.data;
  loading.value = false;
}


async function onShoppingcartAdd() {
  await axios.post('/api/shoppingcarts/', {
    ...shoppingcartsToAdd.value,
  });
  await fetchShoppingcarts();
}

const shoppingCartUser = computed(() => {
  return shoppingcarts.value?.user?.username || 'Неизвестный пользователь';
});

async function onRemoveClick(shoppingcart) {
  await axios.delete(`/api/shoppingcarts/${shoppingcart.id}/`);
  await fetchShoppingcarts();
}

async function onShoppingcartEditClick(shoppingcart) {
  shoppingcartsToEdit.value = { ...shoppingcart };
}

async function onUpdateShoppingcart() {
  await axios.put(`/api/shoppingcarts/${shoppingcartsToEdit.value.id}/`, {
    ...shoppingcartsToEdit.value,
  });
  await fetchShoppingcarts();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchUsers();
  await fetchShoppingcarts();
});
</script>

<template>
  <div
    class="modal fade"
    id="editShoppingcartModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Корзины</h5>
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
                <input type="number" class="form-control" v-model="shoppingcartsToEdit.sum" required />
                <label for="floatingInput">Сумма</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="shoppingcartsToEdit.user_id" required>
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
            @click="onUpdateShoppingcart"
            data-bs-dismiss="modal">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent.stop="onShoppingcartAdd">
      <!-- <div class="row">
        <div class="col">
          <div class="form-floating mb-3" style="margin-top: 10px;">
            <input type="number" class="form-control" v-model="shoppingcartsToAdd.sum" required />
            <label for="floatingInput">Сумма</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-floating mb-3" style="margin-top: 10px">
            <select class="form-select" v-model="shoppingcartsToAdd.user_id" required>
              <option v-for="u in users" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Покупатель</label>
          </div>
        </div>
        <div class="col-auto" style="margin-top: 10px">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div> -->
    </form>
    <div v-if="is_auth">
      <h5>
        Покупатель: {{ username }} 
        <span v-if="is_superuser">(Администратор)</span>
      </h5>
      <ul v-if="shoppingcarts && shoppingcarts.productshoppingcart_set">
        <li v-for="item in shoppingcarts.productshoppingcart_set" :key="item.id">
          {{ item.product.name }} - {{ item.quantity }} шт. - {{ item.product_cost }} ₽
          <button class="btn btn-danger btn-sm" @click="removeProductFromCart(item.id)">
            <i class="bi bi-x"></i>
          </button>
        </li>
      </ul>
      <strong v-if="shoppingcarts">Общая сумма: {{ shoppingcarts.total }} ₽</strong>
    </div>

    <div v-else>
      <p>Вы не авторизованы. Пожалуйста, войдите в систему.</p>
    </div>
    
    
  </div>
</template>

<style lang="scss" scoped>
.shoppingcart_item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
