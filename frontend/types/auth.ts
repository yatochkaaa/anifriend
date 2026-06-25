import { components } from '@/types/api'

export type Token = components['schemas']['Token']
export type UserCreate = components['schemas']['UserCreate']

export interface TokenData {
  sub: string
  username: string
  exp: number
}

export interface UserLogin {
  username: string
  password: string
}
