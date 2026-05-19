import { Survey, SurveyCreate } from '@/types/survey'

export const createSurvey = async (survey: SurveyCreate): Promise<Survey> => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/survey/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(survey),
  })

  if (!res.ok) throw new Error('Failed to send survey')

  return res.json()
}
