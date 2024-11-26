<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';
import { storeToRefs } from 'pinia';
import useUserProfileStore from "@/stores/userProfileStore";

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser } = storeToRefs(userProfileStore);


const reviewsToAdd = ref({});
const reviewsToEdit = ref({});

const reviews = ref([]);
const products = ref([]);
const users = ref([]);
const loading = ref(false);
const selectedUserId = ref('');

async function fetchReviews() {
  loading.value = true;
  let url = '/api/reviews/';
  
  if (selectedUserId.value) {
    url += `?user_id=${selectedUserId.value}`;
  }

  const r = await axios.get(url);
  reviews.value = r.data;
  loading.value = false;
}

async function fetchProducts() {
  const r = await axios.get('/api/products/');
  products.value = r.data;
}

async function fetchUsers() {
  try {
    const response = await axios.get('/api/user/all');
    users.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке пользователей:", error);
  }
}

async function onReviewsAdd() {
  await axios.post('/api/reviews/', {
    ...reviewsToAdd.value,
  });
  await fetchReviews();
}

async function onRemoveClick(review) {
  await axios.delete(`/api/reviews/${review.id}/`);
  await fetchReviews();
}

async function onReviewEditClick(review) {
  reviewsToEdit.value = { ...review };
}

async function onUpdateReview() {
  await axios.put(`/api/reviews/${reviewsToEdit.value.id}/`, {
    ...reviewsToEdit.value,
  });
  await fetchReviews();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchReviews();
  await fetchProducts();
  await fetchUsers();
  if (is_superuser.value) {
    await fetchUsers();
  }
});
</script>

<template>
  <div class="form-floating mb-3" v-if="is_superuser">
    <select class="form-select" v-model="selectedUserId" @change="fetchReviews">
      <option value="">Все пользователи</option>
      <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
    </select>
    <label for="floatingSelect">Фильтр по пользователю</label>
  </div>

  <div
    class="modal fade"
    id="editReviewModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование отзыва</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-3">
            <textarea class="form-control" v-model="reviewsToEdit.text" required></textarea>
            <label for="floatingInput">Текст</label>
          </div>
          <div class="form-floating mb-3">
            <input
              type="number"
              class="form-control"
              v-model="reviewsToEdit.rating"
              min="1"
              max="5"
              required />
            <label for="floatingInput">Оценка (1-5)</label>
          </div>
          <div class="form-floating mb-3" v-if="is_superuser">
            <select class="form-select" v-model="reviewsToEdit.user_id" required>
              <option v-for="u in users" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Пользователь</label>
          </div>          
          <div class="form-floating mb-3">
            <select class="form-select" v-model="reviewsToEdit.product_id" required>
              <option v-for="p in products" :value="p.id">{{ p.name }}</option>
            </select>
            <label for="floatingInput">Товар</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button
            type="button"
            class="btn btn-primary"
            @click="onUpdateReview"
            data-bs-dismiss="modal">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent.stop="onReviewsAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating mb-3">
            <textarea
              class="form-control"
              v-model="reviewsToAdd.text"
              required
              placeholder="Введите текст отзыва"></textarea>
            <label for="floatingTextarea">Текст отзыва</label>
          </div>
          <div class="form-floating mb-3">
            <input
              type="number"
              class="form-control"
              v-model="reviewsToAdd.rating"
              min="1"
              max="5"
              required
              placeholder="Оценка" />
            <label for="floatingInput">Оценка (1-5)</label>
          </div>
        </div>
        <!-- <div class="col-auto" v-if="is_superuser">
          <div class="form-floating mb-3">
            <select class="form-select" v-model="reviewsToAdd.user_id" required>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Пользователь</label>
          </div>
        </div> -->
        <div class="col-auto">
          <div class="form-floating mb-3">
            <select class="form-select" v-model="reviewsToAdd.product_id" required>
              <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
            <label for="floatingInput">Продукт</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary" type="submit">Добавить отзыв</button>
        </div>
      </div>
    </form>

    <div v-if="!loading && reviews.length" class="mt-4">
      <div v-for="item in reviews" :key="item.id" class="review-item">
        <span v-if="is_superuser"><b>Пользователь:</b> {{ item.user.username }}</span>
        <span><b>Продукт:</b> {{ item.product.name }}</span>
        <span><b>Оценка:</b> {{ item.rating }}</span>
        <span><b>Текст:</b> {{ item.text }}</span>
        <button
          class="btn btn-info"
          @click="onReviewEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editReviewModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.review-item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 4px solid #d1d1d1;
  border-radius: 8px;
  background-color: #d9c006b6;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto auto;
  gap: 16px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
