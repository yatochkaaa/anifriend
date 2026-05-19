'use client'

import { Button } from '@/components/ui/button'
import { createSurvey } from '@/lib/api/survey'
import { cn } from '@/lib/utils'
import { Genre } from '@/types/genre'
import { zodResolver } from '@hookform/resolvers/zod'
import { useRouter } from 'next/navigation'
import { ComponentProps } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { z } from 'zod'

interface SurveyFormProps {
  genres: Genre[]
}

const formSchema = z.object({
  genres_prefer: z.array(z.int()),
  genres_avoid: z.array(z.int()),
  animes_prefer: z.array(z.int()),
  characters_prefer: z.array(z.int()),
})

type FormData = z.infer<typeof formSchema>
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

export default function SurveyForm({ genres }: SurveyFormProps) {
  const router = useRouter()

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      genres_prefer: [],
      genres_avoid: [],
      animes_prefer: [],
      characters_prefer: [],
    },
  })

  const preferGenres = useWatch({ control: form.control, name: 'genres_prefer' })
  const avoidGenres = useWatch({ control: form.control, name: 'genres_avoid' })

  const getGenreState = (genreId: number): GenreState => {
    if (preferGenres.includes(genreId)) return 'prefer'
    if (avoidGenres.includes(genreId)) return 'avoid'
    return 'neutral'
  }

  const toggleGenre = (genreId: number) => {
    const state = getGenreState(genreId)
    if (state === 'prefer') {
      form.setValue(
        'genres_prefer',
        preferGenres.filter((id) => id !== genreId)
      )
      form.setValue('genres_avoid', [...avoidGenres, genreId])
    } else if (state === 'avoid') {
      form.setValue(
        'genres_avoid',
        avoidGenres.filter((id) => id !== genreId)
      )
    } else {
      form.setValue('genres_prefer', [...preferGenres, genreId])
    }
  }

  const onSubmit = async (survey: FormData) => {
    try {
      await createSurvey(survey)
      router.push('/recommendations')
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-8">
      <div>
        <h2 className="text-lg font-semibold">Genres</h2>
        <p className="text-muted-foreground text-sm">
          Click once to mark as favorite ❤️, click again to mark as avoid 💀, click once more to
          reset.
        </p>
      </div>

      <ul className="flex flex-wrap gap-2">
        {genres.map((genre) => {
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

      <div>
        <Button type="submit" className="ml-auto flex" disabled={form.formState.isSubmitting}>
          Submit
        </Button>
      </div>
    </form>
  )
}
