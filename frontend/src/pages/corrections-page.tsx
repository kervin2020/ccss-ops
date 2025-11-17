'use client'

import { useState, useEffect } from 'react'
import { correctionsAPI, attendancesAPI, agentsAPI } from '@/lib/api'
import { CustomButton } from '@/components/buttons/custom-button'
import { Card } from '@/components/ui/card'
import { Check, X } from 'lucide-react'

interface Correction {
  id: number
  attendance_id: number
  agent_id: number
  reason: string
  correction_status: string
  requested_clock_in?: string
  requested_clock_out?: string
}

export default function CorrectionsPage() {
  const [corrections, setCorrections] = useState<Correction[]>([])
  const [attendances, setAttendances] = useState<any[]>([])
  const [agents, setAgents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [corrData, attData, agentsData] = await Promise.all([
        correctionsAPI.getAll(),
        attendancesAPI.getAll(),
        agentsAPI.getAll()
      ])
      setCorrections(corrData)
      setAttendances(attData)
      setAgents(agentsData)
    } catch (error) {
      alert('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (id: number) => {
    try {
      await correctionsAPI.approve(id)
      loadData()
    } catch (error) {
      alert('Failed to approve correction')
    }
  }

  const handleReject = async (id: number) => {
    try {
      await correctionsAPI.reject(id, 'Rejected by admin')
      loadData()
    } catch (error) {
      alert('Failed to reject correction')
    }
  }

  const pendingCorrections = corrections.filter(c => c.correction_status === 'pending')

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">Corrections</h2>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-2 text-muted-foreground">Loading corrections...</p>
        </div>
      ) : (
        <div className="space-y-4">
          {pendingCorrections.length === 0 ? (
            <Card className="p-6 text-center">No pending corrections</Card>
          ) : (
            pendingCorrections.map((corr) => {
              const agent = agents.find(a => a.id === corr.agent_id)
              const attendance = attendances.find(a => a.id === corr.attendance_id)
              return (
                <Card key={corr.id} className="p-5 hover:shadow-lg transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg text-foreground">{agent?.name} {agent?.surname}</h3>
                      <p className="text-sm text-muted-foreground mt-1">Attendance: {attendance && new Date(attendance.attendance_date).toLocaleDateString()}</p>
                    </div>
                    <span className="px-2 py-1 text-xs rounded-full font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">Pending</span>
                  </div>
                  <div className="space-y-2 text-sm mb-4 pb-4 border-b border-border/50">
                    <p className="text-foreground"><span className="text-muted-foreground">Reason:</span> {corr.reason}</p>
                    {corr.requested_clock_in && <p className="text-foreground"><span className="text-muted-foreground">Requested In:</span> {new Date(corr.requested_clock_in).toLocaleString()}</p>}
                    {corr.requested_clock_out && <p className="text-foreground"><span className="text-muted-foreground">Requested Out:</span> {new Date(corr.requested_clock_out).toLocaleString()}</p>}
                  </div>
                  <div className="flex gap-2">
                    <CustomButton variant="primary" size="sm" onClick={() => handleApprove(corr.id)} className="flex-1">
                      <Check className="w-4 h-4 mr-1" /> Approve
                    </CustomButton>
                    <CustomButton variant="outline" size="sm" onClick={() => handleReject(corr.id)} className="flex-1">
                      <X className="w-4 h-4 mr-1" /> Reject
                    </CustomButton>
                  </div>
                </Card>
              )
            })
          )}
        </div>
      )}
    </div>
  )
}

