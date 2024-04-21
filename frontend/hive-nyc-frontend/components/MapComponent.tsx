"use client";
import { useEffect, useState } from "react";
import { TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import L from "leaflet";
import dynamic from "next/dynamic";
import "leaflet/dist/leaflet.css";

const MapContainer = dynamic(
  () => import("react-leaflet").then((mod) => mod.MapContainer),
  {
    ssr: false, // This will make the component only be rendered on client-side
  }
);

const MapComponent = () => {

  const [sites, setSites] = useState([]);
  // Set the default center and zoom level of the map
  const defaultCenter: LatLngTuple = [40.7128, -74.006]; // Coordinates for NYC
  const defaultZoom = 12;

  // Fetch historical sites data from your backend
  useEffect(() => {
    const fetchSites = async () => {
      const response = await fetch('http://localhost:8000/sites'); // Adjust the URL to your API endpoint
      const data = await response.json();
      setSites(data);
    };

    fetchSites();
  }, []);

  return (
    <MapContainer
      center={defaultCenter}
      zoom={defaultZoom}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        // URL to a tile server, using OpenStreetMap tiles
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {/* Markers for historical sites would go here */}
    </MapContainer>
  );
};

export default MapComponent;
