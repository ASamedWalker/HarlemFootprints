// components/Sidebar.tsx
import Image from "next/image";
import { HistoricalSite } from "@/types/historicalSiteTypes";

interface SidebarProps {
  siteDetails: HistoricalSite | null;
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar = ({ siteDetails, isOpen, onClose }: SidebarProps) => {
  if (!isOpen || !siteDetails) {
    return null;
  }
  const fullImageUrl = `${process.env.NEXT_PUBLIC_API_URL}${siteDetails.images[0]}`;

  return (
    <aside
      className={`transform top-0 right-0 w-80 bg-white fixed h-full overflow-auto ease-in-out transition-all duration-300 z-1000 ${
        isOpen ? "translate-x-0" : "translate-x-full"
        } shadow-lg`}
        style={{ zIndex: 1000 }}
    >
       <div className="flex justify-between items-center p-4 border-b border-gray-200">
        <h1 className="text-lg font-semibold">{siteDetails.name}</h1>
        <button onClick={onClose} className="p-1 rounded-full bg-gray-200 hover:bg-gray-300 focus:outline-none">
          <span className="material-icons">close</span>
        </button>
      </div>

      {siteDetails.images && siteDetails.images.length > 0 && (
        <div className="relative w-full h-56">
          <Image
            src={fullImageUrl}
            alt={siteDetails.name}
            layout="fill"
            objectFit="cover"
            className="object-cover rounded-lg"
          />
        </div>
      )}
       <div className="p-4">
        <p className="text-sm text-gray-500">{siteDetails.description}</p>
        {siteDetails.address && (
          <p className="mt-2 text-sm text-gray-600"><strong>Address:</strong> {siteDetails.address}</p>
        )}
        {siteDetails.era && (
          <p className="mt-1 text-sm text-gray-600"><strong>Era:</strong> {siteDetails.era}</p>
        )}
        {siteDetails.tags && siteDetails.tags.length > 0 && (
          <div className="mt-2">
            <strong>Tags:</strong>
            <ul className="flex flex-wrap gap-2 mt-1">
              {siteDetails.tags.map(tag => (
                <li key={tag} className="bg-blue-100 text-blue-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded">
                  {tag}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
