"use client"
import { useEffect, useState } from 'react'
import { ReasoningCard } from '@/components/ReasoningCard'

export default function Home() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        // REPLACE WITH YOUR ACTUAL VPS IP
        const res = await fetch('http://172.26.153.3:8000/api/status')
        if (!res.ok) throw new Error('API down')
        const json = await res.json()
        setData(json)
        setError(false)
      } catch (err) {
        console.error("Fetch error:", err)
        setError(true)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <main className="min-h-screen bg-black flex flex-col items-center justify-center p-4">
      <h1 className="text-yellow-500 text-3xl font-bold mb-8 uppercase tracking-widest">
        Celo Agent V2 Control
      </h1>
      
      {error && (
        <div className="mb-4 p-2 bg-red-900/50 border border-red-500 text-red-200 text-xs rounded">
          ⚠️ Cannot reach Agent API. Check if port 8000 is open.
        </div>
      )}

      {data ? (
        <ReasoningCard data={data} />
      ) : (
        <div className="flex flex-col items-center space-y-4">
          <div className="h-12 w-12 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-slate-400 animate-pulse text-sm">Synchronizing with Celo Mainnet...</p>
        </div>
      )}
    </main>
  )
}
