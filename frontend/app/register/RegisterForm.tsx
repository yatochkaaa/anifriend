'use client'

import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Field, FieldError, FieldGroup, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import { zodResolver } from '@hookform/resolvers/zod'
import { Calendar as CalendarIcon } from 'lucide-react'
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
    repeatPassword: z.string().min(1, 'Please repeat your password'),
    dateOfBirth: z.date(),
  })
  .refine((data) => data.password === data.repeatPassword, {
    error: "Passwords don't match",
    path: ['repeatPassword'],
  })

type RegisterFormValues = z.infer<typeof formSchema>

export default function RegisterForm() {
  const {
    control,
    register,
    formState: { errors, isSubmitting },
    handleSubmit,
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      username: '',
      password: '',
      repeatPassword: '',
      dateOfBirth: undefined,
    },
  })

  const onSubmit = async (data: RegisterFormValues) => {
    console.log(data)
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

        <Field data-invalid={!!errors.repeatPassword}>
          <FieldLabel htmlFor="repeat-password">Repeat password</FieldLabel>
          <Input
            {...register('repeatPassword')}
            id="repeat-password"
            type="password"
            placeholder="One more time, just to be sure"
            aria-invalid={!!errors.repeatPassword}
          />
          {errors.repeatPassword && <FieldError errors={[errors.repeatPassword]} />}
        </Field>

        <Controller
          name="dateOfBirth"
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

      <Button type="submit" className="ml-auto flex" disabled={isSubmitting}>
        Join
      </Button>
    </form>
  )
}
