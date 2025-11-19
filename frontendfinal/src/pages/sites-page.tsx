'use client'

import { useState, useEffect } from 'react'
import { sitesAPI, clientsAPI } from '@/lib/api'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'
import { Plus, Edit, Trash2, MapPin } from 'lucide-react'

interface Site {
  id: number
  client_id: number
  site_name: string
  address: string
  city?: string
  required_agents: number
  site_status: string
}

export default function SitesPage() {
  const [sites, setSites] = useState<Site[]>([])
  const [clients, setClients] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingSite, setEditingSite] = useState<Site | null>(null)
  const [formData, setFormData] = useState({
    client_id: '',
    site_name: '',
    address: '',
    city: '',
    required_agents: '1',
    site_status: 'active'
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [sitesData, clientsData] = await Promise.all([
        sitesAPI.getAll(),
        clientsAPI.getAll()
      ])
      setSites(sitesData)
      setClients(clientsData)
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
        ...formData,
        client_id: parseInt(formData.client_id),
        required_agents: parseInt(formData.required_agents)
      }
      if (editingSite) {
        await sitesAPI.update(editingSite.id, payload)
      } else {
        await sitesAPI.create(payload)
      }
      resetForm()
      loadData()
    } catch (error) {
      alert('Failed to save site')
    }
  }

  const resetForm = () => {
    setFormData({ client_id: '', site_name: '', address: '', city: '', required_agents: '1', site_status: 'active' })
    setEditingSite(null)
    setShowForm(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Sites</h2>
        <CustomButton onClick={() => setShowForm(true)} variant="primary"><Plus className="w-4 h-4" /> Add Site</CustomButton>
      </div>

      {showForm && (
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4">{editingSite ? 'Edit' : 'Add'} Site</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="client_id">Client</Label>
              <select id="client_id" value={formData.client_id} onChange={(e) => setFormData({ ...formData, client_id: e.target.value })} className="w-full p-2 border rounded" required>
                <option value="">Select client</option>
                {clients.map(c => <option key={c.id} value={c.id}>{c.company_name}</option>)}
              </select>
            </div>
            <div>
              <Label htmlFor="site_name">Site Name</Label>
              <Input id="site_name" value={formData.site_name} onChange={(e) => setFormData({ ...formData, site_name: e.target.value })} required />
            </div>
            <div>
              <Label htmlFor="address">Address</Label>
              <Input id="address" value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} required />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="city">City</Label>
                <Input id="city" value={formData.city} onChange={(e) => setFormData({ ...formData, city: e.target.value })} />
              </div>
              <div>
                <Label htmlFor="required_agents">Required Agents</Label>
                <Input type="number" id="required_agents" value={formData.required_agents} onChange={(e) => setFormData({ ...formData, required_agents: e.target.value })} required />
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
          <p className="mt-2 text-muted-foreground">Loading sites...</p>
        </div>
      ) : sites.length === 0 ? (
        <Card className="p-12 text-center">
          <MapPin className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No sites found</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sites.map((site) => {
            const client = clients.find(c => c.id === site.client_id)
            return (
              <Card key={site.id} className="p-5 hover:shadow-lg transition-shadow">
                <h3 className="font-semibold text-lg mb-2 text-foreground">{site.site_name}</h3>
                <p className="text-sm text-muted-foreground mb-2">{client?.company_name}</p>
                <p className="text-sm mb-2 text-foreground">{site.address}</p>
                <p className="text-sm mb-4 pb-4 border-b border-border/50"><span className="text-muted-foreground">Required:</span> {site.required_agents} agents</p>
                <div className="flex gap-2">
                  <CustomButton variant="outline" size="sm" className="flex-1"><Edit className="w-4 h-4 mr-1" /> Edit</CustomButton>
                  <CustomButton variant="outline" size="sm" className="text-red-600 hover:text-red-700"><Trash2 className="w-4 h-4" /></CustomButton>
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

