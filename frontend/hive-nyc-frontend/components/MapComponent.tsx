"use client";
import { useEffect, useState } from "react";
import { TileLayer } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import dynamic from "next/dynamic";
import "leaflet/dist/leaflet.css";
import SiteMarker from "./SiteMarker";
import { BeatLoader } from "react-spinners";
import { HistoricalSite } from "@/types/historicalSiteTypes";

const MapContainer = dynamic(
  () => import("react-leaflet").then((mod) => mod.MapContainer),
  {
    ssr: false,
  }
);

interface MapComponentProps {
  onMarkerClick: (siteId: number) => void;
}

const MapComponent = ({ onMarkerClick }: MapComponentProps) => {
  const [sites, setSites] = useState<HistoricalSite[]>([]);
  const [loading, setLoading] = useState(true);
  const defaultCenter: LatLngTuple = [40.7128, -74.006]; // Coordinates for NYC
  const defaultZoom = 12;

  useEffect(() => {
    const fetchSites = async () => {
      try {
        const response = await fetch("http://localhost:8000/sites");
        const data = await response.json();
        setSites(data);
      } catch (error) {
        console.error("Failed to fetch sites:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchSites();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <BeatLoader color="#0000FF" />
      </div>
    );
  }

  return (
    <MapContainer
      center={defaultCenter}
      zoom={defaultZoom}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {sites.map((site) => (
        <SiteMarker key={site.id} site={site} onMarkerClick={onMarkerClick} />
      ))}
    </MapContainer>
  );
};

export default MapComponent;
