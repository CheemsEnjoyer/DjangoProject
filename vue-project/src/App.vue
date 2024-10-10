<script setup></script>

<template>
  <div class="container">
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
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
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
