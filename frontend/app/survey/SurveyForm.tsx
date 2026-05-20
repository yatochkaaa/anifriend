'use client'

import { Button } from '@/components/ui/button'
import { createSurvey } from '@/lib/api/survey'
import { cn } from '@/lib/utils'
import { Genre, GenreKind } from '@/types/genre'
import { zodResolver } from '@hookform/resolvers/zod'
import { useRouter } from 'next/navigation'
import { ComponentProps, useMemo } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { z } from 'zod'

interface SurveyFormProps {
  genres: Genre[]
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

export default function SurveyForm({ genres }: SurveyFormProps) {
  const router = useRouter()

  const form = useForm<SurveyFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      genresPrefer: [],
      genresAvoid: [],
      animesPrefer: [],
      charactersPrefer: [],
    },
  })

  const preferGenres = useWatch({ control: form.control, name: 'genresPrefer' })
  const avoidGenres = useWatch({ control: form.control, name: 'genresAvoid' })

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
      form.setValue(
        'genresPrefer',
        preferGenres.filter((id) => id !== genreId)
      )
      form.setValue('genresAvoid', [...avoidGenres, genreId])
    } else if (state === 'avoid') {
      form.setValue(
        'genresAvoid',
        avoidGenres.filter((id) => id !== genreId)
      )
    } else {
      form.setValue('genresPrefer', [...preferGenres, genreId])
    }
  }

  const onSubmit = async (survey: SurveyFormValues) => {
    try {
      await createSurvey(survey)
      router.push('/recommendations')
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-10">
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

      <div>
        <Button type="submit" className="ml-auto flex" disabled={form.formState.isSubmitting}>
          Submit
        </Button>
      </div>
    </form>
  )
}
