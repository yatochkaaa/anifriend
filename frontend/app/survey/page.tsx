import { getGenres } from '@/lib/api/genres'
import SurveyForm from './SurveyForm'
import { Card } from '@/components/ui/card'

export default async function SurveyPage() {
  const genres = await getGenres()

  return (
    <div>
      <h1>Survey</h1>

      <Card className="p-4">
        <SurveyForm genres={genres} />
      </Card>
    </div>
  )
}
