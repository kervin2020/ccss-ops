export default function Agents() {
    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Agents</h1>
                <div className="flex gap-2">
                    <input
                        className="border rounded px-3 py-2"
                        placeholder="Search agents..."
                    />
                    <button className="bg-blue-600 text-white px-4 py-2 rounded">Add Agent</button>
                </div>
            </div>

            <div className="bg-white shadow rounded-xl overflow-hidden">
                <table className="w-full table-auto">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="p-3 text-left">Name</th>
                            <th className="p-3 text-left">Phone</th>
                            <th className="p-3 text-left">Status</th>
                            <th className="p-3 text-left">Site</th>
                            <th className="p-3 text-left">Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr className="border-t">
                            <td className="p-3">Jean Baptiste</td>
                            <td className="p-3">+509 36 65 3787</td>
                            <td className="p-3">Active</td>
                            <td className="p-3">Port-au-Prince</td>
                            <td className="p-3 text-blue-600 cursor-pointer">Edit</td>
                        </tr>

                        <tr className="border-t">
                            <td className="p-3">Marie Claire</td>
                            <td className="p-3">+509 34 21 9876</td>
                            <td className="p-3">Inactive</td>
                            <td className="p-3">Cap-Haïtien</td>
                            <td className="p-3 text-blue-600 cursor-pointer">Edit</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
