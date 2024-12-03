<script setup>
import { computed, ref } from 'vue';
import axios from 'axios';
import { onBeforeMount, watch } from 'vue';
import Cookies from 'js-cookie';
import _ from 'lodash';
import { storeToRefs } from 'pinia';
import useUserProfileStore from "@/stores/userProfileStore";

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser } = storeToRefs(userProfileStore);

const productsToAdd = ref({});
const productsToEdit = ref({});

const categories = ref([]);
const products = ref([]);
const loading = ref(false);

const productPictureRef = ref();
const productAddImageUrl = ref();
const productEditImageUrl = ref();
const productEditPictureRef = ref();

const users = ref([]);
const selectedUserId = ref('');
const selectedCategoryId = ref('');
const selectedPicture = ref(null);

const minPrice = ref('');
const maxPrice = ref('');

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
  
  if (is_superuser.value && selectedUserId.value) {
    url += `?user_id=${selectedUserId.value}`;
  }

  if (selectedCategoryId.value) {
    url += (url.includes('?') ? '&' : '?') + `category_id=${selectedCategoryId.value}`;
  }

  if (minPrice.value) {
    url += (url.includes('?') ? '&' : '?') + `min_price=${minPrice.value}`;
  }

  if (maxPrice.value) {
    url += (url.includes('?') ? '&' : '?') + `max_price=${maxPrice.value}`;
  }

  const r = await axios.get(url);
  products.value = r.data;
  loading.value = false;
}

