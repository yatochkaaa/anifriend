export type GenreKind = 'demographic' | 'genre' | 'theme'

export interface Genre {
  id: number
  shikimori_id: number
  kind: GenreKind
  name: string
  russian: string
}
