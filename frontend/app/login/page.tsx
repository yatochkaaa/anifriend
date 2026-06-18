import { Card } from '@/components/ui/card'
import Link from 'next/link'
import { Suspense } from 'react'
import LoginForm from './LoginForm'

export default async function LoginPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-md flex-col items-center justify-center gap-6 px-4 py-12">
      <div className="w-full space-y-3">
        <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          Welcome back, <span className="text-primary">senpai</span>
        </h1>
        <p className="text-foreground/70">
          Your anime journey continues — let&apos;s find your next obsession.
        </p>
      </div>
      <Card className="w-full p-6 shadow-lg">
        <Suspense>
          <LoginForm />
        </Suspense>
      </Card>
      <p className="text-muted-foreground text-sm">
        No account yet?{' '}
        <Link
          href="/signup"
          className="text-primary font-semibold underline-offset-4 hover:underline"
        >
          Join the club ✨
        </Link>
      </p>
    </main>
  )
}
