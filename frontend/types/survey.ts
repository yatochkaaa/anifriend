export interface SurveyPayload {
  genres_prefer: number[]
  genres_avoid: number[]
  animes_prefer: number[]
  characters_prefer: number[]
}
export interface SurveyRead extends SurveyPayload {
  id: number
  user_id: number
  created_at: string
  updated_at: string
}

export interface SurveyFormData {
  genresPrefer: number[]
  genresAvoid: number[]
  animesPrefer: number[]
  charactersPrefer: number[]
}

export interface Survey extends SurveyFormData {
  id: number
  userId: number
  createdAt: string
  updatedAt: string
}
