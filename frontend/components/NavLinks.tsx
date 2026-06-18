'use client'

import { cn } from '@/lib/utils'
import { Clapperboard, SlidersHorizontal } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  { href: '/recommendations', label: 'For you', Icon: Clapperboard },
  { href: '/survey', label: 'Survey', Icon: SlidersHorizontal },
]

export default function NavLinks() {
  const pathname = usePathname()

  return (
    <nav className="border-border bg-foreground/5 flex items-center gap-1 rounded-full border p-1">
      {links.map(({ href, label, Icon }) => {
        const active = pathname === href
        return (
          <Link
            key={href}
            href={href}
            aria-current={active ? 'page' : undefined}
            className={cn(
              'flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-sm font-semibold tracking-tight transition-all',
              active
                ? 'bg-card text-primary shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            )}
          >
            <Icon className="size-4" />
            {label}
          </Link>
        )
      })}
    </nav>
  )
}
