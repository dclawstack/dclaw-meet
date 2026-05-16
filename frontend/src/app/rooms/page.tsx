"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { createRoom, deleteRoom, listRooms, listUsers, Room, User } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

export default function RoomsPage() {
  const [rooms, setRooms] = useState<Room[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [name, setName] = useState("")
  const [slug, setSlug] = useState("")
  const [hostId, setHostId] = useState("")

  async function load() {
    try {
      setLoading(true)
      const r = await listRooms()
      setRooms(r.items)
      const u = await listUsers()
      setUsers(u.items)
      setError("")
    } catch {
      setError("Failed to load rooms.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault()
    if (!name || !slug || !hostId) return
    try {
      await createRoom({ name, slug, host_id: hostId })
      setName("")
      setSlug("")
      setHostId("")
      load()
    } catch {
      setError("Failed to create room. Slug may already exist.")
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete this room?")) return
    try {
      await deleteRoom(id)
      load()
    } catch {
      setError("Failed to delete room.")
    }
  }

  if (loading && rooms.length === 0) return <div className="p-8">Loading...</div>

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">Rooms</h1>
        <nav className="flex gap-3">
          <Link href="/"><Button variant="outline">Dashboard</Button></Link>
          <Link href="/meetings"><Button variant="outline">Meetings</Button></Link>
        </nav>
      </header>

      <section className="p-6">
        {error && <div className="mb-4 text-red-600">{error}</div>}

        <div className="flex justify-end mb-4">
          <Dialog>
            <DialogTrigger asChild><Button>Create Room</Button></DialogTrigger>
            <DialogContent>
              <DialogHeader><DialogTitle>Create Room</DialogTitle></DialogHeader>
              <form onSubmit={handleCreate} className="space-y-4 mt-2">
                <div>
                  <Label htmlFor="name">Name</Label>
                  <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                  <Label htmlFor="slug">Slug</Label>
                  <Input id="slug" value={slug} onChange={(e) => setSlug(e.target.value)} required placeholder="e.g. weekly-standup" />
                </div>
                <div>
                  <Label htmlFor="host">Host</Label>
                  <Select value={hostId} onChange={(e) => setHostId(e.target.value)}>
                    <option value="">Select a host</option>
                    {users.map((u) => <option key={u.id} value={u.id}>{u.full_name}</option>)}
                  </Select>
                </div>
                <Button type="submit" className="w-full">Create</Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <Card>
          <CardHeader><CardTitle>All Rooms</CardTitle></CardHeader>
          <CardContent>
            {rooms.length === 0 ? (
              <p className="text-gray-500">No rooms found. Create a room and some users first.</p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Slug</TableHead>
                    <TableHead>Host</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rooms.map((r) => (
                    <TableRow key={r.id}>
                      <TableCell>{r.name}</TableCell>
                      <TableCell><code className="text-xs bg-gray-100 px-1 rounded">{r.slug}</code></TableCell>
                      <TableCell>{users.find((u) => u.id === r.host_id)?.full_name || r.host_id}</TableCell>
                      <TableCell className="text-right">
                        <Button size="sm" variant="ghost" onClick={() => handleDelete(r.id)}>Delete</Button>
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
