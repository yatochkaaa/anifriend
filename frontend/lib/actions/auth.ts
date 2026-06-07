'use server'

import { parseToken } from '@/lib/utils'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export const saveToken = async (token: string) => {
  const cookieStore = await cookies()
  const tokenExpSeconds = parseToken(token)?.exp
  const currentSeconds = Math.floor(Date.now() / 1000)
  const maxAge = tokenExpSeconds ? Math.max(0, tokenExpSeconds - currentSeconds) : 0

  cookieStore.set('access_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge,
  })
}

export const logout = async () => {
  const cookieStore = await cookies()
  cookieStore.delete('access_token')
  redirect('/login')
}
