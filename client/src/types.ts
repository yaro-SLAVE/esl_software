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

export type Integration = {
    id: number,
    integration_type: string | undefined,
    integration_url: string | undefined,
    start_time: string | undefined,
    end_time: string | undefined,
    polling_frequency: number | undefined
}

export type IntegrationToUpdateCreate = {
    login: string | undefined,
    password: string | undefined,
    type: string | undefined,
    url: string | undefined,
    start_time: string | undefined,
    end_time: string | undefined,
    polling_frequency: number | undefined
}

export type CompanyOrFilial = {
    name: string | null,
    id: number | null,
}