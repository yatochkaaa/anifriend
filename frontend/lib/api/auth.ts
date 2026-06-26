import { Token, UserCreate, UserLogin } from '@/types/auth'

export const createUser = async (payload: UserCreate): Promise<Token> => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const { detail } = await res.json()
    throw new Error(detail ?? 'Failed to register user')
  }

  return res.json()
}

export const login = async (formData: UserLogin): Promise<Token> => {
  const params = new URLSearchParams({
    username: formData.username,
    password: formData.password,
  })

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params,
  })

  if (!res.ok) {
    const { detail } = await res.json()
    throw new Error(detail ?? 'Failed to login user')
  }

  return res.json()
}
