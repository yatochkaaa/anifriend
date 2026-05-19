import { cacheLife } from 'next/cache'
import { Anime } from '@/types/anime'

export const getRecommendations = async (): Promise<Anime[]> => {
  'use cache'
  cacheLife('hours')

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/recommend/`)
  if (!res.ok) throw new Error('Failed to fetch recommendations')

  return res.json()
}
