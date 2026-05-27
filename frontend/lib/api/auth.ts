import { Token, TokenResponse, UserCreate, UserCreateFormData, UserLogin } from '@/types/auth'

export const createUser = async (formData: UserCreateFormData): Promise<Token> => {
  const payload: UserCreate = {
    email: formData.email,
    username: formData.username,
    password: formData.password,
    password_repeat: formData.passwordRepeat,
    date_of_birth: formData.dateOfBirth.toLocaleDateString('en-CA'),
  }

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const { detail } = await res.json()
    throw new Error(detail ?? 'Failed to register user')
  }

  const { access_token, token_type }: TokenResponse = await res.json()
  return { accessToken: access_token, tokenType: token_type }
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

  const { access_token, token_type }: TokenResponse = await res.json()
  return { accessToken: access_token, tokenType: token_type }
}
