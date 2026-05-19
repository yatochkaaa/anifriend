import { getRecommendations } from '@/lib/api/recommend'
import RecommendationList from './RecommendationList'

export default async function RecommendationsPage() {
  const recommendations = await getRecommendations()

  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Your recommendations</h1>
        <p className="text-muted-foreground mt-2">
          Based on your preferences, here are anime we think you&apos;ll enjoy.
        </p>
      </div>
      <RecommendationList animes={recommendations} />
    </main>
  )
}
