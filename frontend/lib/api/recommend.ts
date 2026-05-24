import { Anime } from '@/types/anime'
import { cookies } from 'next/headers'

export const getRecommendations = async (): Promise<Anime[]> => {
  const token = (await cookies()).get('access_token')?.value

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/recommend/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) throw new Error('Failed to fetch recommendations')

  return res.json()
}
