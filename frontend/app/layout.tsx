import Navbar from '@/components/Navbar'
import { ThemeProvider } from '@/components/providers/ThemeProvider'
import { cn } from '@/lib/utils'
import type { Metadata } from 'next'
import { Fira_Code, Nunito } from 'next/font/google'
import './globals.css'

const fontSans = Nunito({
  subsets: ['latin', 'cyrillic'],
  variable: '--font-sans',
})

const fontMono = Fira_Code({
  subsets: ['latin', 'cyrillic'],
  variable: '--font-mono',
})

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
    <html
      lang="en"
      suppressHydrationWarning
      className={cn('h-full', 'antialiased', 'font-sans', fontSans.variable, fontMono.variable)}
    >
      <body className="flex min-h-full flex-col">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Navbar />
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