async function fetchUsers() {
  try {
    const response = await axios.get('/api/user/all/');
    users.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке пользователей:", error);
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
    headers: { 'Content-Type': 'multipart/form-data' },
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

  formData.set('name', productsToEdit.value.name);
  formData.set('cost', productsToEdit.value.cost);
  formData.set('description', productsToEdit.value.description);
  formData.set('amount', productsToEdit.value.amount);
  formData.set('category_id', productsToEdit.value.category_id);

  await axios.put(`/api/products/${productsToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  await fetchProducts();
}

async function productAddPictureChange() {
  productAddImageUrl.value = URL.createObjectURL(productPictureRef.value.files[0]);
}

async function productsEditPictureChange() {
  productEditImageUrl.value = URL.createObjectURL(productEditPictureRef.value.files[0]);
}

async function addToCart(productId, quantity = 1) {
  try {
    const response = await axios.post('/api/add_to_cart/', {
      product_id: productId,
      quantity: quantity,
    });
    alert("Товар успешно добавлен в корзину!");
  } catch (error) {
    console.error("Ошибка при добавлении товара в корзину:", error);
    alert("Не удалось добавить товар в корзину.");
  }
}

function resetPriceFilters() {
  minPrice.value = '';
  maxPrice.value = '';
  fetchProducts();
}

onBeforeMount(async () => {
  
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await userProfileStore.fetchUserInfo();
  await fetchCategories();
  await fetchProducts();
  if (is_superuser.value) {
    await fetchUsers();
  }
});

watch(selectedUserId, fetchProducts);
</script>

<template>
  <div class="form-floating mb-3" v-if="is_superuser">
    <select class="form-select" v-model="selectedUserId" @change="fetchReviews">
      <option value="">Все пользователи</option>
      <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
    </select>
    <label for="floatingSelect">Фильтр по пользователю</label>
  </div>

  <div class="form-floating mb-3">
    <select class="form-select" v-model="selectedCategoryId" @change="fetchProducts">
      <option value="">Все категории</option>
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
    <label for="categoryFilter">Фильтр по категории</label>
  </div>


  <div class="row mb-3">
    <div class="col-md-4">
      <input type="number" class="form-control" v-model="minPrice" placeholder="Минимальная цена" />
    </div>
    <div class="col-md-4">
      <input type="number" class="form-control" v-model="maxPrice" placeholder="Максимальная цена" />
    </div>
    <div class="col-md-4">
      <button class="btn btn-primary" @click="fetchProducts">Применить фильтры</button>
      <button class="btn btn-secondary" @click="resetPriceFilters" style="margin-left: 30px;">Сбросить</button>
    </div>
  </div>

  <div class="container mt-4">
    <form @submit.prevent="onProductsAdd" class="mb-4">
      <div class="row g-3 align-items-center">
        <div class="col-md-3">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="productName"
              placeholder="Название"
              v-model="productsToAdd.name"
              required
            />
            <label for="productName">Название</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="productCost"
              placeholder="Цена"
              v-model="productsToAdd.cost"
              required
            />
            <label for="productCost">Цена</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="productAmount"
              placeholder="Количество"
              v-model="productsToAdd.amount"
              required
            />
            <label for="productAmount">Количество</label>
          </div>
        </div>
        <div class="col-md-3">
          <div class="form-floating">
            <select
              class="form-select"
              id="productCategory"
              v-model="productsToAdd.category_id"
              required
            >
              <option v-for="category in categories" :value="category.id" :key="category.id">
                {{ category.name }}
              </option>
            </select>
            <label for="productCategory">Категория</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input
              type="file"
              class="form-control"
              id="productPicture"
              placeholder="Изображение"
              ref="productPictureRef"
              @change="productAddPictureChange"
            />
            <label for="productPicture">Изображение</label>
          </div>
        </div>
        <div class="col-md-12">
          <div class="form-floating">
            <textarea
              class="form-control"
              id="productDescription"
              placeholder="Описание"
              rows="2"
              v-model="productsToAdd.description"
              required
            ></textarea>
            <label for="productDescription">Описание</label>
          </div>
        </div>
        <div class="col-auto mt-3" v-if="is_superuser">
          <button class="btn btn-primary">Добавить товар</button>
        </div>
      </div>
      
    </form>

    <div class="row">
      <div class="col-md-4" v-for="product in products" :key="product.id">
        <div class="card mb-4 shadow-sm bg-warning">
          <img v-if="product.picture" :src="product.picture" class="card-img-top" alt="Изображение продукта" @click="selectedPicture = product.picture" />
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text"><b>Описание:</b> {{ product.description }}</p>
            <p class="card-text"><b>Цена:</b> {{ product.cost }} ₽</p>
            <p class="card-text"><b>Количество:</b> {{ product.amount }}</p>
            <p class="card-text"><b>Категория:</b> {{ product.category?.name }}</p>
            <p v-if="is_superuser" class="card-text"><b>Пользователь:</b> {{ product.user?.username }}</p>
            <div class="d-flex justify-content-between">
              <button v-if="is_superuser" class="btn btn-info btn-sm" @click="onProductEditClick(product)" data-bs-toggle="modal" data-bs-target="#editProductModal">
                <i class="bi bi-pen-fill"></i>
              </button>
              <button v-if="is_superuser" class="btn btn-danger btn-sm" @click="onRemoveClick(product)">
                <i class="bi bi-x"></i>
              </button>
              <button class="btn btn-primary" @click="addToCart(product.id, 1)">
                <i class="bi bi-cart"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="editProductModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование продукта</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
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
              <option v-for="category in categories" :value="category.id">{{ category.name }}</option>
            </select>
            <label for="floatingSelect">Категория</label>
          </div>
          <div class="col-auto">
            <input class="form-control" type="file" ref="productEditPictureRef" @change="productsEditPictureChange"></input>
          </div>
          <div class="form-floating mb-3">
            <img :src="productEditImageUrl" style="max-height: 60px" alt="" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" @click="onUpdateProduct" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="selectedPicture" class="overlay" @click="selectedPicture = null">
    <img :src="selectedPicture" class="zoomed-image" alt="Изображение продукта" />
  </div>
</template>

<style scoped>
.card img {
  max-height: 200px;
  object-fit: cover;
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
