import { Survey, SurveyCreate, SurveyFormData } from '@/types/survey'

export const createSurvey = async (survey: SurveyFormData): Promise<Survey> => {
  const payload: SurveyCreate = {
    genres_prefer: survey.genresPrefer,
    genres_avoid: survey.genresAvoid,
    animes_prefer: survey.animesPrefer,
    characters_prefer: survey.charactersPrefer,
  }

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/survey/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) throw new Error('Failed to send survey')

  return res.json()
}
