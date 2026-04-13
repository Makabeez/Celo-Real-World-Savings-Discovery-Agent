import './globals.css'
import { Providers } from './providers' // <-- Add this import

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {/* Wrap children with the Providers */}
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
