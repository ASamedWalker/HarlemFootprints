// components/SitePopup.tsx
import { Popup } from "react-leaflet";

interface SitePopupProps {
  site: {
    id: number;
    name: string;
    description: string;
  };
}

const SitePopup: React.FC<SitePopupProps> = ({ site }) => {
  return (
    <Popup>
      <strong>{site.name}</strong>
      <p>{site.description}</p>
      <a href={`/sites/${site.id}`}>Learn more</a>
    </Popup>
  );
};

export default SitePopup;
