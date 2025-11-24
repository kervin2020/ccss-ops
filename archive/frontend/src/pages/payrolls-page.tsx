export default function Payrolls() {
    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Payrolls</h1>
                <div className="flex gap-2">
                    <select className="border rounded px-3 py-2">
                        <option>This month</option>
                        <option>Last month</option>
                    </select>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded">Run Payroll</button>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow overflow-auto">
                <table className="w-full">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="p-3 text-left">Period</th>
                            <th className="p-3 text-left">Total Paid</th>
                            <th className="p-3 text-left">Status</th>
                            <th className="p-3 text-left">Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr className="border-t">
                            <td className="p-3">October 2025</td>
                            <td className="p-3">$12,450</td>
                            <td className="p-3 text-green-600">Completed</td>
                            <td className="p-3 text-blue-600 cursor-pointer">Download</td>
                        </tr>

                        <tr className="border-t">
                            <td className="p-3">September 2025</td>
                            <td className="p-3">$11,900</td>
                            <td className="p-3 text-green-600">Completed</td>
                            <td className="p-3 text-blue-600 cursor-pointer">Download</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
