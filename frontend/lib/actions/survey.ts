'use server'

import { Survey, SurveyPayload } from '@/types/survey'
import { cookies } from 'next/headers'

export const createSurvey = async (payload: SurveyPayload): Promise<Survey> => {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')?.value

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/survey/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })

  if (!res.ok) throw new Error('Failed to send survey')

  return res.json()
}

export const updateSurvey = async (survey: SurveyPayload): Promise<Survey> => {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')?.value

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/survey/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(survey),
  })

  if (!res.ok) throw new Error('Failed to send survey')

  return res.json()
}
