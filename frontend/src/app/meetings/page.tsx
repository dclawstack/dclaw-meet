"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { createMeeting, deleteMeeting, listMeetings, listRooms, Meeting, Room } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

export default function MeetingsPage() {
  const [meetings, setMeetings] = useState<Meeting[]>([])
  const [rooms, setRooms] = useState<Room[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [title, setTitle] = useState("")
  const [roomId, setRoomId] = useState("")
  const [statusFilter, setStatusFilter] = useState("")

  async function load() {
    try {
      setLoading(true)
      const params = statusFilter ? { status: statusFilter } : undefined
      const m = await listMeetings(params)
      setMeetings(m.items)
      const r = await listRooms()
      setRooms(r.items)
      setError("")
    } catch (e) {
      setError("Failed to load meetings.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [statusFilter])

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault()
    if (!title || !roomId) return
    try {
      await createMeeting({ title, room_id: roomId, status: "scheduled" })
      setTitle("")
      setRoomId("")
      load()
    } catch {
      setError("Failed to create meeting.")
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete this meeting?")) return
    try {
      await deleteMeeting(id)
      load()
    } catch {
      setError("Failed to delete meeting.")
    }
  }

  if (loading && meetings.length === 0) return <div className="p-8">Loading...</div>

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">Meetings</h1>
        <nav className="flex gap-3">
          <Link href="/"><Button variant="outline">Dashboard</Button></Link>
          <Link href="/rooms"><Button variant="outline">Rooms</Button></Link>
        </nav>
      </header>

      <section className="p-6">
        {error && <div className="mb-4 text-red-600">{error}</div>}

        <div className="flex items-end justify-between mb-4 gap-4">
          <div className="w-48">
            <Select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              <option value="">All statuses</option>
              <option value="scheduled">Scheduled</option>
              <option value="live">Live</option>
              <option value="ended">Ended</option>
              <option value="cancelled">Cancelled</option>
            </Select>
          </div>

          <Dialog>
            <DialogTrigger asChild><Button>Create Meeting</Button></DialogTrigger>
            <DialogContent>
              <DialogHeader><DialogTitle>Create Meeting</DialogTitle></DialogHeader>
              <form onSubmit={handleCreate} className="space-y-4 mt-2">
                <div>
                  <Label htmlFor="title">Title</Label>
                  <Input id="title" value={title} onChange={(e) => setTitle(e.target.value)} required />
                </div>
                <div>
                  <Label htmlFor="room">Room</Label>
                  <Select value={roomId} onChange={(e) => setRoomId(e.target.value)}>
                    <option value="">Select a room</option>
                    {rooms.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
                  </Select>
                </div>
                <Button type="submit" className="w-full">Create</Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <Card>
          <CardHeader><CardTitle>All Meetings</CardTitle></CardHeader>
          <CardContent>
            {meetings.length === 0 ? (
              <p className="text-gray-500">No meetings found.</p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Title</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Room</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {meetings.map((m) => (
                    <TableRow key={m.id}>
                      <TableCell>{m.title}</TableCell>
                      <TableCell><Badge variant={m.status === "live" ? "destructive" : "secondary"}>{m.status}</Badge></TableCell>
                      <TableCell>{rooms.find((r) => r.id === m.room_id)?.name || m.room_id}</TableCell>
                      <TableCell>{new Date(m.created_at).toLocaleDateString()}</TableCell>
                      <TableCell className="text-right">
                        <Button size="sm" variant="ghost" onClick={() => handleDelete(m.id)}>Delete</Button>
                      </TableCell>
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
