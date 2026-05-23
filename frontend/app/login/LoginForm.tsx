'use client'

import { Button } from '@/components/ui/button'
import { Field, FieldError, FieldGroup, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { saveToken } from '@/lib/actions/auth'
import { login } from '@/lib/api/auth'
import { zodResolver } from '@hookform/resolvers/zod'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { z } from 'zod'

const formSchema = z.object({
  username: z.string().min(1, 'Required'),
  password: z.string().min(1, 'Required'),
})

type LoginFormValues = z.infer<typeof formSchema>

export default function LoginForm() {
  const router = useRouter()
  const {
    register,
    formState: { errors, isSubmitting },
    handleSubmit,
    setError,
  } = useForm<LoginFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  })

  const onSubmit = async (data: LoginFormValues) => {
    try {
      const { accessToken } = await login(data)
      await saveToken(accessToken)
      router.push('/')
    } catch (e) {
      setError('root', { message: e instanceof Error ? e.message : 'Login failed' })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-10">
      <FieldGroup>
        <Field data-invalid={!!errors.username}>
          <FieldLabel htmlFor="username">Email or username</FieldLabel>
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
            placeholder="Your secret jutsu"
            aria-invalid={!!errors.password}
          />
          {errors.password && <FieldError errors={[errors.password]} />}
        </Field>
      </FieldGroup>

      {errors.root && <p className="text-destructive text-sm">{errors.root.message}</p>}

      <Button type="submit" className="ml-auto flex" disabled={isSubmitting}>
        Sign in
      </Button>
    </form>
  )
}
