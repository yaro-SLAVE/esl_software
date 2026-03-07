import {defineStore} from "pinia";
import {ref, onBeforeMount} from 'vue';
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import type { User} from "../types"
import { useQuasar } from 'quasar';

import { useRouter } from 'vue-router';

const $q = useQuasar();

const router = useRouter();

const useAuthStore = defineStore("AuthStore", () => {
    type Tokens = {
        access: string;
        refresh: string;
    };

    type Token = string | undefined;
    
    const userProf = ref<User>();

    const jwt = ref<Token>(localStorage.getItem('jwt') as string || '');
    const refresh = ref<Token>(localStorage.getItem('refresh') as string || '');

    const is_auth = ref<boolean>(Boolean(localStorage.getItem('authorization')) || false);

    function isTokenValid(token: Token): boolean {
        if (token === undefined) {
            return false;
        } else {
            const decoded = jwtDecode(String(token));
            return Date.now() < decoded.exp! * 1000;
        }
    }

    async function login(username: string, password: string): Promise<boolean> {      
        try {
            const result = (
                await axios.post<Tokens>("/api/auth/login/", {
                    username: username,
                    password: password,
                })
            ).data;

            jwt.value = result.access;
            refresh.value = result.refresh;

            await getUserInfo();

            is_auth.value = true;

            return true;
        } catch(error){
            console.error("При авторизации ошибка", error);
            return false;
        }
    }

    async function logout() {
        const refreshCopy = refresh.value;
        refresh.value = undefined;
        jwt.value = undefined;
        userProf.value = undefined;
        is_auth.value = false;

        await axios.post("/api/auth/logout/", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            },
            refresh: refreshCopy,
        });

        await axios.post("/admin/logout/")

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
        await axios.post("/api/auth/refresh/", {
                refresh: refresh.value,
            })
        ).data;

        jwt.value = newTokens.access;
        refresh.value = newTokens.refresh;
    }

    async function getUserInfo() {
        if (await updateTokens()) {
            try {
                userProf.value = (await axios.get<User>("/api/user/self-info/", {
                    headers: {
                        Authorization: `Bearer ${jwt.value}`
                    },
                })).data;
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

    return {userProf, jwt, is_auth, login, logout, getUserInfo};
});

export default useAuthStore;