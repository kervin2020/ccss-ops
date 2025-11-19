'use client'

import { useState } from 'react'
import { CustomButton } from '@/components/buttons/custom-button'
import Sidebar from '@/components/sidebar'
import OverviewPage from '@/pages/overview-page'
import AgentsPage from '@/pages/agents-page'
import ClientsPage from '@/pages/clients-page'
import SitesPage from '@/pages/sites-page'
import AttendancesPage from '@/pages/attendances-page'
import CorrectionsPage from '@/pages/corrections-page'
import PayrollsPage from '@/pages/payrolls-page'
import AnalyticsPage from '@/pages/analytics-page'
import SettingsPage from '@/pages/settings-page'

interface DashboardProps {
  onLogout: () => void
}

export default function Dashboard({ onLogout }: DashboardProps) {
  const [currentPage, setCurrentPage] = useState('overview')

  const renderPage = () => {
    switch (currentPage) {
      case 'overview':
        return <OverviewPage />
      case 'agents':
        return <AgentsPage />
      case 'clients':
        return <ClientsPage />
      case 'sites':
        return <SitesPage />
      case 'attendances':
        return <AttendancesPage />
      case 'corrections':
        return <CorrectionsPage />
      case 'payrolls':
        return <PayrollsPage />
      case 'analytics':
        return <AnalyticsPage />
      case 'settings':
        return <SettingsPage />
      default:
        return <OverviewPage />
    }
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar currentPage={currentPage} onPageChange={setCurrentPage} />

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Header */}
        <div className="sticky top-0 z-10 bg-card/95 backdrop-blur-sm border-b border-border/50 px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <CustomButton
            onClick={onLogout}
            variant="outline"
            size="md"
          >
            Sign Out
          </CustomButton>
        </div>

        {/* Page Content */}
        <div className="p-6">
          {renderPage()}
        </div>
      </div>
    </div>
  )
}
