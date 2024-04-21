import Image from "next/image";
import MapComponent from "@/components/MapComponent";
import Sidebar from "@/components/Sidebar";

export default function Home() {
  return (
    <>
      <div className="flex h-screen">

        {/* Sidebar */}
        {/* <aside className="w-80">
          <Sidebar />
        </aside> */}

        {/* Map */}
        <div className="flex-grow">
          <MapComponent />
        </div>
      </div>
    </>
  );
}
