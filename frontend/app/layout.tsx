import type { Metadata } from 'next'
import { Figtree } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'

const figtree = Figtree({ subsets: ['latin'], variable: '--font-sans' })

export const metadata: Metadata = {
  title: 'AniFriend',
  description: 'AI-driven anime recommender',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={cn('dark', 'h-full', 'antialiased', 'font-sans', figtree.variable)}>
      <body className="flex min-h-full flex-col">{children}</body>
    </html>
  )
}
