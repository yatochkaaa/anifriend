import { getRecommendations } from '@/lib/api/recommend'
import RecommendationList from './RecommendationList'

export default async function RecommendationsPage() {
  const recommendations = await getRecommendations()

  return (
    <div>
      <h1>Recommendations</h1>

      <RecommendationList animes={recommendations} />
    </div>
  )
}
