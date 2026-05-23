import { Card } from '@/components/ui/card'
import Link from 'next/link'
import { Suspense } from 'react'
import SignupForm from './SignupForm'

export default async function SignupPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-md flex-col items-center justify-center gap-6 px-4 py-12">
      <div className="w-full">
        <h1 className="text-3xl font-bold">Join AniFriend</h1>
        <p className="text-muted-foreground mt-2">
          Create your account to get personalized anime recommendations.
        </p>
      </div>
      <Card className="w-full p-6">
        <Suspense>
          <SignupForm />
        </Suspense>
      </Card>
      <p className="text-muted-foreground text-sm">
        Already have an account?{' '}
        <Link href="/login" className="text-foreground underline-offset-4 hover:underline">
          Sign in
        </Link>
      </p>
    </main>
  )
}
