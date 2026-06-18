import { Button } from '@/components/ui/button'
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
        <li key={i} className="overflow-hidden rounded-2xl">
          <Skeleton className="aspect-80/113 w-full rounded-b-none" />
          <div className="space-y-1 p-2.5">
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
      <div className="border-border bg-card w-full rounded-3xl border py-16">
        <div className="mx-auto flex max-w-sm flex-col items-center gap-4 text-center">
          <span className="text-5xl">🍜</span>
          <div className="space-y-1">
            <p className="text-lg font-bold">Nothing here yet!</p>
            <p className="text-muted-foreground text-sm">
              Tell us what you&apos;re into and we&apos;ll cook up some picks just for you.
            </p>
          </div>
          <Button asChild>
            <Link href="/survey">Take the survey →</Link>
          </Button>
        </div>
      </div>
    )

  return (
    <ul className="grid grid-cols-3 gap-4 sm:grid-cols-4 lg:grid-cols-6">
      {animes.map((anime, index) => (
        <li key={anime.id}>
          <Card className="group gap-0 overflow-hidden py-0 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
            <div className="relative aspect-80/113 w-full overflow-hidden">
              {anime.poster?.main_url ? (
                <Image
                  src={anime.poster.main_url}
                  alt={anime.name}
                  fill
                  className="object-cover transition-transform duration-300 group-hover:scale-105"
                  sizes="(min-width: 1024px) 16vw, (min-width: 640px) 25vw, 33vw"
                  priority={index < 6}
                />
              ) : (
                <div className="bg-muted text-muted-foreground flex h-full items-center justify-center text-sm">
                  No poster
                </div>
              )}
              {anime.score != null && (
                <span className="bg-background/85 absolute top-2 right-2 rounded-full px-2 py-0.5 font-mono text-xs font-semibold backdrop-blur">
                  ★ {anime.score}
                </span>
              )}
            </div>
            <CardContent className="p-2.5">
              <p className="group-hover:text-primary truncate text-sm leading-tight font-semibold transition-colors">
                {anime.name}
              </p>
            </CardContent>
          </Card>
        </li>
      ))}
    </ul>
  )
}
