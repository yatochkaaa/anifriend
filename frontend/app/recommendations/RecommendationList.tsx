import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Anime } from '@/types/anime'
import Image from 'next/image'
import Link from 'next/link'

interface RecommendationListProps {
  animes: Anime[]
}

export function RecommendationsSkeleton() {
  return (
    <ul className="grid grid-cols-3 gap-4 sm:grid-cols-4 lg:grid-cols-6">
      {Array.from({ length: 12 }).map((_, i) => (
        <li key={i} className="overflow-hidden rounded-lg">
          <Skeleton className="aspect-[80/113] w-full rounded-b-none" />
          <div className="space-y-1 p-2">
            <Skeleton className="h-3 w-full" />
            <Skeleton className="h-2 w-1/2" />
          </div>
        </li>
      ))}
    </ul>
  )
}

export default function RecommendationList({ animes }: RecommendationListProps) {
  if (!animes.length)
    return (
      <div className="border-border w-full rounded-2xl border py-16">
        <div className="mx-auto flex max-w-sm flex-col items-center gap-4 text-center">
          <span className="text-4xl">🎌</span>
          <div>
            <p className="font-medium">No recommendations yet</p>
            <p className="text-muted-foreground mt-1 text-sm">
              Select some genres in the survey and we&apos;ll find anime for you.
            </p>
          </div>
          <Link href="/survey" className="text-primary text-sm underline-offset-4 hover:underline">
            Go to survey →
          </Link>
        </div>
      </div>
    )

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
              {anime.score != null && (
                <p className="text-muted-foreground text-xs">★ {anime.score}</p>
              )}
            </CardContent>
          </Card>
        </li>
      ))}
    </ul>
  )
}
