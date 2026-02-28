import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../auth'

// Mock the auth API module
vi.mock('@/api/auth', () => ({
  loginUser: vi.fn(),
  registerUser: vi.fn(),
  getCurrentUser: vi.fn(),
}))

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('starts unauthenticated', () => {
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.user).toBeNull()
    expect(auth.token).toBeNull()
  })

  it('login sets user and token', async () => {
    const { loginUser } = await import('@/api/auth')
    const mockLogin = vi.mocked(loginUser)
    mockLogin.mockResolvedValueOnce({
      access_token: 'test-token',
      token_type: 'bearer',
      user: {
        id: '123',
        email: 'test@example.com',
        is_verified: true,
        is_superuser: false,
        created_at: '2024-01-01T00:00:00Z',
      },
    })

    const auth = useAuthStore()
    await auth.login('test@example.com', 'password')

    expect(auth.isAuthenticated).toBe(true)
    expect(auth.token).toBe('test-token')
    expect(auth.user?.email).toBe('test@example.com')
    expect(localStorage.getItem('token')).toBe('test-token')
  })

  it('logout clears state', async () => {
    const auth = useAuthStore()
    auth.token = 'some-token'
    auth.user = {
      id: '123',
      email: 'test@example.com',
      is_verified: true,
      is_superuser: false,
      created_at: '2024-01-01T00:00:00Z',
    }
    localStorage.setItem('token', 'some-token')

    auth.logout()

    expect(auth.isAuthenticated).toBe(false)
    expect(auth.token).toBeNull()
    expect(auth.user).toBeNull()
    expect(localStorage.getItem('token')).toBeNull()
  })
})
