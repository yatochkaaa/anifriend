'use client'

import { Button } from '@/components/ui/button'
import { createSurvey, updateSurvey } from '@/lib/actions/survey'
import { cn } from '@/lib/utils'
import { Genre } from '@/types/genre'
import { SurveyFormData } from '@/types/survey'
import { zodResolver } from '@hookform/resolvers/zod'
import { Heart, HeartCrack, Sparkles } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { ComponentProps } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { z } from 'zod'

interface SurveyFormProps {
  survey: SurveyFormData
  genres: Genre[]
  isCreate: boolean
}

const formSchema = z.object({
  genres: z.array(z.object({ id: z.number(), isLiked: z.boolean() })),
  animes: z.array(z.int()),
})

type SurveyFormValues = z.infer<typeof formSchema>

const STATE_BG: Map<
  boolean | null,
  NonNullable<ComponentProps<typeof Button>['variant']>
> = new Map([
  [true, 'success'],
  [false, 'destructive'],
  [null, 'outline'],
])

const STATE_MARKER: Map<boolean | null, { Icon: typeof Heart; className: string }> = new Map([
  [true, { Icon: Heart, className: 'fill-current text-green-600 dark:text-green-400' }],
  [false, { Icon: HeartCrack, className: 'text-red-600 dark:text-red-400' }],
  [null, { Icon: Heart, className: '' }], // neutral marker stays hidden via opacity-0
])

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
      genres: survey.genres,
      animes: survey.animes,
    },
  })

  const userGenres = useWatch({ control, name: 'genres' })
  const getUserGenre = (id: number) => userGenres.find((ug) => ug.id === id) ?? null

  const toggleGenre = (genreId: number) => {
    const curGenre = getUserGenre(genreId)

    if (curGenre) {
      if (curGenre.isLiked) {
        setValue(
          'genres',
          userGenres.map((ug) => (ug.id !== genreId ? ug : { ...ug, isLiked: false }))
        )
      } else {
        setValue(
          'genres',
          userGenres.filter((ug) => ug.id !== genreId)
        )
      }
    } else {
      setValue('genres', [...userGenres, { id: genreId, isLiked: true }])
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
        <span className="flex items-center gap-1">
          <Heart className="size-3.5 fill-current text-green-600 dark:text-green-400" />
          {userGenres.filter((g) => g.isLiked).length}
        </span>
        <span className="flex items-center gap-1">
          <HeartCrack className="size-3.5 text-red-600 dark:text-red-400" />
          {userGenres.filter((g) => !g.isLiked).length}
        </span>
      </div>

      <div className="flex flex-col gap-3">
        <h2 className="text-foreground/70 text-base font-semibold tracking-wide uppercase">
          Genres
        </h2>
        <ul className="flex flex-wrap gap-2">
          {genres.map(({ id, name }) => {
            const curGenre = getUserGenre(id)
            const state = curGenre?.isLiked ?? null
            const { Icon: Marker, className: markerClass } = STATE_MARKER.get(state)!
            return (
              <li key={id}>
                <Button
                  className="relative transition-transform hover:-translate-y-0.5 hover:scale-105"
                  type="button"
                  variant={STATE_BG.get(state)}
                  onClick={() => toggleGenre(id)}
                >
                  {name}
                  <Marker
                    className={cn(
                      'absolute -top-1.5 -right-2 size-4 rotate-12 transition-opacity duration-300',
                      markerClass,
                      state === null ? 'opacity-0' : 'opacity-100'
                    )}
                  />
                </Button>
              </li>
            )
          })}
        </ul>
      </div>

      <div>
        {errors.genres && <p className="text-destructive text-sm">{errors.genres.message}</p>}
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
