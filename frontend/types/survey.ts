export interface SurveyGenrePayload {
  id: number
  is_liked: boolean
}

export interface SurveyPayload {
  genres: SurveyGenrePayload[]
  animes: number[]
}

export interface SurveyRead extends SurveyPayload {
  id: number
  user_id: number
  created_at: string
  updated_at: string
}

export interface SurveyGenreFormData {
  id: number
  isLiked: boolean
}

export interface SurveyFormData {
  genres: SurveyGenreFormData[]
  animes: number[]
}

export interface Survey extends SurveyFormData {
  id: number
  userId: number
  createdAt: string
  updatedAt: string
}
