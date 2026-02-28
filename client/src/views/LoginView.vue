<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e: unknown) {
    if (e && typeof e === 'object' && 'response' in e) {
      const axiosError = e as { response?: { data?: { detail?: string } } }
      error.value = axiosError.response?.data?.detail || 'Login failed'
    } else {
      error.value = 'Login failed'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <form class="auth-form" @submit.prevent="handleLogin">
      <h1>Sign in</h1>

      <div v-if="error" class="error">{{ error }}</div>

      <label>
        Email
        <input v-model="email" type="email" required autocomplete="email" />
      </label>

      <label>
        Password
        <input v-model="password" type="password" required autocomplete="current-password" />
      </label>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign in' }}
      </button>

      <p class="link">Don't have an account? <RouterLink to="/register">Register</RouterLink></p>
    </form>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 360px;
  padding: 2rem;
}

.auth-form h1 {
  margin: 0 0 0.5rem;
}

.auth-form label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.auth-form input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  font-size: 1rem;
}

.auth-form button {
  padding: 0.625rem;
  border: none;
  border-radius: 6px;
  background: var(--color-primary);
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
}

.auth-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  background: #fef2f2;
  color: #dc2626;
  font-size: 0.875rem;
}

.link {
  text-align: center;
  font-size: 0.875rem;
}

.link a {
  color: var(--color-primary);
}
</style>
