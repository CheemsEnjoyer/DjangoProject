<script setup>
import { ref, computed } from 'vue';
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
const categoriesToAdd = ref({});
const categoriesToEdit = ref({});
const categories = ref([]);
const loading = ref(false);
const users = ref([]);


async function fetchCategories() {
  loading.value = true;
  let url = '/api/categories/';
  if (is_superuser.value && selectedUserId.value) {
    url += `?user_id=${selectedUserId.value}`;
  }
  const r = await axios.get(url);
  categories.value = r.data;
  loading.value = false;
}

async function fetchUsers() {
  try {
    const response = await axios.get('/api/user/all');
    users.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке пользователей:", error);
  }
}

function onUserChange() {
  fetchCategories();
}

async function onCategoriesAdd() {
  const data = { ...categoriesToAdd.value };
  delete data.user;
  await axios.post('/api/categories/', data);
  await fetchCategories();
}

async function onRemoveClick(category) {
  await axios.delete(`/api/categories/${category.id}/`);
  await fetchCategories();
}

async function onCategoryEditClick(category) {
  categoriesToEdit.value = { ...category };
}

async function onUpdateCategory() {
  const data = { ...categoriesToEdit.value };
  delete data.user;
  await axios.put(`/api/categories/${categoriesToEdit.value.id}/`, data);
  await fetchCategories();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchUsers();
  await fetchCategories();
  if (is_superuser.value) {
    await fetchUsers();
  }
});
</script>

<template>
  <div v-if="is_superuser">
    <div class="form-floating mb-3">
      <select class="form-select" v-model="selectedUserId" @change="onUserChange">
        <option value="">Все пользователи</option>
        <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
      </select>
      <label for="floatingSelect">Фильтр по пользователю</label>
    </div>
  </div>

  <div class="modal fade" id="editCategoryModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование категории</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-3">
            <input type="text" class="form-control" v-model="categoriesToEdit.name" required />
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating mb-3" v-if="is_superuser">
            <select class="form-select" v-model="categoriesToEdit.user_id" required>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
            </select>
            <label for="floatingSelect">Пользователь</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" @click="onUpdateCategory" data-bs-dismiss="modal">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent.stop="onCategoriesAdd">
      <div class="row">
        <div class="col">
          <div v-if="is_superuser" class="form-floating mb-3">
            <input type="text" class="form-control" v-model="categoriesToAdd.name" required />
            <label for="floatingInput">Название</label>
          </div>
          <!-- <div v-if="is_superuser">
            <div class="form-floating mb-3">
              <select class="form-select" v-model="categoriesToAdd.user_id" required>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
              </select>
              <label for="floatingSelect">Пользователь</label>
            </div>
          </div> -->
        </div>
        <div v-if="is_superuser" class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="category in categories" class="category_item" :key="category.id">
      <span>
        <b>Название:</b> {{ category.name }}
        <span v-if="is_superuser"><b>Пользователь:</b> {{ category.user?.username }}</span>

      </span>
      <button v-if="is_superuser" class="btn btn-info" @click="onCategoryEditClick(category)" data-bs-toggle="modal" data-bs-target="#editCategoryModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button v-if="is_superuser" class="btn btn-danger" @click="onRemoveClick(category)"><i class="bi bi-x"></i></button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.category_item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 4px solid #d1d1d1;
  border-radius: 8px;
  background-color: #d9c006b6;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
