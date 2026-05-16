const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  return response.json();
}

// ── Health ────────────────────────────────────────────

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

// ── Users ─────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  full_name: string;
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

export async function createUser(data: { email: string; full_name: string; avatar_url?: string | null }) {
  return fetchJson<User>("/api/v1/users", { method: "POST", body: JSON.stringify(data) });
}

export async function listUsers() {
  return fetchJson<PaginatedResponse<User>>("/api/v1/users");
}

export async function getUser(id: string) {
  return fetchJson<User>(`/api/v1/users/${id}`);
}

export async function updateUser(id: string, data: Partial<Omit<User, "id" | "created_at" | "updated_at">>) {
  return fetchJson<User>(`/api/v1/users/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function deleteUser(id: string) {
  return fetchJson<void>(`/api/v1/users/${id}`, { method: "DELETE" });
}

// ── Rooms ───────────────────────────────────────────────

export interface Room {
  id: string;
  name: string;
  slug: string;
  host_id: string;
  settings: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export async function createRoom(data: { name: string; slug: string; host_id: string; settings?: Record<string, unknown> }) {
  return fetchJson<Room>("/api/v1/rooms", { method: "POST", body: JSON.stringify(data) });
}

export async function listRooms() {
  return fetchJson<PaginatedResponse<Room>>("/api/v1/rooms");
}

export async function getRoom(id: string) {
  return fetchJson<Room>(`/api/v1/rooms/${id}`);
}

export async function updateRoom(id: string, data: Partial<Omit<Room, "id" | "created_at" | "updated_at">>) {
  return fetchJson<Room>(`/api/v1/rooms/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function deleteRoom(id: string) {
  return fetchJson<void>(`/api/v1/rooms/${id}`, { method: "DELETE" });
}

// ── Meetings ──────────────────────────────────────────

export interface Meeting {
  id: string;
  room_id: string;
  title: string;
  scheduled_start: string | null;
  scheduled_end: string | null;
  status: string;
  recording_url: string | null;
  summary: string | null;
  created_at: string;
  updated_at: string;
}

export interface MeetingDetail extends Meeting {
  participants: Participant[];
  action_items: ActionItem[];
}

export interface Participant {
  id: string;
  meeting_id: string;
  user_id: string | null;
  email: string;
  role: string;
  joined_at: string | null;
  left_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ActionItem {
  id: string;
  meeting_id: string;
  assignee_id: string | null;
  description: string;
  due_date: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export async function createMeeting(data: { title: string; room_id: string; scheduled_start?: string | null; scheduled_end?: string | null; status?: string }) {
  return fetchJson<Meeting>("/api/v1/meetings", { method: "POST", body: JSON.stringify(data) });
}

export async function listMeetings(params?: { status?: string; room_id?: string }) {
  const qs = new URLSearchParams();
  if (params?.status) qs.set("status", params.status);
  if (params?.room_id) qs.set("room_id", params.room_id);
  return fetchJson<PaginatedResponse<Meeting>>(`/api/v1/meetings?${qs.toString()}`);
}

export async function getMeeting(id: string) {
  return fetchJson<MeetingDetail>(`/api/v1/meetings/${id}`);
}

export async function updateMeeting(id: string, data: Partial<Omit<Meeting, "id" | "created_at" | "updated_at">>) {
  return fetchJson<Meeting>(`/api/v1/meetings/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function deleteMeeting(id: string) {
  return fetchJson<void>(`/api/v1/meetings/${id}`, { method: "DELETE" });
}

// ── Dashboard ─────────────────────────────────────────

export interface DashboardStats {
  total_meetings: number;
  total_rooms: number;
  total_participants: number;
  open_action_items: number;
}

export async function getDashboardStats() {
  return fetchJson<DashboardStats>("/api/v1/dashboard");
}

export { ApiError };
