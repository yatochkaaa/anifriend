import { TokenData } from '@/types/auth'
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function parseToken(token: string): TokenData | null {
  try {
    const tokenBase64Payload = token.split('.')[1]
    return JSON.parse(atob(tokenBase64Payload)) ?? null
  } catch {
    return null
  }
}

export const isTokenValid = (token?: string) => {
  if (!token) return false
  const tokenExpMs = (parseToken(token)?.exp ?? 0) * 1000
  const bufferMs = 5000
  return tokenExpMs - Date.now() > bufferMs
}
