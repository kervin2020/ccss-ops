export default function Sites() {
    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Sites</h1>
                <button className="bg-blue-600 text-white px-4 py-2 rounded">Add Site</button>
            </div>

            <div className="bg-white rounded-xl shadow overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="p-3 text-left">Site Name</th>
                            <th className="p-3 text-left">Address</th>
                            <th className="p-3 text-left">Client</th>
                            <th className="p-3 text-left">Active</th>
                            <th className="p-3 text-left">Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr className="border-t">
                            <td className="p-3">Carrefour Delmas</td>
                            <td className="p-3">Delmas 33</td>
                            <td className="p-3">Carrefour</td>
                            <td className="p-3">Yes</td>
                            <td className="p-3 text-blue-600 cursor-pointer">Edit</td>
                        </tr>

                        <tr className="border-t">
                            <td className="p-3">Hotel Montana</td>
                            <td className="p-3">Turgeau</td>
                            <td className="p-3">Hotel Soleil</td>
                            <td className="p-3">No</td>
                            <td className="p-3 text-blue-600 cursor-pointer">Edit</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
