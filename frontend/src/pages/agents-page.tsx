'use client'

import { useState, useEffect } from 'react'
import { agentsAPI } from '@/lib/api'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'
import { Plus, Edit, Trash2, Search, Users } from 'lucide-react'

interface Agent {
  id: number
  name: string
  surname: string
  cin: string
  phone?: string
  address?: string
  hourly_rate: number
  status: string
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingAgent, setEditingAgent] = useState<Agent | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    cin: '',
    phone: '',
    address: '',
    hourly_rate: '',
    status: 'actif'
  })

  useEffect(() => {
    loadAgents()
  }, [])

  const loadAgents = async () => {
    try {
      setLoading(true)
      const data = await agentsAPI.getAll()
      setAgents(data)
    } catch (error) {
      alert('Failed to load agents: ' + (error instanceof Error ? error.message : 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const payload = {
        ...formData,
        hourly_rate: parseFloat(formData.hourly_rate)
      }
      
      if (editingAgent) {
        await agentsAPI.update(editingAgent.id, payload)
      } else {
        await agentsAPI.create(payload)
      }
      
      resetForm()
      loadAgents()
    } catch (error) {
      alert('Failed to save agent: ' + (error instanceof Error ? error.message : 'Unknown error'))
    }
  }

  const handleEdit = (agent: Agent) => {
    setEditingAgent(agent)
    setFormData({
      name: agent.name,
      surname: agent.surname,
      cin: agent.cin,
      phone: agent.phone || '',
      address: agent.address || '',
      hourly_rate: agent.hourly_rate.toString(),
      status: agent.status
    })
    setShowForm(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this agent?')) return
    
    try {
      await agentsAPI.delete(id)
      loadAgents()
    } catch (error) {
      alert('Failed to delete agent: ' + (error instanceof Error ? error.message : 'Unknown error'))
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      surname: '',
      cin: '',
      phone: '',
      address: '',
      hourly_rate: '',
      status: 'actif'
    })
    setEditingAgent(null)
    setShowForm(false)
  }

  const filteredAgents = agents.filter(agent =>
    `${agent.name} ${agent.surname} ${agent.cin}`.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Agents</h2>
        <CustomButton onClick={() => setShowForm(true)} variant="primary" size="md">
          <Plus className="w-4 h-4" />
          Add Agent
        </CustomButton>
      </div>

      {showForm && (
        <Card className="p-6 border-2 border-primary/20">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold">{editingAgent ? 'Edit' : 'Add'} Agent</h3>
            <CustomButton variant="ghost" size="sm" onClick={resetForm}>×</CustomButton>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div>
                <Label htmlFor="surname">Surname</Label>
                <Input
                  id="surname"
                  value={formData.surname}
                  onChange={(e) => setFormData({ ...formData, surname: e.target.value })}
                  required
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="cin">CIN</Label>
                <Input
                  id="cin"
                  value={formData.cin}
                  onChange={(e) => setFormData({ ...formData, cin: e.target.value })}
                  required
                />
              </div>
              <div>
                <Label htmlFor="hourly_rate">Hourly Rate</Label>
                <Input
                  id="hourly_rate"
                  type="number"
                  step="0.01"
                  value={formData.hourly_rate}
                  onChange={(e) => setFormData({ ...formData, hourly_rate: e.target.value })}
                  required
                />
              </div>
            </div>
            <div>
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="address">Address</Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              />
            </div>
            <div className="flex gap-2">
              <CustomButton type="submit" variant="primary">Save</CustomButton>
              <CustomButton type="button" variant="outline" onClick={resetForm}>Cancel</CustomButton>
            </div>
          </form>
        </Card>
      )}

      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
        <Input
          placeholder="Search agents..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
        />
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-2 text-muted-foreground">Loading agents...</p>
        </div>
      ) : filteredAgents.length === 0 ? (
        <Card className="p-12 text-center">
          <Users className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No agents found</p>
          {searchTerm && (
            <p className="text-sm text-muted-foreground mt-2">Try adjusting your search</p>
          )}
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredAgents.map((agent) => (
            <Card key={agent.id} className="p-5 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg text-foreground">{agent.name} {agent.surname}</h3>
                  <p className="text-sm text-muted-foreground mt-1">CIN: {agent.cin}</p>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                  agent.status === 'actif' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                    : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
                }`}>
                  {agent.status}
                </span>
              </div>
              <div className="space-y-2 text-sm mb-4 pb-4 border-b border-border/50">
                {agent.phone && (
                  <p className="text-foreground">
                    <span className="text-muted-foreground">Phone:</span> {agent.phone}
                  </p>
                )}
                <p className="text-foreground font-medium">
                  <span className="text-muted-foreground">Rate:</span> ${agent.hourly_rate.toFixed(2)}/hr
                </p>
                {agent.address && (
                  <p className="text-muted-foreground text-xs truncate">{agent.address}</p>
                )}
              </div>
              <div className="flex gap-2">
                <CustomButton
                  variant="outline"
                  size="sm"
                  onClick={() => handleEdit(agent)}
                  className="flex-1"
                >
                  <Edit className="w-4 h-4 mr-1" />
                  Edit
                </CustomButton>
                <CustomButton
                  variant="outline"
                  size="sm"
                  onClick={() => handleDelete(agent.id)}
                  className="text-red-600 hover:text-red-700 hover:border-red-300"
                >
                  <Trash2 className="w-4 h-4" />
                </CustomButton>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

