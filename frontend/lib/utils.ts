import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getUsernameFromToken(token: string): string | null {
  try {
    const tokenBase64Payload = token.split('.')[1]
    return JSON.parse(atob(tokenBase64Payload)).username ?? null
  } catch {
    return null
  }
}
