import {defineStore} from "pinia";
import {ref, onBeforeMount} from 'vue';
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import type { User} from "../types"
import { useQuasar } from 'quasar';

import { useRouter } from 'vue-router';

const $q = useQuasar();

const router = useRouter();

const useUserProfileStore = defineStore("UserProfileStore", () => {
    type Tokens = {
        access: string;
        refresh: string;
    };

    type Token = string | undefined;
    
    const userProf = ref<User>();

    const jwt = ref<Token>($q.localStorage.getItem('jwt') as string || '');
    const refresh = ref<Token>($q.localStorage.getItem('refresh') as string || '');

    const is_auth = ref<boolean>($q.localStorage.getItem('authorization') || false);

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

            await getAuthInfo();

            return true;
        } catch(error){
            console.error("При авторизации ошибка", error);
            return false;
        }
    }

    async function registry(
        username: string, 
        password: string,
        first_name: string,
        last_name: string,
        email: string,
        role: number
    ) {
        try {
            const userData = new FormData();
            userData.append('username', username);
            userData.append('password', password);
            userData.append('first_name', first_name);
            userData.append('last_name', last_name);

            console.log(email);
            if (email !== undefined) {
                userData.append('email', email);
            }

            const user = (await axios.post("/api/user/", userData)).data;

            const profData = new FormData();
            profData.append('user', String(user.id));
            profData.append('role', String(role));

            // const profile = (await axios.post("/api/profile/", profData));

            return true;
        } catch(error) {
            console.error(error);
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
                userProf.value = (await axios.get<User>("/api/profile/info/", {
                    headers: {
                        Authorization: `Bearer ${jwt.value}`
                    },
                })).data;
            } catch(error) {
                console.error("Ошибка при получении инфы о пользователе", error);
            }
        }
    }

    async function getAuthInfo() {
        if (await updateTokens()) {
            try {
                const data = (await axios.get("/api/user/auth_info/", {
                    headers: {
                        Authorization: `Bearer ${jwt.value}`
                    },
                })).data;

                is_auth.value = data["is_auth"];
            } catch(error) {
                console.error("Ошибка при получении инфы об авторизации пользователя", error);
            }
        }
    }

    onBeforeMount(async () => {
        await getAuthInfo();
        await getUserInfo();
    });

    setInterval(() => {
        updateTokens().catch(error => {
            console.error('Error updating tokens:', error);
        });
    }, 120000);

    return {userProf, jwt, is_auth, login, logout, getUserInfo, registry, getAuthInfo};
});

export default useUserProfileStore;