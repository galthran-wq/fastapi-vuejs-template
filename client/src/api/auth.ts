import api from './client'

export interface UserResponse {
  id: string
  email: string | null
  is_verified: boolean
  is_superuser: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserResponse
}

export async function loginUser(email: string, password: string): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/users/login', { email, password })
  return data
}

export async function createAnonUser(): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/users/')
  return data
}

export async function registerUser(email: string, password: string): Promise<TokenResponse> {
  // Step 1: create anonymous user to get a token
  const anon = await createAnonUser()
  localStorage.setItem('token', anon.access_token)

  // Step 2: register with email/password using the anon token
  const { data } = await api.post<TokenResponse>('/users/register', { email, password })
  return data
}

export async function getCurrentUser(): Promise<UserResponse> {
  const { data } = await api.get<UserResponse>('/users/me')
  return data
}
