// components/SiteMarker.tsx
import { Marker } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import L from "leaflet";
import "leaflet-extra-markers";
import "leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css";
import "leaflet-extra-markers/dist/js/leaflet.extra-markers.min.js";
import SitePopup from "@/components/SitePopup";

interface SiteMarkerProps {
  site: {
    id: number;
    latitude: number;
    longitude: number;
    name: string;
    description: string;
  };
  onMarkerClick: (siteId: number) => void;
}

const SiteMarker = ({ site, onMarkerClick }: SiteMarkerProps) => {
  const position: LatLngTuple = [site.latitude, site.longitude];
  const markerIcon = L.ExtraMarkers.icon({
    icon: "fa-number", // Choose the appropriate icon class from FontAwesome
    markerColor: "orange-dark", // Choose marker color
  });

  return (
    <Marker
      position={position}
      icon={markerIcon}
      eventHandlers={{
        click: () => {
          onMarkerClick(site.id);
        },
      }}
    >
      <SitePopup site={site} />
    </Marker>
  );
};

export default SiteMarker;
