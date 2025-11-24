export default function Overview() {
    return (
        <div className="p-6 space-y-6">
            <h1 className="text-3xl font-bold">Overview</h1>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Total Agents</p>
                    <p className="text-2xl font-semibold mt-2">128</p>
                </div>

                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Active Sites</p>
                    <p className="text-2xl font-semibold mt-2">24</p>
                </div>

                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Today Attendances</p>
                    <p className="text-2xl font-semibold mt-2">92</p>
                </div>

                <div className="bg-white rounded-xl shadow p-5">
                    <p className="text-sm text-gray-500">Pending Corrections</p>
                    <p className="text-2xl font-semibold mt-2">7</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <div className="col-span-2 bg-white rounded-xl shadow p-6 h-64 flex items-center justify-center text-gray-400">
                    Chart / Timeline Placeholder
                </div>

                <div className="bg-white rounded-xl shadow p-6">
                    <h2 className="font-semibold mb-3">Recent Activity</h2>
                    <ul className="space-y-2 text-sm text-gray-700">
                        <li>Agent John submitted attendance correction</li>
                        <li>New site created: Carrefour</li>
                        <li>Payroll for Oct 2025 processed</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
