import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

const useUserProfileStore = defineStore("UserProfileStore", () => {
  const is_auth = ref(false);
  const username = ref("");
  const is_superuser = ref(false);

  async function fetchUserInfo() {
    try {
      const response = await axios.get("/api/user/info/");
      is_auth.value = response.data.is_authenticated;
      username.value = response.data.username || "";
      is_superuser.value = response.data.is_superuser || false;
    } catch (error) {
      console.error("Ошибка при получении информации о пользователе:", error);
    }
  }

  async function loginUser(usernameInput, passwordInput) {
    try {
      const response = await axios.post("/api/user/login/", {
        username: usernameInput,
        password: passwordInput,
      });

      await fetchUserInfo();
    } catch (error) {
      console.error("Ошибка авторизации:", error.response?.data || error.message);
      throw error;
    }
  }

  async function logoutUser() {
    try {
      await axios.get("/api/user/logout/");
      await fetchUserInfo();
    } catch (error) {
      console.error("Ошибка при выходе из системы:", error.response?.data || error.message);
    }
  }

  return {
    is_auth,
    username,
    is_superuser,
    fetchUserInfo,
    loginUser,
    logoutUser,
  };
});

export default useUserProfileStore;
