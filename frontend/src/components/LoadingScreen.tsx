export default function LoadingScreen() {
  return (
    <div className="p-8 space-y-4 animate-pulse">
      <div className="h-6 w-56 bg-gray-800 rounded" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-24 bg-gray-900 border border-gray-800 rounded-xl" />
        ))}
      </div>
      <div className="h-56 bg-gray-900 border border-gray-800 rounded-xl" />
    </div>
  )
}
