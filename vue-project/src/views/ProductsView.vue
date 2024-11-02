<script setup>
import { computed, ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.css';
import _ from 'lodash';

const productsToAdd = ref({});
const productsToEdit = ref({});

const categories = ref([]);
const products = ref([]);
const loading = ref(false);

const productPictureRef = ref();
const productAddImageUrl = ref();
const productEditImageUrl = ref();
const productEditPictureRef = ref();

const isSuperuser = ref(false);
const users = ref([]);
const selectedUserId = ref('');

const selectedPicture = ref(null);

const productsById = computed(() => {
  return _.keyBy(products.value, (x) => x.id);
});

async function fetchCategories() {
  const r = await axios.get('/api/categories/');
  categories.value = r.data;
}

async function fetchProducts() {
  loading.value = true;
  let url = '/api/products/';
  
  if (isSuperuser.value && selectedUserId.value) {
    url += `?user_id=${selectedUserId.value}`;
  }

  const r = await axios.get(url);
  products.value = r.data;
  loading.value = false;
}

async function fetchUsers() {
  try {
    const response = await axios.get('/api/users/');
    users.value = response.data;
    isSuperuser.value = true;
  } catch (error) {
    isSuperuser.value = false;
  }
}

async function onProductsAdd() {
  const formData = new FormData();

  formData.append('picture', productPictureRef.value.files[0]);

  formData.set('name', productsToAdd.value.name);
  formData.set('cost', productsToAdd.value.cost);
  formData.set('description', productsToAdd.value.description);
  formData.set('amount', productsToAdd.value.amount);
  formData.set('category_id', productsToAdd.value.category_id);

  await axios.post('/api/products/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  await fetchProducts();
}

async function onRemoveClick(product) {
  await axios.delete(`/api/products/${product.id}/`);
  await fetchProducts();
}

async function onProductEditClick(product) {
  productsToEdit.value = { ...product };
}

async function onUpdateProduct() {
  const formData = new FormData();
  if (productEditPictureRef.value.files[0]) {
    formData.append('picture', productEditPictureRef.value.files[0]);
  }
  console.log(productEditPictureRef.value.files);
  
  formData.set('name', productsToEdit.value.name);
  formData.set('cost', productsToEdit.value.cost);
  formData.set('description', productsToEdit.value.description);
  formData.set('amount', productsToEdit.value.amount);
  formData.set('category_id', productsToEdit.value.category_id);

  await axios.put(`/api/products/${productsToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  await fetchProducts();
}


async function productAddPictureChange() {
  productAddImageUrl.value = URL.createObjectURL(productPictureRef.value.files[0]);
}

async function productsEditPictureChange() {
  productEditImageUrl.value = URL.createObjectURL(productEditPictureRef.value.files[0]);
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchUsers();
  await fetchCategories();
  await fetchProducts();
});

</script>

<template>
  <div v-if="isSuperuser" class="form-floating mb-3">
    <select class="form-select" v-model="selectedUserId" @change="fetchProducts">
      <option value="">Все пользователи</option>
      <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
    </select>
    <label for="floatingSelect">Фильтр по пользователю</label>
  </div>

  <div
    class="modal fade"
    id="editProductModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование продукта</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-3">
            <input type="text" class="form-control" v-model="productsToEdit.name" required />
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating mb-3">
            <input type="number" class="form-control" v-model="productsToEdit.cost" required />
            <label for="floatingInput">Цена</label>
          </div>
          <div class="form-floating mb-3">
            <textarea class="form-control" v-model="productsToEdit.description" required></textarea>
            <label for="floatingTextarea">Описание</label>
          </div>
          <div class="form-floating mb-3">
            <input type="number" class="form-control" v-model="productsToEdit.amount" required />
            <label for="floatingInput">Количество</label>
          </div>
          <div class="form-floating mb-3">
            <select class="form-select" v-model="productsToEdit.category_id" required>
              <option v-for="category in categories" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            <label for="floatingSelect">Категория</label>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <input class="form-control" type="file" ref="productEditPictureRef" @change="productsEditPictureChange"></input>
            </div>
          </div>
          <div class="form-floating mb-3">
            <img :src="productEditImageUrl" style="max-height: 60px" alt="" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button
            type="button"
            class="btn btn-primary"
            @click="onUpdateProduct"
            data-bs-dismiss="modal">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent.stop="onProductsAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating mb-3">
            <input type="text" class="form-control" v-model="productsToAdd.name" required />
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating mb-3">
            <input type="number" class="form-control" v-model="productsToAdd.cost" required />
            <label for="floatingInput">Цена</label>
          </div>
          <div class="form-floating mb-3">
            <textarea class="form-control" v-model="productsToAdd.description" required></textarea>
            <label for="floatingTextarea">Описание</label>
          </div>
          <div class="form-floating mb-3">
            <input type="number" class="form-control" v-model="productsToAdd.amount" required />
            <label for="floatingInput">Количество</label>
          </div>
          <div class="form-floating mb-3">
            <select class="form-select" v-model="productsToAdd.category_id" required>
              <option v-for="category in categories" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            <label for="floatingSelect">Категория</label>
          </div>
        </div>
        <div class="col-auto">
          <input
            class="form-control"
            type="file"
            ref="productPictureRef"
            @change="productAddPictureChange" />
        </div>
        <div class="col-auto">
          <img :src="productAddImageUrl" style="max-height: 60px" alt="" />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>
    <div v-for="product in products" class="product_item" :key="product.id">
      <span><b>Название:</b> {{ product.name }}</span>
      <span><b>Цена:</b> {{ product.cost }}</span>
      <span><b>Описание:</b> {{ product.description }}</span>
      <span><b>Количество:</b> {{ product.amount }}</span>
      <span><b>Категория:</b> {{ product.category?.name }}</span>
      <span v-if="isSuperuser"><b>Пользователь:</b> {{ product.user?.username }}</span>
      <div v-show="product.picture">
        <img
          :src="product.picture"
          style="max-height: 60px; max-width: 100%; cursor: pointer"
          @click="selectedPicture = product.picture"
          alt="Изображение продукта" />
      </div>
      <button
        class="btn btn-info"
        @click="onProductEditClick(product)"
        data-bs-toggle="modal"
        data-bs-target="#editProductModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(product)">
        <i class="bi bi-x"></i>
      </button>
    </div>
  </div>

  <div v-if="selectedPicture" class="overlay" @click="selectedPicture = null">
    <img :src="selectedPicture" class="zoomed-image" alt="Изображение" />
  </div>
</template>

<style lang="scss" scoped>
.product_item {
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid #d1d1d1;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr auto auto auto;
  gap: 16px;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.zoomed-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
}
</style>
