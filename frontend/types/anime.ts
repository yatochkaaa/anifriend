export interface Poster {
  main_url: string | null
}

export interface Anime {
  id: number
  name: string
  russian: string | null
  score: number | null
  poster: Poster | null
}
