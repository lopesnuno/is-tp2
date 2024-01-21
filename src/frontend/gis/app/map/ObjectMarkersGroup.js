'use client'
import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from './ObjectMarker';


function ObjectMarkersGroup() {
  const map = useMap();
  const [data, setData] = useState(null);
  const [geom, setGeom] = useState(null);
  const [bounds, setBounds] = useState(map.getBounds());

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:20002/api/markers');
        if (!response.ok) {
          return new Error('Network response was not ok');
        }
        const results = await response.json();
        setData(results);
        console.log('API call successful');
      } catch (error) {
        console.error('Error fetching data:', error);
      }x
    };
    fetchData();
  }, []);

  useEffect(() => {
    const cb = () => {
      setBounds(map.getBounds());
    };
    map.on('moveend', cb);

    return () => {
      map.off('moveend', cb);
    };
  }, [map]);

  useEffect(() => {
    console.log(`> getting data for bounds...`, bounds);
    if (data) {
      setGeom(data);
    }
  }, [data, bounds]);

  return (
    <LayerGroup>
      {Array.isArray(geom) &&
        geom.map((geoJSON) => (
          <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON} />
        ))}
    </LayerGroup>
  );
}

export default ObjectMarkersGroup;