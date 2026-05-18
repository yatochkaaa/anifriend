import { Genre } from '@/types/genre'
import { cache } from 'react'

export const getGenres: () => Promise<Genre[]> = cache(async () => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/genres/`)

  if (!res.ok) throw new Error('Failed to fetch genres')

  return res.json()
})
