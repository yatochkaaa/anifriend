'use server'

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export const saveToken = async (token: string) => {
  const cookieStore = await cookies()
  cookieStore.set('access_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
  })
}

export const logout = async () => {
  const cookieStore = await cookies()
  cookieStore.delete('access_token')
  redirect('/login')
}
