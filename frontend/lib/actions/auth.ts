'use server'

import { cookies } from 'next/headers'

export const saveToken = async (token: string) => {
  const cookieStore = await cookies()
  cookieStore.set('access_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
  })
}
