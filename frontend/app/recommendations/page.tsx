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
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Your recommendations</h1>
        <p className="text-muted-foreground mt-2">
          Based on your preferences, here are anime we think you&apos;ll enjoy.
        </p>
      </div>
      <Suspense fallback={<RecommendationsSkeleton />}>
        <RecommendationsFeed />
      </Suspense>
    </main>
  )
}
