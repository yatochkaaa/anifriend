import { Anime } from '@/types/anime'

interface RecommendationListProps {
  animes: Anime[]
}

export default function RecommendationList({ animes }: RecommendationListProps) {
  return (
    <ul className="flex flex-wrap gap-2">
      {animes.map((anime) => (
        <li key={anime.id}>{anime.name}</li>
      ))}
    </ul>
  )
}
