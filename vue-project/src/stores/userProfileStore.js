import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

const useUserProfileStore = defineStore("UserProfileStore", () => {
    const is_auth = ref(false);
    const username = ref("");
    const is_superuser = ref(false);

    async function fetchUserInfo() {
        try {
            const r = await axios.get("/api/user/info");
            is_auth.value = r.data.is_authenticated;
            username.value = r.data.username;
            is_superuser.value = r.data.is_superuser;
        } catch (error) {
            console.error("Ошибка при получении информации о пользователе:", error);
        }
    }
    return { is_auth, username, is_superuser, fetchUserInfo };
});

export default useUserProfileStore;
