import { Card } from '@/components/ui/card'
import Link from 'next/link'
import { Suspense } from 'react'
import SignupForm from './SignupForm'

export default async function SignupPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-md flex-col items-center justify-center gap-6 px-4 py-12">
      <div className="w-full space-y-3">
        <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          Join <span className="text-primary">AniFriend</span>
        </h1>
        <p className="text-foreground/70">
          Make an account and we&apos;ll hand-pick anime just for your taste. 🍥
        </p>
      </div>
      <Card className="w-full p-6 shadow-lg">
        <Suspense>
          <SignupForm />
        </Suspense>
      </Card>
      <p className="text-muted-foreground text-sm">
        Already one of us?{' '}
        <Link
          href="/login"
          className="text-primary font-semibold underline-offset-4 hover:underline"
        >
          Sign in
        </Link>
      </p>
    </main>
  )
}
