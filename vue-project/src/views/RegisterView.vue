<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { faAmazonPay, faApplePay, faGooglePay, faPaypal } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'; 

const registrationData = ref({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  password: '',
});

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

const registerUser = async () => {
  try {
    const response = await axios.post('/api/register/', registrationData.value);
    alert('Регистрация прошла успешно!');
    console.log('Ответ сервера:', response.data);
  } catch (error) {
    console.error('Ошибка при регистрации:', error.response?.data || error.message);
    alert('Ошибка при регистрации. Попробуйте снова.');
  }
};

const openYouTube = () => {
  window.open('https://youtu.be/k2ZEsfteJ5g', '_blank');
};

</script>

<template>
<!-- Section: Design Block -->
<section class="text-center">
    <!-- Background image -->
    <div class="p-5 bg-image" style="background-image: url('https://mdbootstrap.com/img/new/textures/full/171.jpg'); height: 300px;"></div>
    <!-- Background image -->

    <div class="card mx-4 mx-md-5 shadow-5-strong bg-body-tertiary" style="margin-top: -100px; backdrop-filter: blur(30px);">
      <div class="card-body py-5 px-md-5">

        <div class="row d-flex justify-content-center">
          <div class="col-lg-8">
            <h2 class="fw-bold mb-5">Окно регистрации</h2>
            <form @submit.prevent="registerUser">
              <div class="row">
                <div class="col-md-6 mb-4">
                  <div data-mdb-input-init class="form-outline">
                    <input
                      type="text"
                      id="form3Example1"
                      class="form-control"
                      v-model="registrationData.first_name"
                      required
                    />
                    <label class="form-label" for="form3Example1">Имя</label>
                  </div>
                </div>
                <div class="col-md-6 mb-4">
                  <div data-mdb-input-init class="form-outline">
                    <input
                      type="text"
                      id="form3Example2"
                      class="form-control"
                      v-model="registrationData.last_name"
                      required
                    />
                    <label class="form-label" for="form3Example2">Фамилия</label>
                  </div>
                </div>
              </div>

              <div data-mdb-input-init class="form-outline mb-4">
                <input
                  type="email"
                  id="form3Example3"
                  class="form-control"
                  v-model="registrationData.email"
                  required
                />
                <label class="form-label" for="form3Example3">Почта</label>
              </div>

              <div data-mdb-input-init class="form-outline mb-4">
                <input
                  type="text"
                  id="formUsername"
                  class="form-control"
                  v-model="registrationData.username"
                  required
                />
                <label class="form-label" for="formUsername">Username</label>
              </div>

              <div data-mdb-input-init class="form-outline mb-4">
                <input
                  type="password"
                  id="form3Example4"
                  class="form-control"
                  v-model="registrationData.password"
                  required
                />
                <label class="form-label" for="form3Example4">Пароль</label>
              </div>

              <button type="submit" class="btn btn-primary btn-block mb-4">
                Зарегистрироваться
              </button>
            </form>

            <p class="text-center mt-4">или зарегистрироваться с помощью:</p>

            <div class="d-flex justify-content-center">
              <button type="button" class="btn btn-light me-2" @click="openYouTube">
                <FontAwesomeIcon :icon="faGooglePay" class="me-2" />
                Google Pay
              </button>
              <button type="button" class="btn btn-light me-2" @click="openYouTube">
                <FontAwesomeIcon :icon="faAmazonPay" class="me-2" />
                Amazon Pay
              </button>
              <button type="button" class="btn btn-light me-2" @click="openYouTube">
                <FontAwesomeIcon :icon="faApplePay" class="me-2" />
                Apple Pay
              </button>
              <button type="button" class="btn btn-light" @click="openYouTube">
                <FontAwesomeIcon :icon="faPaypal" class="me-2" />
                PayPal
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </section>
  <!-- Section: Design Block -->
</template>
