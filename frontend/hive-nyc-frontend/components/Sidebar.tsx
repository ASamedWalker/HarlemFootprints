// app/components/Sidebar.tsx
export default function Sidebar() {
  return (
    <div className="p-4">
      {/* Logo */}
      <h1 className="text-2xl font-bold mb-4">HiveNYC</h1>

      {/* Search bar */}
      <input
        type="search"
        placeholder="Search historical sites"
        className="w-full mb-4 p-2"
      />

      {/* List of sites */}
      <div className="overflow-y-auto">
        {/* Here you'll map over sites to create list items */}
      </div>
    </div>
  );
}
