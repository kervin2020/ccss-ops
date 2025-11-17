'use client'

import { useState, useEffect } from 'react'
import { payrollsAPI, agentsAPI } from '@/lib/api'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'
import { Plus, DollarSign } from 'lucide-react'

interface Payroll {
  id: number
  agent_id: number
  pay_period_start: string
  pay_period_end: string
  total_hours: number
  hourly_rate: number
  gross_pay: number
  deductions: number
  net_pay: number
  payment_status: string
}

export default function PayrollsPage() {
  const [payrolls, setPayrolls] = useState<Payroll[]>([])
  const [agents, setAgents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    agent_id: '',
    pay_period_start: '',
    pay_period_end: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [payData, agentsData] = await Promise.all([
        payrollsAPI.getAll(),
        agentsAPI.getAll()
      ])
      setPayrolls(payData)
      setAgents(agentsData)
    } catch (error) {
      alert('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await payrollsAPI.create(formData)
      resetForm()
      loadData()
    } catch (error) {
      alert('Failed to create payroll')
    }
  }

  const resetForm = () => {
    setFormData({ agent_id: '', pay_period_start: '', pay_period_end: '' })
    setShowForm(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Payrolls</h2>
        <CustomButton onClick={() => setShowForm(true)} variant="primary"><Plus className="w-4 h-4" /> Generate Payroll</CustomButton>
      </div>

      {showForm && (
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4">Generate Payroll</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="agent_id">Agent</Label>
              <select id="agent_id" value={formData.agent_id} onChange={(e) => setFormData({ ...formData, agent_id: e.target.value })} className="w-full p-2 border rounded" required>
                <option value="">Select agent</option>
                {agents.map(a => <option key={a.id} value={a.id}>{a.name} {a.surname}</option>)}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="pay_period_start">Period Start</Label>
                <Input type="date" id="pay_period_start" value={formData.pay_period_start} onChange={(e) => setFormData({ ...formData, pay_period_start: e.target.value })} required />
              </div>
              <div>
                <Label htmlFor="pay_period_end">Period End</Label>
                <Input type="date" id="pay_period_end" value={formData.pay_period_end} onChange={(e) => setFormData({ ...formData, pay_period_end: e.target.value })} required />
              </div>
            </div>
            <div className="flex gap-2">
              <CustomButton type="submit" variant="primary">Generate</CustomButton>
              <CustomButton type="button" variant="outline" onClick={resetForm}>Cancel</CustomButton>
            </div>
          </form>
        </Card>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-2 text-muted-foreground">Loading payrolls...</p>
        </div>
      ) : payrolls.length === 0 ? (
        <Card className="p-12 text-center">
          <DollarSign className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No payrolls found</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {payrolls.map((payroll) => {
            const agent = agents.find(a => a.id === payroll.agent_id)
            return (
              <Card key={payroll.id} className="p-5 hover:shadow-lg transition-shadow">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-foreground">{agent?.name} {agent?.surname}</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      {new Date(payroll.pay_period_start).toLocaleDateString()} - {new Date(payroll.pay_period_end).toLocaleDateString()}
                    </p>
                  </div>
                  <span className="px-2 py-1 text-xs rounded-full font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">{payroll.payment_status}</span>
                </div>
                <div className="space-y-2 text-sm mb-4 pb-4 border-b border-border/50">
                  <p className="text-foreground"><span className="text-muted-foreground">Hours:</span> {payroll.total_hours.toFixed(2)}</p>
                  <p className="text-foreground"><span className="text-muted-foreground">Rate:</span> ${payroll.hourly_rate.toFixed(2)}/hr</p>
                  <p className="text-foreground"><span className="text-muted-foreground">Gross:</span> ${payroll.gross_pay.toFixed(2)}</p>
                  <p className="text-foreground"><span className="text-muted-foreground">Deductions:</span> ${payroll.deductions.toFixed(2)}</p>
                </div>
                <div className="pt-2">
                  <p className="font-semibold text-xl text-foreground">Net Pay: ${payroll.net_pay.toFixed(2)}</p>
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

