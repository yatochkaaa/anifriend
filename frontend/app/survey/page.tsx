import { Card } from '@/components/ui/card'
import { getGenres } from '@/lib/api/genres'
import { getSurvey } from '@/lib/api/survey'
import { SurveyFormData } from '@/types/survey'
import { Heart, HeartCrack } from 'lucide-react'
import { Suspense } from 'react'
import SurveyForm from './SurveyForm'

async function SurveyFormFeed() {
  const [survey, genres] = await Promise.all([getSurvey(), getGenres()])
  const surveyFormData: SurveyFormData = {
    genres: survey?.genres ?? [],
    animes: survey?.animes ?? [],
  }

  return <SurveyForm survey={surveyFormData} genres={genres} isCreate={!Boolean(survey?.id)} />
}

export default function SurveyPage() {
  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-12">
      <div className="mb-8 space-y-3">
        <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          Find your <span className="text-primary">anime</span>
        </h1>
        <p className="text-foreground/70">
          Tell us what you&apos;re into and we&apos;ll do the matchmaking. 💘
        </p>
        <p className="border-primary/30 bg-primary/12 text-foreground/80 rounded-xl border px-4 py-3 text-sm">
          Tap once for favorite{' '}
          <Heart className="inline-block size-4 fill-current align-text-bottom text-green-600 dark:text-green-400" />{' '}
          · tap again for avoid{' '}
          <HeartCrack className="inline-block size-4 align-text-bottom text-red-600 dark:text-red-400" />{' '}
          · tap once more to reset.
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
