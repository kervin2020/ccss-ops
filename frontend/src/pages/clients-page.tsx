export default function Clients() {
    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Clients</h1>
                <button className="bg-blue-600 text-white px-4 py-2 rounded">Add Client</button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white rounded-xl shadow p-5">
                    <h2 className="font-semibold mb-2">Client list</h2>
                    <ul className="text-sm text-gray-700">
                        <li className="py-2 border-b">ABC Corporation — (contact: alice@abc.com)</li>
                        <li className="py-2 border-b">Hotel Soleil — (contact: contact@soleil.ht)</li>
                        <li className="py-2">Carrefour Market — (contact: ops@carrefour.ht)</li>
                    </ul>
                </div>

                <div className="bg-white rounded-xl shadow p-5">
                    <h2 className="font-semibold mb-2">Client details</h2>
                    <p className="text-sm text-gray-600">Select a client from the list to view details and contracts.</p>
                </div>
            </div>
        </div>
    );
}
