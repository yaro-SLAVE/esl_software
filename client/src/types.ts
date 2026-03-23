export type User = {
    is_superuser: boolean;
    username: string;
    first_name: string | undefined;
    last_name: string | undefined;
};

export type UserProfile = {
    user: User,
    role: string,
    company_id: number | undefined,
    filial_id: number | undefined,
    is_auth: boolean,
}