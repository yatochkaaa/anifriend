'use server'

import { Survey, SurveyFormData, SurveyPayload } from '@/types/survey'
import { cookies } from 'next/headers'

export const createSurvey = async (survey: SurveyFormData): Promise<Survey> => {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')?.value

  const payload: SurveyPayload = {
    genres: survey.genres.map((g) => ({ id: g.id, is_liked: g.isLiked })),
    animes: survey.animes,
  }

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

export const updateSurvey = async (survey: SurveyFormData): Promise<Survey> => {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')?.value

  const payload: SurveyPayload = {
    genres: survey.genres.map((g) => ({ id: g.id, is_liked: g.isLiked })),
    animes: survey.animes,
  }

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/survey/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })

  if (!res.ok) throw new Error('Failed to send survey')

  return res.json()
}
