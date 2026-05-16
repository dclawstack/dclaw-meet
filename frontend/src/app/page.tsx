"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { getDashboardStats, getHealth, Meeting, listMeetings, listRooms, Room } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function DashboardPage() {
  const [stats, setStats] = useState({ total_meetings: 0, total_rooms: 0, total_participants: 0, open_action_items: 0 })
  const [meetings, setMeetings] = useState<Meeting[]>([])
  const [rooms, setRooms] = useState<Room[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function load() {
      try {
        await getHealth()
        const s = await getDashboardStats()
        setStats(s)
        const m = await listMeetings()
        setMeetings(m.items.slice(0, 5))
        const r = await listRooms()
        setRooms(r.items.slice(0, 5))
      } catch (e) {
        setError("Failed to load dashboard data. Is the backend running?")
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) return <div className="p-8">Loading...</div>
  if (error) return <div className="p-8 text-red-600">{error}</div>

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">DClaw Meet</h1>
        <nav className="flex gap-3">
          <Link href="/meetings"><Button variant="outline">Meetings</Button></Link>
          <Link href="/rooms"><Button variant="outline">Rooms</Button></Link>
        </nav>
      </header>

      <section className="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium">Total Meetings</CardTitle></CardHeader>
          <CardContent><div className="text-3xl font-bold">{stats.total_meetings}</div></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium">Rooms</CardTitle></CardHeader>
          <CardContent><div className="text-3xl font-bold">{stats.total_rooms}</div></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium">Participants</CardTitle></CardHeader>
          <CardContent><div className="text-3xl font-bold">{stats.total_participants}</div></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium">Open Action Items</CardTitle></CardHeader>
          <CardContent><div className="text-3xl font-bold">{stats.open_action_items}</div></CardContent>
        </Card>
      </section>

      <section className="px-6 pb-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Meetings</CardTitle>
            <CardDescription>Latest scheduled and live meetings</CardDescription>
          </CardHeader>
          <CardContent>
            {meetings.length === 0 ? (
              <p className="text-gray-500">No meetings yet. <Link href="/meetings" className="underline">Create one</Link></p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow><TableHead>Title</TableHead><TableHead>Status</TableHead><TableHead>Created</TableHead></TableRow>
                </TableHeader>
                <TableBody>
                  {meetings.map((m) => (
                    <TableRow key={m.id}>
                      <TableCell>{m.title}</TableCell>
                      <TableCell><Badge variant={m.status === "live" ? "destructive" : "secondary"}>{m.status}</Badge></TableCell>
                      <TableCell>{new Date(m.created_at).toLocaleDateString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Meeting Rooms</CardTitle>
            <CardDescription>Persistent rooms for recurring meetings</CardDescription>
          </CardHeader>
          <CardContent>
            {rooms.length === 0 ? (
              <p className="text-gray-500">No rooms yet. <Link href="/rooms" className="underline">Create one</Link></p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow><TableHead>Name</TableHead><TableHead>Slug</TableHead></TableRow>
                </TableHeader>
                <TableBody>
                  {rooms.map((r) => (
                    <TableRow key={r.id}>
                      <TableCell>{r.name}</TableCell>
                      <TableCell><code className="text-xs bg-gray-100 px-1 rounded">{r.slug}</code></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </section>
    </main>
  )
}
