"use client";

import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEffect, useRef } from "react";

export default function Map() {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_KEY!;

    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      center: { latitude: 53.3483, longitude: -6.2717 }, // Fixed key names
      zoom: 12,
    });

    return () => mapRef.current?.remove();
  }, []);

  return <div id="map-container" className="bg-slate-100 h-screen" ref={mapContainerRef} />;
}


