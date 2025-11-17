'use client'

import { useState, useEffect } from 'react'
import { clientsAPI } from '@/lib/api'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'
import { Plus, Edit, Trash2, Search, Building2 } from 'lucide-react'

interface Client {
  id: number
  company_name: string
  primary_contact_name: string
  primary_contact_phone: string
  primary_contact_email: string
  address: string
  city: string
  contract_status: string
}

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingClient, setEditingClient] = useState<Client | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [formData, setFormData] = useState({
    company_name: '',
    primary_contact_name: '',
    primary_contact_phone: '',
    primary_contact_email: '',
    address: '',
    city: '',
    contract_status: 'active'
  })

  useEffect(() => {
    loadClients()
  }, [])

  const loadClients = async () => {
    try {
      setLoading(true)
      const data = await clientsAPI.getAll()
      setClients(data)
    } catch (error) {
      alert('Failed to load clients')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingClient) {
        await clientsAPI.update(editingClient.id, formData)
      } else {
        await clientsAPI.create(formData)
      }
      resetForm()
      loadClients()
    } catch (error) {
      alert('Failed to save client')
    }
  }

  const handleEdit = (client: Client) => {
    setEditingClient(client)
    setFormData({
      company_name: client.company_name,
      primary_contact_name: client.primary_contact_name,
      primary_contact_phone: client.primary_contact_phone,
      primary_contact_email: client.primary_contact_email,
      address: client.address,
      city: client.city,
      contract_status: client.contract_status
    })
    setShowForm(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure?')) return
    try {
      await clientsAPI.delete(id)
      loadClients()
    } catch (error) {
      alert('Failed to delete client')
    }
  }

  const resetForm = () => {
    setFormData({
      company_name: '',
      primary_contact_name: '',
      primary_contact_phone: '',
      primary_contact_email: '',
      address: '',
      city: '',
      contract_status: 'active'
    })
    setEditingClient(null)
    setShowForm(false)
  }

  const filteredClients = clients.filter(client =>
    client.company_name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Clients</h2>
        <CustomButton onClick={() => setShowForm(true)} variant="primary">
          <Plus className="w-4 h-4" /> Add Client
        </CustomButton>
      </div>

      {showForm && (
        <Card className="p-6 border-2 border-primary/20">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold">{editingClient ? 'Edit' : 'Add'} Client</h3>
            <CustomButton variant="ghost" size="sm" onClick={resetForm}>×</CustomButton>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="company_name">Company Name</Label>
              <Input id="company_name" value={formData.company_name} onChange={(e) => setFormData({ ...formData, company_name: e.target.value })} required />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="primary_contact_name">Contact Name</Label>
                <Input id="primary_contact_name" value={formData.primary_contact_name} onChange={(e) => setFormData({ ...formData, primary_contact_name: e.target.value })} required />
              </div>
              <div>
                <Label htmlFor="primary_contact_phone">Phone</Label>
                <Input id="primary_contact_phone" value={formData.primary_contact_phone} onChange={(e) => setFormData({ ...formData, primary_contact_phone: e.target.value })} required />
              </div>
            </div>
            <div>
              <Label htmlFor="primary_contact_email">Email</Label>
              <Input type="email" id="primary_contact_email" value={formData.primary_contact_email} onChange={(e) => setFormData({ ...formData, primary_contact_email: e.target.value })} required />
            </div>
            <div>
              <Label htmlFor="address">Address</Label>
              <Input id="address" value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} required />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="city">City</Label>
                <Input id="city" value={formData.city} onChange={(e) => setFormData({ ...formData, city: e.target.value })} required />
              </div>
              <div>
                <Label htmlFor="contract_status">Status</Label>
                <Input id="contract_status" value={formData.contract_status} onChange={(e) => setFormData({ ...formData, contract_status: e.target.value })} />
              </div>
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
        <Input placeholder="Search clients..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="pl-10" />
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-2 text-muted-foreground">Loading clients...</p>
        </div>
      ) : filteredClients.length === 0 ? (
        <Card className="p-12 text-center">
          <Building2 className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No clients found</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredClients.map((client) => (
            <Card key={client.id} className="p-5 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold text-lg text-foreground flex-1">{client.company_name}</h3>
                <span className="px-2 py-1 text-xs rounded-full font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">{client.contract_status}</span>
              </div>
              <div className="space-y-2 text-sm mb-4 pb-4 border-b border-border/50">
                <p className="text-foreground"><span className="text-muted-foreground">Contact:</span> {client.primary_contact_name}</p>
                <p className="text-foreground"><span className="text-muted-foreground">Phone:</span> {client.primary_contact_phone}</p>
                <p className="text-foreground"><span className="text-muted-foreground">Email:</span> {client.primary_contact_email}</p>
                <p className="text-muted-foreground">{client.city}</p>
              </div>
              <div className="flex gap-2">
                <CustomButton variant="outline" size="sm" onClick={() => handleEdit(client)} className="flex-1"><Edit className="w-4 h-4 mr-1" /> Edit</CustomButton>
                <CustomButton variant="outline" size="sm" onClick={() => handleDelete(client.id)} className="text-red-600 hover:text-red-700"><Trash2 className="w-4 h-4" /></CustomButton>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

