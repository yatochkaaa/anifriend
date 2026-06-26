'use client'

import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Field, FieldError, FieldGroup, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { saveToken } from '@/lib/actions/auth'
import { createUser } from '@/lib/api/auth'
import { cn } from '@/lib/utils'
import { zodResolver } from '@hookform/resolvers/zod'
import { format } from 'date-fns'
import { ArrowRight, Calendar as CalendarIcon } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { Controller, useForm } from 'react-hook-form'
import { z } from 'zod'

const formSchema = z
  .object({
    email: z.email(),
    username: z
      .string()
      .min(4, 'Username must be at least 4 characters long')
      .max(20, 'Username must be at most 20 characters long')
      .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters long')
      .max(100, 'Password must be at most 100 characters long')
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/,
        'Password must contain at least one uppercase letter, one lowercase letter, and one number'
      ),
    password_repeat: z.string().min(1, 'Please repeat your password'),
    date_of_birth: z.date({ error: 'Please select your date of birth' }),
  })
  .refine((data) => data.password === data.password_repeat, {
    error: "Passwords don't match",
    path: ['password_repeat'],
  })

type SignupFormValues = z.infer<typeof formSchema>

export default function SignupForm() {
  const router = useRouter()
  const {
    control,
    register,
    formState: { errors, isSubmitting },
    handleSubmit,
    setError,
  } = useForm<SignupFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      username: '',
      password: '',
      password_repeat: '',
      date_of_birth: undefined,
    },
  })

  const onSubmit = async (data: SignupFormValues) => {
    try {
      const payload = { ...data, date_of_birth: format(data.date_of_birth, 'yyyy-MM-dd') }
      const { access_token } = await createUser(payload)
      await saveToken(access_token)
      router.push('/survey')
    } catch (e) {
      setError('root', { message: e instanceof Error ? e.message : 'Registration failed' })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-10">
      <FieldGroup>
        <Field data-invalid={!!errors.email}>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input
            {...register('email')}
            id="email"
            type="email"
            placeholder="senpai@noticed.me"
            aria-invalid={!!errors.email}
          />
          {errors.email && <FieldError errors={[errors.email]} />}
        </Field>

        <Field data-invalid={!!errors.username}>
          <FieldLabel htmlFor="username">Username</FieldLabel>
          <Input
            {...register('username')}
            id="username"
            type="text"
            placeholder="SenpaiNoticed"
            aria-invalid={!!errors.username}
          />
          {errors.username && <FieldError errors={[errors.username]} />}
        </Field>

        <Field data-invalid={!!errors.password}>
          <FieldLabel htmlFor="password">Password</FieldLabel>
          <Input
            {...register('password')}
            id="password"
            type="password"
            placeholder="Min 8 chars, no chakra required"
            aria-invalid={!!errors.password}
          />
          {errors.password && <FieldError errors={[errors.password]} />}
        </Field>

        <Field data-invalid={!!errors.password_repeat}>
          <FieldLabel htmlFor="password-repeat">Repeat password</FieldLabel>
          <Input
            {...register('password_repeat')}
            id="password-repeat"
            type="password"
            placeholder="One more time, just to be sure"
            aria-invalid={!!errors.password_repeat}
          />
          {errors.password_repeat && <FieldError errors={[errors.password_repeat]} />}
        </Field>

        <Controller
          name="date_of_birth"
          control={control}
          render={({ field, fieldState }) => (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel htmlFor="date-of-birth">Date of birth</FieldLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    id="date-of-birth"
                    type="button"
                    variant="outline"
                    className={cn(
                      !field.value && 'text-muted-foreground',
                      'w-full justify-start text-left font-normal'
                    )}
                  >
                    <CalendarIcon />
                    {field.value ? field.value.toLocaleDateString() : 'When, senpai?'}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={field.value ?? undefined}
                    captionLayout="dropdown"
                    startMonth={new Date(new Date().getFullYear() - 100, 0)}
                    endMonth={new Date(new Date().getFullYear() - 12, 11)}
                    onSelect={(date) => field.onChange(date ?? null)}
                  />
                </PopoverContent>
              </Popover>
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />
      </FieldGroup>

      {errors.root && <p className="text-destructive text-sm">{errors.root.message}</p>}

      <Button
        type="submit"
        size="lg"
        className="ml-auto flex gap-2 px-6 font-bold"
        disabled={isSubmitting}
      >
        Join the club <ArrowRight className="size-4" />
      </Button>
    </form>
  )
}
