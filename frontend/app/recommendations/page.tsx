import { getRecommendations } from '@/lib/api/recommend'
import { Suspense } from 'react'
import RecommendationList, { RecommendationsSkeleton } from './RecommendationList'

async function RecommendationsFeed() {
  const recommendations = await getRecommendations()
  return <RecommendationList animes={recommendations} />
}

export default function RecommendationsPage() {
  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-12">
      <div className="mb-8 space-y-3">
        <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          Your <span className="text-primary">picks</span>
        </h1>
        <p className="text-foreground/70">
          Matched to your taste — go on, find your next obsession.
        </p>
      </div>
      <Suspense fallback={<RecommendationsSkeleton />}>
        <RecommendationsFeed />
      </Suspense>
    </main>
  )
}
