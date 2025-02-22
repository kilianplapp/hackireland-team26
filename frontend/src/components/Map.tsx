"use client";

import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEffect, useRef } from "react";

export default function Map() {
  const mapRef = useRef(null);
  const mapContainerRef = useRef(null);

  useEffect(() => {
    mapboxgl.accessToken =
      "pk.eyJ1IjoiMTIxMzA4NzU2IiwiYSI6ImNtNjU5YzFyZDFyZzUya3F0ZjluMnE0NHcifQ.byvxdkN_EdqJekDzfY5wlA";

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
