'use client'

import { useState } from 'react'
import { CustomButton } from '@/components/buttons/custom-button'
import Sidebar from '@/components/sidebar'
import OverviewPage from '@/pages/overview-page'
import AnalyticsPage from '@/pages/analytics-page'
import SettingsPage from '@/pages/settings-page'
import ButtonShowcase from '@/components/buttons/button-showcase'

interface DashboardProps {
  onLogout: () => void
}

export default function Dashboard({ onLogout }: DashboardProps) {
  const [currentPage, setCurrentPage] = useState('overview')

  const renderPage = () => {
    switch (currentPage) {
      case 'overview':
        return <OverviewPage />
      case 'analytics':
        return <AnalyticsPage />
      case 'settings':
        return <SettingsPage />
      case 'buttons':
        return <ButtonShowcase />
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
