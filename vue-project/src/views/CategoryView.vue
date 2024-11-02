<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';

const categoriesToAdd = ref({});
const categoriesToEdit = ref({});
const categories = ref([]);
const users = ref([]);
const isSuperuser = ref(false);
const selectedUserId = ref('');
const loading = ref(false);

async function fetchUsers() {
  try {
    const response = await axios.get('/api/users/');
    users.value = response.data;
    isSuperuser.value = true;
  } catch (error) {
    isSuperuser.value = false;
  }
}

async function fetchCategories() {
  loading.value = true;
  let url = '/api/categories/';
  if (isSuperuser.value && selectedUserId.value) {
    url += `?user_id=${selectedUserId.value}`;
  }
  const r = await axios.get(url);
  categories.value = r.data;
  loading.value = false;
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
});
</script>


<template>
  <div v-if="isSuperuser">
    <div class="form-floating mb-3">
      <select class="form-select" v-model="selectedUserId" @change="onUserChange">
        <option value="">Все пользователи</option>
        <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
      </select>
      <label for="floatingSelect">Фильтр по пользователю</label>
    </div>
  </div>

  <div
  class="modal fade"
  id="editCategoryModal"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true">
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

        <!-- Поле выбора пользователя, отображается только для суперюзеров -->
        <div class="form-floating mb-3" v-if="isSuperuser">
          <select class="form-select" v-model="categoriesToEdit.user_id" required>
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
          @click="onUpdateCategory"
          data-bs-dismiss="modal">
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
          <div class="form-floating mb-3">
            <input type="text" class="form-control" v-model="categoriesToAdd.name" required />
            <label for="floatingInput">Название</label>
          </div>
          <div v-if="isSuperuser">
            <div class="form-floating mb-3">
              <select class="form-select" v-model="categoriesToAdd.user_id" required>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
              </select>
              <label for="floatingSelect">Пользователь</label>
            </div>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="category in categories" class="category_item" :key="category.id">
      <span>
        <b>Название:</b> {{ category.name }}
        <template v-if="isSuperuser">
          <br /><b>Пользователь:</b> {{ category.user.username }}
        </template>
      </span>
      <button
        class="btn btn-info"
        @click="onCategoryEditClick(category)"
        data-bs-toggle="modal"
        data-bs-target="#editCategoryModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(category)"><i class="bi bi-x"></i></button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.category_item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
