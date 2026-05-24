'use client'

import { Button } from '@/components/ui/button'
import { createSurvey, updateSurvey } from '@/lib/actions/survey'
import { cn } from '@/lib/utils'
import { Genre, GenreKind } from '@/types/genre'
import { SurveyFormData } from '@/types/survey'
import { zodResolver } from '@hookform/resolvers/zod'
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
  genresPrefer: z.array(z.int()),
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

const STATE_ICONS: Record<GenreState, string> = {
  prefer: '❤️',
  avoid: '💀',
  neutral: '💀', // neutral uses '💀' as hidden placeholder to enable smooth opacity transition
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
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-10">
      {genresByKind.map(({ kind, genres: kindGenres }) => (
        <div key={kind} className="flex flex-col gap-3">
          <h2 className="text-foreground/70 text-base font-semibold tracking-wide uppercase">
            {KIND_LABELS[kind]}
          </h2>
          <ul className="flex flex-wrap gap-2">
            {kindGenres.map((genre) => {
              const state = getGenreState(genre.id)
              return (
                <li key={genre.id}>
                  <Button
                    className="relative"
                    type="button"
                    variant={STATE_BG[state]}
                    onClick={() => toggleGenre(genre.id)}
                  >
                    {genre.name}
                    <span
                      className={cn(
                        'absolute -top-1 -right-2 rotate-20 transition-opacity duration-300',
                        state === 'neutral' ? 'opacity-0' : 'opacity-100'
                      )}
                    >
                      {STATE_ICONS[state]}
                    </span>
                  </Button>
                </li>
              )
            })}
          </ul>
        </div>
      ))}

      {errors.root && <p className="text-destructive text-sm">{errors.root.message}</p>}

      <div>
        <Button type="submit" className="ml-auto flex" disabled={isSubmitting}>
          {isCreate ? 'Find my destiny' : 'Update preferences'}
        </Button>
      </div>
    </form>
  )
}
