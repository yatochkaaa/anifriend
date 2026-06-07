import { parseToken } from '@/lib/utils'
import { cookies } from 'next/headers'
import Link from 'next/link'
import { Suspense } from 'react'
import NavbarUserMenu from './NavbarUserMenu'

async function NavbarUser() {
  const token = (await cookies()).get('access_token')?.value
  if (!token) return null
  const username = parseToken(token)?.username
  if (!username) return null

  return (
    <div className="flex items-center gap-4">
      <Link href="/recommendations" className="text-muted-foreground hover:text-foreground text-sm">
        Recommendations
      </Link>
      <Link href="/survey" className="text-muted-foreground hover:text-foreground text-sm">
        Survey
      </Link>
      <NavbarUserMenu username={username} />
    </div>
  )
}

export default function Navbar() {
  return (
    <header className="border-border border-b">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/recommendations" className="font-bold">
          🎌 AniFriend
        </Link>

        <Suspense>
          <NavbarUser />
        </Suspense>
      </nav>
    </header>
  )
}
