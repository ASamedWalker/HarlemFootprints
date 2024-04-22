// components/Sidebar.tsx
import { useState, useEffect } from "react";
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
      className={`sidebar ${isOpen ? "open" : ""}`}
      aria-hidden={!isOpen}
      style={{
        position: "fixed",
        right: 0,
        top: 0,
        height: "100vh",
        width: "300px",
        overflowY: "auto",
        overflowX: "hidden",
        zIndex: 1000,
        marginLeft: 'auto',
        scrollbarWidth: 'none',
      }}
    >
      <button onClick={onClose} className="sidebar-close">
        Close
      </button>
      <div className="sidebar-content">
        {siteDetails.images && siteDetails.images.length > 0 && (
          <Image
            src={fullImageUrl}
            alt={siteDetails.name}
            height={300}
            width={400}
            className="sidebar-image"
          />
        )}
        <h1 className="sidebar-title">{siteDetails.name}</h1>
        <p className="sidebar-description">{siteDetails.description}</p>
        {siteDetails.address && (
          <p className="sidebar-address">{siteDetails.address}</p>
        )}
        {siteDetails.era && (
          <p className="sidebar-era">Era: {siteDetails.era}</p>
        )}
        {siteDetails.tags && (
          <ul className="sidebar-tags">
            {siteDetails.tags.map((tag) => (
              <li key={tag}>{tag}</li>
            ))}
          </ul>
        )}
        {siteDetails.audio_guide_url && (
          <audio controls className="sidebar-audio">
            <source src={siteDetails.audio_guide_url} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        )}
        {/* You can add more details as required */}
      </div>
    </aside>
  );
};

export default Sidebar;
