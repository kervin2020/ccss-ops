export default function Attendances() {
    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-4">Attendances</h1>

            <div className="bg-white rounded-xl shadow p-4 mb-6">
                <div className="flex items-center gap-3">
                    <input type="date" className="border rounded px-3 py-2" />
                    <button className="bg-blue-600 text-white px-4 py-2 rounded">Filter</button>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow overflow-auto">
                <table className="w-full">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="p-3 text-left">Agent</th>
                            <th className="p-3 text-left">Site</th>
                            <th className="p-3 text-left">Time In</th>
                            <th className="p-3 text-left">Time Out</th>
                            <th className="p-3 text-left">Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr className="border-t">
                            <td className="p-3">Jean Baptiste</td>
                            <td className="p-3">Carrefour Delmas</td>
                            <td className="p-3">08:00</td>
                            <td className="p-3">17:00</td>
                            <td className="p-3">Present</td>
                        </tr>

                        <tr className="border-t">
                            <td className="p-3">Marie Claire</td>
                            <td className="p-3">Hotel Montana</td>
                            <td className="p-3">--</td>
                            <td className="p-3">--</td>
                            <td className="p-3 text-yellow-600">Missing</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
