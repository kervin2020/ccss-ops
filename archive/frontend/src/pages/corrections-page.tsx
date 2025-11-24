export default function Corrections() {
    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Corrections</h1>
                <button className="bg-blue-600 text-white px-4 py-2 rounded">New Correction</button>
            </div>

            <div className="bg-white rounded-xl shadow p-4">
                <h2 className="font-semibold mb-3">Pending Corrections</h2>
                <ul className="space-y-3">
                    <li className="border rounded p-3 flex justify-between items-center">
                        <div>
                            <div className="font-medium">Correction #1024</div>
                            <div className="text-sm text-gray-600">Agent: Jean — Missing clock-in</div>
                        </div>
                        <div className="flex gap-2">
                            <button className="px-3 py-1 bg-green-600 text-white rounded">Approve</button>
                            <button className="px-3 py-1 bg-red-500 text-white rounded">Reject</button>
                        </div>
                    </li>

                    <li className="border rounded p-3 flex justify-between items-center">
                        <div>
                            <div className="font-medium">Correction #1023</div>
                            <div className="text-sm text-gray-600">Agent: Marie — Wrong site</div>
                        </div>
                        <div className="flex gap-2">
                            <button className="px-3 py-1 bg-green-600 text-white rounded">Approve</button>
                            <button className="px-3 py-1 bg-red-500 text-white rounded">Reject</button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    );
}
