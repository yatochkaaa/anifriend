import { Card, CardContent } from '@/components/ui/card'
import { Anime } from '@/types/anime'
import Image from 'next/image'

interface RecommendationListProps {
  animes: Anime[]
}

export default function RecommendationList({ animes }: RecommendationListProps) {
  return (
    <ul className="grid grid-cols-3 gap-4 sm:grid-cols-4 lg:grid-cols-6">
      {animes.map((anime, index) => (
        <li key={anime.id}>
          <Card className="gap-0 overflow-hidden py-0">
            <div className="relative aspect-[80/113] w-full">
              {anime.poster?.main_url ? (
                <Image
                  src={anime.poster.main_url}
                  alt={anime.name}
                  fill
                  className="object-cover"
                  sizes="(min-width: 1024px) 16vw, (min-width: 640px) 25vw, 33vw"
                  priority={index < 6}
                />
              ) : (
                <div className="bg-muted text-muted-foreground flex h-full items-center justify-center text-sm">
                  No poster
                </div>
              )}
            </div>
            <CardContent className="p-2">
              <p className="truncate text-sm leading-tight font-medium">{anime.name}</p>
              {anime.score && <p className="text-muted-foreground text-xs">★ {anime.score}</p>}
            </CardContent>
          </Card>
        </li>
      ))}
    </ul>
  )
}
