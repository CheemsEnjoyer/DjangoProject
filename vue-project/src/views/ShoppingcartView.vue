<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserProfileStore from "@/stores/userProfileStore";

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser } = storeToRefs(userProfileStore);

const shoppingcart = ref(null);
const loading = ref(false);

async function fetchShoppingcart() {
  loading.value = true;
  try {
    const response = await axios.get('/api/shoppingcarts/');
    shoppingcart.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке корзины:", error);
  } finally {
    loading.value = false;
  }
}

async function removeProductFromCart(cartItemId) {
  try {
    await axios.delete(`/api/productshoppingcart/${cartItemId}/`);
    await fetchShoppingcart();
  } catch (error) {
    console.error("Ошибка при удалении товара из корзины:", error);
  }
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchShoppingcart();
});
</script>

<template>
  <div v-if="is_auth">
    <h5>
      Покупатель: {{ username }}
      <span v-if="is_superuser">(Администратор)</span>
    </h5>

    <ul v-if="shoppingcart && shoppingcart.items && shoppingcart.items.length">
      <li v-for="item in shoppingcart.items" :key="item.id">
        {{ item.product.name }} - 
        {{ item.quantity }} шт. - 
        {{ item.product_cost }} ₽
        <button class="btn btn-danger btn-sm" @click="removeProductFromCart(item.id)">
          <i class="bi bi-x"></i>
        </button>
      </li>
    </ul>

    <p v-else>Корзина пуста.</p>

    <strong v-if="shoppingcart && shoppingcart.total">Общая сумма: {{ shoppingcart.total }} ₽</strong>
  </div>

  <div v-else>
    <p>Вы не авторизованы. Пожалуйста, войдите в систему.</p>
  </div>
</template>

<style scoped>
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
