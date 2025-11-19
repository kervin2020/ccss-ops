import React, { useState } from "react";
import Sidebar from "../Components/Sidebar";
import { Outlet } from "react-router-dom";

export default function DashboardLayout() {
    const [collapsed, setCollapsed] = useState(false);

    return (
        <div className="flex min-h-screen bg-gray-100">
            <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />

            {/* PAGE CONTENT */}
            <main className="flex-1 p-6">
                <Outlet />
            </main>
        </div>
    );
}
