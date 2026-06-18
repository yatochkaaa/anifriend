'use client'

import { Button } from '@/components/ui/button'
import { createSurvey, updateSurvey } from '@/lib/actions/survey'
import { cn } from '@/lib/utils'
import { Genre, GenreKind } from '@/types/genre'
import { SurveyFormData } from '@/types/survey'
import { zodResolver } from '@hookform/resolvers/zod'
import { Heart, HeartCrack, Sparkles } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { ComponentProps, useMemo } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { z } from 'zod'

interface SurveyFormProps {
  survey: SurveyFormData
  genres: Genre[]
  isCreate: boolean
}

const formSchema = z.object({
  genresPrefer: z.array(z.int()).max(5, 'You can pick up to 5 preferred genres'),
  genresAvoid: z.array(z.int()),
  animesPrefer: z.array(z.int()),
  charactersPrefer: z.array(z.int()),
})

type SurveyFormValues = z.infer<typeof formSchema>
type GenreState = 'prefer' | 'avoid' | 'neutral'

const STATE_BG: Record<GenreState, NonNullable<ComponentProps<typeof Button>['variant']>> = {
  prefer: 'success',
  avoid: 'destructive',
  neutral: 'outline',
}

const STATE_MARKER: Record<GenreState, { Icon: typeof Heart; className: string }> = {
  prefer: { Icon: Heart, className: 'fill-current text-green-600 dark:text-green-400' },
  avoid: { Icon: HeartCrack, className: 'text-red-600 dark:text-red-400' },
  neutral: { Icon: Heart, className: '' }, // neutral marker stays hidden via opacity-0
}

const KIND_LABELS: Record<GenreKind, string> = {
  demographic: 'Demographics',
  genre: 'Genres',
  theme: 'Themes',
}

const KIND_ORDER: GenreKind[] = ['demographic', 'genre', 'theme']

export default function SurveyForm({ survey, genres, isCreate }: SurveyFormProps) {
  const router = useRouter()

  const {
    control,
    handleSubmit,
    setValue,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<SurveyFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      genresPrefer: survey.genresPrefer,
      genresAvoid: survey.genresAvoid,
      animesPrefer: survey.animesPrefer,
      charactersPrefer: survey.charactersPrefer,
    },
  })

  const preferGenres = useWatch({ control, name: 'genresPrefer' })
  const avoidGenres = useWatch({ control, name: 'genresAvoid' })

  const preferSet = useMemo(() => new Set(preferGenres), [preferGenres])
  const avoidSet = useMemo(() => new Set(avoidGenres), [avoidGenres])
  const preferGenresLimit = 5

  const genresByKind = KIND_ORDER.map((kind) => ({
    kind,
    genres: genres.filter((g) => g.kind === kind),
  }))

  const getGenreState = (genreId: number): GenreState => {
    if (preferSet.has(genreId)) return 'prefer'
    if (avoidSet.has(genreId)) return 'avoid'
    return 'neutral'
  }

  const toggleGenre = (genreId: number) => {
    const state = getGenreState(genreId)
    if (state === 'prefer') {
      setValue(
        'genresPrefer',
        preferGenres.filter((id) => id !== genreId)
      )
      setValue('genresAvoid', [...avoidGenres, genreId])
    } else if (state === 'avoid') {
      setValue(
        'genresAvoid',
        avoidGenres.filter((id) => id !== genreId)
      )
    } else {
      setValue('genresPrefer', [...preferGenres, genreId])
    }
  }

  const onSubmit = async (survey: SurveyFormValues) => {
    try {
      if (isCreate) {
        await createSurvey(survey)
      } else {
        await updateSurvey(survey)
      }
      router.push('/recommendations')
    } catch (e) {
      const action = isCreate ? 'Create' : 'Update'
      setError('root', { message: e instanceof Error ? e.message : `${action} survey failed` })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="relative flex flex-col gap-10">
      <div className="text-muted-foreground absolute top-0 right-0 flex gap-3 text-sm font-semibold tabular-nums">
        <span
          className={cn(
            'flex items-center gap-1',
            preferGenres.length > preferGenresLimit && 'text-destructive'
          )}
        >
          <Heart className="size-3.5 fill-current text-green-600 dark:text-green-400" />
          {preferGenres.length}/{preferGenresLimit}
        </span>
        <span className="flex items-center gap-1">
          <HeartCrack className="size-3.5 text-red-600 dark:text-red-400" />
          {avoidGenres.length}
        </span>
      </div>
      {genresByKind.map(({ kind, genres: kindGenres }) => (
        <div key={kind} className="flex flex-col gap-3">
          <h2 className="text-foreground/70 text-base font-semibold tracking-wide uppercase">
            {KIND_LABELS[kind]}
          </h2>
          <ul className="flex flex-wrap gap-2">
            {kindGenres.map((genre) => {
              const state = getGenreState(genre.id)
              const { Icon: Marker, className: markerClass } = STATE_MARKER[state]
              return (
                <li key={genre.id}>
                  <Button
                    className="relative transition-transform hover:-translate-y-0.5 hover:scale-105"
                    type="button"
                    variant={STATE_BG[state]}
                    onClick={() => toggleGenre(genre.id)}
                  >
                    {genre.name}
                    <Marker
                      className={cn(
                        'absolute -top-1.5 -right-2 size-4 rotate-12 transition-opacity duration-300',
                        markerClass,
                        state === 'neutral' ? 'opacity-0' : 'opacity-100'
                      )}
                    />
                  </Button>
                </li>
              )
            })}
          </ul>
        </div>
      ))}

      <div>
        {errors.genresPrefer && (
          <p className="text-destructive text-sm">{errors.genresPrefer.message}</p>
        )}
        {errors.root && <p className="text-destructive text-sm">{errors.root.message}</p>}
      </div>

      <div>
        <Button
          type="submit"
          size="lg"
          className="ml-auto flex gap-2 px-6 font-bold"
          disabled={isSubmitting}
        >
          <Sparkles className="size-4" />
          {isCreate ? 'Find my destiny' : 'Update preferences'}
        </Button>
      </div>
    </form>
  )
}
