<script setup>
import { storeToRefs } from 'pinia';
import useUserProfileStore from "@/stores/userProfileStore";
import { onMounted, watch, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser } = storeToRefs(userProfileStore);
const router = useRouter();
const route = useRoute();

const hideNavigation = computed(() => {
  return route.path === '/login' || route.path === '/register';
});

onMounted(async () => {
  await userProfileStore.fetchUserInfo();
  if (!is_auth.value && route.path !== '/login' && route.path !== '/register') {
    router.push('/login');
  }
});

const logoutUser = async () => {
  await userProfileStore.logoutUser();
  await router.push('/login');
};
</script>

<template>
  <div class="container" v-if="!hideNavigation">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"><i class="bi bi-backpack-fill"></i></a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Заказы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/shoppingcarts">Корзина</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/products">Товары</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/reviews">Отзывы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/categories">Категории</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false">
                {{ is_auth ? username : 'Пользователь' }}
              </a>
              <ul class="dropdown-menu">
                <li v-if="!is_auth"><a class="dropdown-item" href="/register">Регистрация</a></li>
                <li v-if="!is_auth"><a class="dropdown-item" href="/login">Авторизация</a></li>
                <li v-if="is_superuser"><a class="dropdown-item" href="/admin">Админка</a></li>
                <li v-if="is_auth">
                  <button class="dropdown-item" @click="logoutUser">Выйти</button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <RouterView />
  </div>
</template>

<style lang="scss" scoped></style>
