import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout.tsx'
import Overview from './pages/Overview-page.tsx'
import Agents from './pages/Agents-page.tsx'
import Clients from './pages/Clients-page.tsx'
import Sites from './pages/Sites-page.tsx'
import Attendances from './pages/Attendances-page.tsx'
import Corrections from './pages/Corrections-page.tsx'
import Payrolls from './pages/Payrolls-page.tsx'
import Analytics from './pages/Analytics-page.tsx'
import Settings from './pages/Settings-page.tsx'
import './App.css'

export default function App() {


  return (
    // <>
    //   <div className='text-red-500'>ccss Ops</div>
    //   <div>Sidebar</div>
    //   <div><Overview /></div>
    //   <div><Agents /></div>
    //   <div><Clients /></div>
    //   <div><Sites /></div>
    //   <div><Attendances /></div>
    //   <div><Corrections /></div>
    //   <div><Payrolls /></div>
    //   <div><Analytics /></div>
    //   <div><Settings /></div>
    // </>
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard/*" element={<DashboardLayout />}>
        <Route index element={<Overview />} />
        <Route path="agents" element={<Agents />} />
        <Route path="clients" element={<Clients />} />
        <Route path="sites" element={<Sites />} />
        <Route path="attendances" element={<Attendances />} />
        <Route path="corrections" element={<Corrections />} />
        <Route path="payrolls" element={<Payrolls />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="settings" element={<Settings />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<div className='p-6'>404 - Not Found</div>} />
    </Routes>
  )
}





