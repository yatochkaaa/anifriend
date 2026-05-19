import { Card } from '@/components/ui/card'
import { getGenres } from '@/lib/api/genres'
import SurveyForm from './SurveyForm'

export default async function SurveyPage() {
  const genres = await getGenres()

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
        <SurveyForm genres={genres} />
      </Card>
    </main>
  )
}
