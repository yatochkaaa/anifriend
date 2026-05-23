import { Card } from '@/components/ui/card'
import Link from 'next/link'
import { Suspense } from 'react'
import LoginForm from './LoginForm'

export default async function LoginPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-md flex-col items-center justify-center gap-6 px-4 py-12">
      <div className="w-full">
        <h1 className="text-3xl font-bold">Welcome back, senpai</h1>
        <p className="text-muted-foreground mt-2">Your anime journey continues.</p>
      </div>
      <Card className="w-full p-6">
        <Suspense>
          <LoginForm />
        </Suspense>
      </Card>
      <p className="text-muted-foreground text-sm">
        Don&apos;t have an account?{' '}
        <Link href="/register" className="text-foreground underline-offset-4 hover:underline">
          Join the club
        </Link>
      </p>
    </main>
  )
}
