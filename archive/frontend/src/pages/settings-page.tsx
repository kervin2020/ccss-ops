export default function Settings() {
    return (
        <div className="p-6 max-w-3xl">
            <h1 className="text-3xl font-bold mb-6">Settings</h1>

            <form className="space-y-6 bg-white rounded-xl shadow p-6">
                <div>
                    <label className="block text-sm text-gray-600 mb-1">Company Name</label>
                    <input className="w-full border rounded px-3 py-2" placeholder="CCSS Ops" />
                </div>

                <div>
                    <label className="block text-sm text-gray-600 mb-1">Default Currency</label>
                    <select className="w-full border rounded px-3 py-2">
                        <option>USD</option>
                        <option>HTG</option>
                    </select>
                </div>

                <div>
                    <label className="block text-sm text-gray-600 mb-1">Notification Email</label>
                    <input className="w-full border rounded px-3 py-2" placeholder="admin@company.com" />
                </div>

                <div className="flex justify-end gap-3">
                    <button className="px-4 py-2 border rounded">Cancel</button>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded">Save</button>
                </div>
            </form>
        </div>
    );
}
