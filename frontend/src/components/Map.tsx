"use client";

import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEffect, useRef } from "react";

export default function Map() {
  const mapRef = useRef(null);
  const mapContainerRef = useRef(null);

  useEffect(() => {
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_KEY;

    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      center: {
        lat: 53.3483457818045,
        lng: -6.271704148999037,
      },
      zoom: 12,
    });

    return () => {
      mapRef.current.remove();
    };
  }, []);

  return (
    <div
      id="map-container"
      className="bg-slate-100 h-screen"
      ref={mapContainerRef}
    />
  );
}
