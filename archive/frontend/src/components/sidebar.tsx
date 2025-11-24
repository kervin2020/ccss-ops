import React from "react";
import { NavLink } from "react-router-dom";
import {
    Home,
    Users,
    UserCheck,
    Building2,
    CalendarCheck,
    Pencil,
    Wallet,
    BarChart3,
    Settings as SettingsIcon,
    ChevronLeft,
} from "lucide-react";
import classNames from "classnames";

type SidebarProps = {
    collapsed: boolean;
    setCollapsed: (value: boolean) => void;
};

export default function Sidebar({ collapsed, setCollapsed }: SidebarProps) {
    const navItems = [
        { to: "/dashboard", label: "Overview", icon: <Home size={20} /> },
        { to: "/dashboard/agents", label: "Agents", icon: <Users size={20} /> },
        { to: "/dashboard/clients", label: "Clients", icon: <UserCheck size={20} /> },
        { to: "/dashboard/sites", label: "Sites", icon: <Building2 size={20} /> },
        { to: "/dashboard/attendances", label: "Attendances", icon: <CalendarCheck size={20} /> },
        { to: "/dashboard/corrections", label: "Corrections", icon: <Pencil size={20} /> },
        { to: "/dashboard/payrolls", label: "Payrolls", icon: <Wallet size={20} /> },
        { to: "/dashboard/analytics", label: "Analytics", icon: <BarChart3 size={20} /> },
        { to: "/dashboard/settings", label: "Settings", icon: <SettingsIcon size={20} /> },
    ];

    return (
        <aside
            className={classNames(
                "h-screen bg-gray-900 text-white transition-all flex flex-col",
                collapsed ? "w-20" : "w-64"
            )}
        >
            {/* SIDEBAR HEADER */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
                {!collapsed && <h1 className="text-xl font-bold">CCSS Ops</h1>}

                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-2 rounded hover:bg-gray-700 transition"
                >
                    <ChevronLeft
                        className={classNames(
                            "transition-transform",
                            collapsed ? "rotate-180" : ""
                        )}
                    />
                </button>
            </div>

            {/* NAVIGATION */}
            <nav className="flex flex-col mt-2 gap-1">
                {navItems.map((item) => (
                    <NavLink
                        key={item.to}
                        to={item.to}
                        end={item.to === "/dashboard"}
                        className={({ isActive }) =>
                            classNames(
                                "flex items-center px-4 py-3 gap-3 hover:bg-gray-800 transition",
                                isActive ? "bg-gray-800" : ""
                            )
                        }
                    >
                        {/* ICON */}
                        <span>{item.icon}</span>

                        {/* LABEL (hidden when collapsed) */}
                        {!collapsed && <span className="text-sm">{item.label}</span>}
                    </NavLink>
                ))}
            </nav>

            {/* FOOTER */}
            <div className="mt-auto p-4 border-t border-gray-700">
                {!collapsed ? (
                    <>
                        <div className="text-sm text-gray-300">Logged in as</div>
                        <div className="font-medium">Kervin</div>
                    </>
                ) : (
                    <div className="mx-auto text-gray-300 text-xs">KR</div>
                )}
            </div>
        </aside>
    );
}
