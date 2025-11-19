export default function Analytics() {
    return (
        <div className="p-6 space-y-6">
            <h1 className="text-3xl font-bold">Analytics</h1>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Weekly Attendance</p>
                    <p className="text-2xl font-semibold mt-2">92%</p>
                </div>

                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Average Shift Length</p>
                    <p className="text-2xl font-semibold mt-2">8.2h</p>
                </div>

                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Payroll Burn</p>
                    <p className="text-2xl font-semibold mt-2">$12.4k</p>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow p-6 h-72 flex items-center justify-center text-gray-400">
                Charts / KPIs Placeholder
            </div>

            <div className="bg-white rounded-xl shadow p-4">
                <h2 className="font-semibold mb-3">Trends</h2>
                <ul className="text-sm text-gray-700 space-y-2">
                    <li>Attendance increased by 3% vs last month</li>
                    <li>Corrections resolved faster (median 1.2 days)</li>
                    <li>Top performing site: Carrefour Delmas</li>
                </ul>
            </div>
        </div>
    );
}
