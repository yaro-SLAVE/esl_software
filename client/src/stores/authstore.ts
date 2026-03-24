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

export const useAuthStore = defineStore("AuthStore", () => {
    const $q = useQuasar();

    const router = useRouter();

    type Tokens = {
        access: string;
        refresh: string;
    };

    type Token = string | undefined;
    
    const userProf = ref<UserProfile>();

    const jwt = ref<Token>(LocalStorage.getItem('jwt') as string || '');
    const refresh = ref<Token>(LocalStorage.getItem('refresh') as string || '');

    const is_auth = ref<boolean>(true);
    const role = ref<String>('');
    const filialId = ref();

    function isTokenValid(token: Token): boolean {

        if (token === undefined) {
    
            return false;
        } else {
            const decoded = jwtDecode(String(token));
            return Date.now() < decoded.exp! * 1000;
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

        await api.post("/api/auth/logout/",{
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
                const r = await api.get<UserProfile>("/api/user/self-info/");
                userProf.value = r.data;
                is_auth.value = userProf.value.is_auth;
                role.value = userProf.value.role;
                filialId.value = userProf.value.filial_id;
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

    return {userProf, jwt, is_auth, role, filialId, login, logout, getUserInfo, updateTokens};
});