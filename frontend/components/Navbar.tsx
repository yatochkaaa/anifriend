import { parseToken } from '@/lib/utils'
import { cookies } from 'next/headers'
import Link from 'next/link'
import { Suspense } from 'react'
import { ModeToggle } from './ModeToggle'
import NavLinks from './NavLinks'
import NavbarUserMenu from './NavbarUserMenu'

async function NavbarUser() {
  const token = (await cookies()).get('access_token')?.value
  if (!token) return null
  const username = parseToken(token)?.username
  if (!username) return null

  return (
    <div className="flex items-center gap-2 sm:gap-3">
      <NavLinks />
      <NavbarUserMenu username={username} />
    </div>
  )
}

export default function Navbar() {
  return (
    <header className="bg-background/80 border-foreground/10 sticky top-0 z-50 border-b backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link
          href="/recommendations"
          className="flex items-center gap-1.5 text-xl font-extrabold tracking-tight transition-transform duration-300 hover:-rotate-2"
        >
          <span>🎌</span>
          <span>
            Ani<span className="text-primary">Friend</span>
          </span>
        </Link>

        <div className="flex items-center gap-1 sm:gap-2">
          <Suspense>
            <NavbarUser />
          </Suspense>
          <ModeToggle />
        </div>
      </nav>
    </header>
  )
}
