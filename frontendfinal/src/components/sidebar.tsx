'use client'

import { useState } from 'react'
import {
  BarChart3, Settings, Home, Users, Building2, MapPin, Clock, FileEdit, DollarSign, ChevronLeft, ChevronRight
} from 'lucide-react'
import { CustomButton } from '@/components/buttons/custom-button'

interface SidebarProps {
  currentPage: string
  onPageChange: (page: string) => void
}

export default function Sidebar({ currentPage, onPageChange }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)

  const menuItems = [
    { id: 'overview', label: 'Overview', icon: Home },
    { id: 'agents', label: 'Agents', icon: Users },
    { id: 'clients', label: 'Clients', icon: Building2 },
    { id: 'sites', label: 'Sites', icon: MapPin },
    { id: 'attendances', label: 'Attendances', icon: Clock },
    { id: 'corrections', label: 'Corrections', icon: FileEdit },
    { id: 'payrolls', label: 'Payrolls', icon: DollarSign },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className={`flex flex-col h-screen bg-sidebar border-r border-sidebar-border transition-width duration-300 ${isCollapsed ? 'w-20' : 'w-64'}`}>
      {/* Logo + Collapse Button */}
      <div className="flex items-center justify-between px-4 py-6 border-b border-sidebar-border">
        {!isCollapsed && <div className="text-xl font-bold text-sidebar-foreground">CCSS Ops</div>}
        <CustomButton
          onClick={() => setIsCollapsed(!isCollapsed)}
          variant="ghost"
          className="p-1"
        >
          {isCollapsed ? <ChevronRight className="w-8 h-8" /> : <ChevronLeft className="w-8 h-8" />}
        </CustomButton>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-2 py-6 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id

          return (
            <CustomButton
              key={item.id}
              onClick={() => onPageChange(item.id)}
              variant={isActive ? 'primary' : 'ghost'}
              className={`w-full justify-start gap-3 px-2 ${isActive ? 'text-primary-foreground' : 'text-sidebar-foreground'
                }`}
            >
              <Icon className="w-5 h-5" />
              {!isCollapsed && <span className="font-medium">{item.label}</span>}
            </CustomButton>
          )
        })}
      </nav>

      {/* Footer */}
      {!isCollapsed && (
        <div className="px-4 py-6 border-t border-sidebar-border text-xs text-sidebar-foreground/60">
          <p>© 2025 Your App. All rights reserved.</p>
        </div>
      )}
    </div>
  )
}
