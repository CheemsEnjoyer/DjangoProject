<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';

const categoriesToAdd = ref({});
const categoriesToEdit = ref({});

const categories = ref([]);
const loading = ref(false);

async function fetchCategories() {
  loading.value = true;
  const r = await axios.get('/api/categories/');
  categories.value = r.data;
  loading.value = false;
}

async function onCategoriesAdd() {
  await axios.post('/api/categories/', {
    ...categoriesToAdd.value,
  });
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
  await axios.put(`/api/categories/${categoriesToEdit.value.id}/`, {
    ...categoriesToEdit.value,
  });
  await fetchCategories();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchCategories();
});
</script>

<template>
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
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-3">
            <input type="text" class="form-control" v-model="categoriesToEdit.name" required />
            <label for="floatingInput">Название</label>
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
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>
    <div v-for="category in categories" class="category_item" :key="category.id">
      <span><b>Название:</b> {{ category.name }}</span>
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
