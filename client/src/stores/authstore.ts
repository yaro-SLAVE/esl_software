import {defineStore} from "pinia";
import {ref, onBeforeMount, computed} from 'vue';
import { api } from 'boot/axios';
import { jwtDecode } from "jwt-decode";
import type { User, UserProfile} from "../types"
import { useQuasar } from 'quasar';

import { useRouter } from 'vue-router';
import { LocalStorage } from 'quasar'
import { onMounted } from "vue";
import { computedAsync } from "@vueuse/core";

const $q = useQuasar();

const router = useRouter();

export const useAuthStore = defineStore("AuthStore", () => {
    type Tokens = {
        access: string;
        refresh: string;
    };

    type Token = string | undefined;
    
    const userProf = ref<UserProfile>();

    const jwt = ref<Token>(LocalStorage.getItem('jwt') as string || '');
    const refresh = ref<Token>(LocalStorage.getItem('refresh') as string || '');

    const is_auth = ref<boolean>(true);

    function isTokenValid(token: Token): boolean {

        if (token === undefined) {
    
            return false;
        } else {
            const decoded = jwtDecode(String(token));
            return Date.now() < decoded.exp! * 3000;
        }
    }

    function saveTokens(){
        LocalStorage.set('jwt', jwt.value);
        LocalStorage.set('refresh', refresh.value);
    }

    async function login(username: string, password: string): Promise<boolean> {      
        try {
            const result = (
                await api.post<Tokens>("/api/auth/login/", {
                    username: username,
                    password: password,
                })
            ).data;

            jwt.value = result.access;
            refresh.value = result.refresh;

            saveTokens();

            await getUserInfo();

            is_auth.value = true;
            return true;
        } catch(error) {
            is_auth.value = false;
            return false;
        }
    }

    async function logout() {
        const refreshCopy = refresh.value;
        refresh.value = undefined;
        jwt.value = undefined;
        userProf.value = undefined;
        is_auth.value = false;

        LocalStorage.set('jwt', '');
        LocalStorage.set('refresh', '');

        await api.post("/api/auth/logout/", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            },
            refresh: refreshCopy,
        });

        await api.post("/admin/logout/");
        saveTokens();

        await router.push('/login');
    }

    async function updateTokens(): Promise<boolean> {
        if (!isTokenValid(refresh.value)) {
            await logout();
            return false;
        } else if (!isTokenValid(jwt.value)) {
            await refreshTokens();
        }

        return true;
    }

    async function refreshTokens() {
        const newTokens: Tokens = (
        await api.post("/api/auth/refresh/", {
                refresh: refresh.value,
            })
        ).data;

        jwt.value = newTokens.access;
        refresh.value = newTokens.refresh;

        saveTokens();
    }

    async function getUserInfo() {
        if (await updateTokens()) {
            try {
                userProf.value = (await api.get<UserProfile>("/api/user/self-info/")).data;
                is_auth.value = userProf.value.is_auth;
            } catch(error) {
                console.error("Ошибка при получении инфы о пользователе", error);
            }
        }
    }

    onBeforeMount(async () => {
        await getUserInfo();
    });

    setInterval(() => {
        updateTokens().catch(error => {
            console.error('Error updating tokens:', error);
        });
    }, 120000);

    return {userProf, jwt, is_auth, login, logout, getUserInfo, updateTokens};
});