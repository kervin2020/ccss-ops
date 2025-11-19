'use client'

import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { agentsAPI, clientsAPI, sitesAPI, attendancesAPI, payrollsAPI } from '@/lib/api'
import { Users, Building2, MapPin, Clock, DollarSign, TrendingUp } from 'lucide-react'

export default function OverviewPage() {
  const [stats, setStats] = useState({
    agents: 0,
    clients: 0,
    sites: 0,
    attendances: 0,
    payrolls: 0,
    totalPayroll: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      const [agents, clients, sites, attendances, payrolls] = await Promise.all([
        agentsAPI.getAll(),
        clientsAPI.getAll(),
        sitesAPI.getAll(),
        attendancesAPI.getAll(),
        payrollsAPI.getAll()
      ])
      
      const totalPayroll = payrolls.reduce((sum: number, p: any) => sum + (p.net_pay || 0), 0)
      
      setStats({
        agents: agents.length,
        clients: clients.length,
        sites: sites.length,
        attendances: attendances.length,
        payrolls: payrolls.length,
        totalPayroll
      })
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    { label: 'Total Agents', value: stats.agents, icon: Users, color: 'text-blue-600' },
    { label: 'Clients', value: stats.clients, icon: Building2, color: 'text-green-600' },
    { label: 'Sites', value: stats.sites, icon: MapPin, color: 'text-purple-600' },
    { label: 'Attendances', value: stats.attendances, icon: Clock, color: 'text-orange-600' },
    { label: 'Payrolls', value: stats.payrolls, icon: DollarSign, color: 'text-emerald-600' },
    { label: 'Total Payroll', value: `$${stats.totalPayroll.toFixed(2)}`, icon: TrendingUp, color: 'text-red-600' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-foreground">Dashboard Overview</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Welcome back! Here's your system overview.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading statistics...</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {statCards.map((stat) => {
              const Icon = stat.icon
              return (
                <Card key={stat.label} className="border-border/50 p-6 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between mb-4">
                    <Icon className={`w-8 h-8 ${stat.color}`} />
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                    <p className="text-3xl font-bold text-foreground">{stat.value}</p>
                  </div>
                </Card>
              )
            })}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card className="border-border/50 p-6">
              <h3 className="font-bold text-foreground mb-4">Quick Actions</h3>
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">
                  • Manage agents, clients, and sites from the sidebar
                </p>
                <p className="text-sm text-muted-foreground">
                  • Record attendance and generate payrolls
                </p>
                <p className="text-sm text-muted-foreground">
                  • Review and approve attendance corrections
                </p>
              </div>
            </Card>

            <Card className="border-border/50 p-6">
              <h3 className="font-bold text-foreground mb-4">System Status</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-foreground">Database</span>
                  <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-800">Connected</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-foreground">API</span>
                  <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-800">Active</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-foreground">Authentication</span>
                  <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-800">Enabled</span>
                </div>
              </div>
            </Card>
          </div>
        </>
      )}
    </div>
  )
}
