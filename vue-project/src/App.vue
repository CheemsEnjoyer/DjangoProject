<script setup></script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"><i class="bi bi-backpack-fill"></i></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Заказы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/clients">Клиенты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/shoppingcarts">Корзины</router-link>
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
          <ul class="navbar-nav"></ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <RouterView/>
  </div>
</template>

<style lang="scss" scoped></style>
