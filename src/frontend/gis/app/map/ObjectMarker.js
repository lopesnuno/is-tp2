'use client'
import React from "react";
import { Avatar, List, ListItem, ListItemIcon, ListItemText } from "@mui/material";
import SchoolIcon from "@mui/icons-material/School";
import { Marker, Popup } from "react-leaflet";
import { icon as leafletIcon, point } from "leaflet";

const LIST_PROPERTIES = [
  { key: "name", label: "College", Icon: SchoolIcon },
];

export function ObjectMarker({ geoJSON }) {
  const properties = geoJSON?.properties;
  const { name } = properties;
  const coordinates = geoJSON?.geometry?.coordinates;

  return (
    <Marker
      position={coordinates}
      icon={leafletIcon({
        iconUrl: "https://cdn-icons-png.flaticon.com/512/5351/5351056.png",
        iconRetinaUrl: "https://cdn-icons-png.flaticon.com/512/5351/5351056.png",
        iconSize: point(50, 50),
      })}
    >
      <Popup>
        <List dense={true}>
          <ListItem>
            <ListItemIcon>
              <Avatar alt={name} src="https://cdn-icons-png.flaticon.com/512/5351/5351056.png" />
            </ListItemIcon>
            <ListItemText primary={name} />
          </ListItem>
          {LIST_PROPERTIES.map(({ key, label, Icon }) => (
            <ListItem key={key}>
              <ListItemIcon>
                <Icon style={{ color: "black" }} />
              </ListItemIcon>
              <ListItemText
                primary={
                  <span>
                    {properties[key]}
                    <br />
                    <label style={{ fontSize: "xx-small" }}>{label}</label>
                  </span>
                }
              />
            </ListItem>
          ))}
        </List>
      </Popup>
    </Marker>
  );
}
