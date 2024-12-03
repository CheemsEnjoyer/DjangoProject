<script setup>
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import useUserProfileStore from "@/stores/userProfileStore";
import { faAmazonPay, faApplePay, faGooglePay, faPaypal } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const userProfileStore = useUserProfileStore();
const { is_auth, username, is_superuser } = storeToRefs(userProfileStore);
const router = useRouter();

const loginData = ref({
  username: '',
  password: '',
});

const errorMessage = ref('');

const loginUser = async () => {
  try {
    await userProfileStore.loginUser(loginData.value.username, loginData.value.password);
    errorMessage.value = '';
    alert('Вы успешно вошли в систему!');
    router.push('/products');
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Ошибка при авторизации. Проверьте данные.';
  }
};

const logoutUser = async () => {
  try {
    await userProfileStore.logoutUser();
    alert('Вы успешно вышли из системы!');
  } catch (error) {
    console.error('Ошибка при выходе из системы:', error.response?.data || error.message);
  }
};

const openYouTube = () => {
  window.open('https://youtu.be/k2ZEsfteJ5g', '_blank');
};
</script>

<template>
  <section class="vh-100 gradient-custom">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <div class="card bg-dark text-white" style="border-radius: 1rem;">
            <div class="card-body p-5 text-center">

              <!-- Conditional content based on auth status -->
              <div v-if="is_auth">
                <h2 class="fw-bold mb-4">Добро пожаловать, {{ username }}!</h2>
                <button class="btn btn-outline-light btn-lg px-5 mb-4" @click="logoutUser">Выйти</button>
              </div>

              <div v-else>
                <h2 class="fw-bold mb-2 text-uppercase">Авторизация</h2>
                <p class="text-white-50 mb-5">Введите свой логин и пароль!</p>

                <!-- Username input -->
                <div data-mdb-input-init class="form-outline form-white mb-4">
                  <input
                    type="text"
                    id="typeUsername"
                    class="form-control form-control-lg"
                    v-model="loginData.username"
                    required
                  />
                  <label class="form-label" for="typeUsername">Логин</label>
                </div>

                <!-- Password input -->
                <div data-mdb-input-init class="form-outline form-white mb-4">
                  <input
                    type="password"
                    id="typePasswordX"
                    class="form-control form-control-lg"
                    v-model="loginData.password"
                    required
                  />
                  <label class="form-label" for="typePasswordX">Пароль</label>
                </div>

                <!-- Error message -->
                <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>

                <!-- Login button -->
                <button
                  data-mdb-button-init
                  data-mdb-ripple-init
                  class="btn btn-outline-light btn-lg px-5"
                  type="button"
                  @click="loginUser"
                >
                  Войти
                </button>

                <p class="text-center mt-4">или зарегистрироваться с помощью:</p>

                <!-- External service buttons -->
                <div class="d-flex justify-content-center">
                  <button type="button" class="btn btn-dark me-3" @click="openYouTube">
                    <FontAwesomeIcon :icon="faGooglePay" class="me-2" />
                    Google Pay
                  </button>
                  <button type="button" class="btn btn-dark me-2" @click="openYouTube">
                    <FontAwesomeIcon :icon="faAmazonPay" class="me-2" />
                    Amazon Pay
                  </button>
                  <button type="button" class="btn btn-dark me-2" @click="openYouTube">
                    <FontAwesomeIcon :icon="faApplePay" class="me-2" />
                    Apple Pay
                  </button>
                  <button type="button" class="btn btn-dark" @click="openYouTube">
                    <FontAwesomeIcon :icon="faPaypal" class="me-2" />
                    PayPal
                  </button>
                </div>

                <p class="mt-4">
                  У вас нет аккаунта? 
                  <router-link to="/register" class="text-primary">Зарегистрироваться</router-link>
                </p>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
</style>
