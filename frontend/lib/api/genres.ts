import { cacheLife } from 'next/cache'
import { Genre } from '@/types/genre'

export const getGenres = async (): Promise<Genre[]> => {
  'use cache'
  cacheLife('days')

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/genres/`)
  if (!res.ok) throw new Error('Failed to fetch genres')

  return res.json()
}
