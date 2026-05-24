import { Card } from '@/components/ui/card'
import { getGenres } from '@/lib/api/genres'
import { getSurvey } from '@/lib/api/survey'
import { SurveyFormData } from '@/types/survey'
import { Suspense } from 'react'
import SurveyForm from './SurveyForm'

async function SurveyFormFeed() {
  const [survey, genres] = await Promise.all([getSurvey(), getGenres()])
  const surveyFormData: SurveyFormData = {
    genresPrefer: survey?.genresPrefer ?? [],
    genresAvoid: survey?.genresAvoid ?? [],
    animesPrefer: survey?.animesPrefer ?? [],
    charactersPrefer: survey?.charactersPrefer ?? [],
  }

  return <SurveyForm survey={surveyFormData} genres={genres} isCreate={!Boolean(survey?.id)} />
}

export default function SurveyPage() {
  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Find your anime</h1>
        <p className="text-muted-foreground mt-2">
          Tell us your preferences and we&apos;ll recommend anime just for you.
        </p>
        <p className="border-border text-muted-foreground mt-4 border-l-2 pl-3 text-sm">
          Click once to mark as favorite ❤️, click again to mark as avoid 💀, click once more to
          reset.
        </p>
      </div>
      <Card className="p-6">
        <Suspense>
          <SurveyFormFeed />
        </Suspense>
      </Card>
    </main>
  )
}
