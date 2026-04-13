import './globals.css'
import { Providers } from './providers'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta name="talentapp:project_verification" content="9207d630a4593884ac6d64a2bd1ef31fa36434c229196ccd663e4bf353a655fe15511408a65631f6906dc5b32baeb8c895853b7e8a6ee4aada1cc23cfb6b2e47" />
      </head>
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
