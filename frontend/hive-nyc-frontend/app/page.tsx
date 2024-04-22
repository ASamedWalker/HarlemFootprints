"use client";
import { useState, useEffect } from "react";
import MapComponent from "@/components/MapComponent";
import Sidebar from "@/components/Sidebar";

const HomePage = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [currentSiteDetails, setCurrentSiteDetails] = useState(null);

  // Function to call when a marker is clicked
  const handleMarkerClick = async (siteId) => {
    const response = await fetch(`http://localhost:8000/sites/${siteId}`);
    const data = await response.json();
    setCurrentSiteDetails(data);
    setSidebarOpen(true);
  };

  // Function to close the sidebar
  const handleCloseSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <div className="flex h-screen relative">
      {/* Your map component goes here, and you pass handleMarkerClick to it */}
      <MapComponent onMarkerClick={handleMarkerClick} />

      {/* Sidebar component */}
      <Sidebar
        siteDetails={currentSiteDetails}
        isOpen={isSidebarOpen}
        onClose={handleCloseSidebar}
      />
    </div>
  );
};

export default HomePage;
