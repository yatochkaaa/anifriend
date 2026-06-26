import { Survey } from '@/types/survey'
import { cookies } from 'next/headers'

export async function getSurvey(): Promise<Survey | null> {
  const token = (await cookies()).get('access_token')?.value

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/survey/`, {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (res.status === 404) return null
  if (!res.ok) throw new Error('Failed to get survey')

  return res.json()
}
