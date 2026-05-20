export interface SurveyCreate {
  genres_prefer: number[]
  genres_avoid: number[]
  animes_prefer: number[]
  characters_prefer: number[]
}

export interface Survey extends SurveyCreate {
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
