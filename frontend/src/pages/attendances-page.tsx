'use client'

import { useState, useEffect } from 'react'
import { attendancesAPI, agentsAPI, sitesAPI } from '@/lib/api'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'
import { Plus, Calendar } from 'lucide-react'

interface Attendance {
  id: number
  agent_id: number
  site_id: number
  attendance_date: string
  clock_in_time?: string
  clock_out_time?: string
  total_hours: number
  attendance_status: string
}

export default function AttendancesPage() {
  const [attendances, setAttendances] = useState<Attendance[]>([])
  const [agents, setAgents] = useState<any[]>([])
  const [sites, setSites] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    agent_id: '',
    site_id: '',
    attendance_date: new Date().toISOString().split('T')[0],
    clock_in_time: '',
    clock_out_time: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [attData, agentsData, sitesData] = await Promise.all([
        attendancesAPI.getAll(),
        agentsAPI.getAll(),
        sitesAPI.getAll()
      ])
      setAttendances(attData)
      setAgents(agentsData)
      setSites(sitesData)
    } catch (error) {
      alert('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const payload = {
        agent_id: parseInt(formData.agent_id),
        site_id: parseInt(formData.site_id),
        attendance_date: formData.attendance_date,
        clock_in_time: formData.clock_in_time ? `${formData.attendance_date}T${formData.clock_in_time}` : undefined,
        clock_out_time: formData.clock_out_time ? `${formData.attendance_date}T${formData.clock_out_time}` : undefined
      }
      await attendancesAPI.create(payload)
      resetForm()
      loadData()
    } catch (error) {
      alert('Failed to save attendance')
    }
  }

  const resetForm = () => {
    setFormData({ agent_id: '', site_id: '', attendance_date: new Date().toISOString().split('T')[0], clock_in_time: '', clock_out_time: '' })
    setShowForm(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Attendances</h2>
        <CustomButton onClick={() => setShowForm(true)} variant="primary"><Plus className="w-4 h-4" /> Add Attendance</CustomButton>
      </div>

      {showForm && (
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4">Add Attendance</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="agent_id">Agent</Label>
                <select id="agent_id" value={formData.agent_id} onChange={(e) => setFormData({ ...formData, agent_id: e.target.value })} className="w-full p-2 border rounded" required>
                  <option value="">Select agent</option>
                  {agents.map(a => <option key={a.id} value={a.id}>{a.name} {a.surname}</option>)}
                </select>
              </div>
              <div>
                <Label htmlFor="site_id">Site</Label>
                <select id="site_id" value={formData.site_id} onChange={(e) => setFormData({ ...formData, site_id: e.target.value })} className="w-full p-2 border rounded" required>
                  <option value="">Select site</option>
                  {sites.map(s => <option key={s.id} value={s.id}>{s.site_name}</option>)}
                </select>
              </div>
            </div>
            <div>
              <Label htmlFor="attendance_date">Date</Label>
              <Input type="date" id="attendance_date" value={formData.attendance_date} onChange={(e) => setFormData({ ...formData, attendance_date: e.target.value })} required />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="clock_in_time">Clock In</Label>
                <Input type="time" id="clock_in_time" value={formData.clock_in_time} onChange={(e) => setFormData({ ...formData, clock_in_time: e.target.value })} />
              </div>
              <div>
                <Label htmlFor="clock_out_time">Clock Out</Label>
                <Input type="time" id="clock_out_time" value={formData.clock_out_time} onChange={(e) => setFormData({ ...formData, clock_out_time: e.target.value })} />
              </div>
            </div>
            <div className="flex gap-2">
              <CustomButton type="submit" variant="primary">Save</CustomButton>
              <CustomButton type="button" variant="outline" onClick={resetForm}>Cancel</CustomButton>
            </div>
          </form>
        </Card>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-2 text-muted-foreground">Loading attendances...</p>
        </div>
      ) : attendances.length === 0 ? (
        <Card className="p-12 text-center">
          <Clock className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No attendances found</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {attendances.map((att) => {
            const agent = agents.find(a => a.id === att.agent_id)
            const site = sites.find(s => s.id === att.site_id)
            return (
              <Card key={att.id} className="p-5 hover:shadow-lg transition-shadow">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-foreground">{agent?.name} {agent?.surname}</h3>
                    <p className="text-sm text-muted-foreground mt-1">{site?.site_name}</p>
                  </div>
                  <span className="px-2 py-1 text-xs rounded-full font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">{att.attendance_status}</span>
                </div>
                <div className="space-y-2 text-sm pb-4 border-b border-border/50">
                  <p className="text-foreground"><span className="text-muted-foreground">Date:</span> {new Date(att.attendance_date).toLocaleDateString()}</p>
                  {att.clock_in_time && <p className="text-foreground"><span className="text-muted-foreground">In:</span> {new Date(att.clock_in_time).toLocaleTimeString()}</p>}
                  {att.clock_out_time && <p className="text-foreground"><span className="text-muted-foreground">Out:</span> {new Date(att.clock_out_time).toLocaleTimeString()}</p>}
                  <p className="text-foreground font-semibold"><span className="text-muted-foreground">Hours:</span> {att.total_hours.toFixed(2)}</p>
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

