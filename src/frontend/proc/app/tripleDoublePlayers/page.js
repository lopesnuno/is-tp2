'use client'
import React, { useEffect, useState } from "react";
import {
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper
} from "@mui/material";

export default function TripleDoublePlayers() {
  const [procData, setProcData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:20004/api/triple_double_players');
        const data = await response.json();
        console.log(data[0]['name'])
        setProcData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <h1 sx={{ fontSize: "100px" }}>Triple Double Players - <b>PROC</b></h1>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow sx={{ backgroundColor: "lightgray" }}>
              <TableCell>Name</TableCell>
              <TableCell align="center">Number Of Seasons</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {procData ? (
              <TableRow key={procData}>
                <TableCell component="td" scope="row">
                  {procData[0]['name']}
                </TableCell>
                <TableCell component="td" align="center" scope="row">
                  {procData[0]['seasons']}
                </TableCell>
              </TableRow>
            ) : (
              <TableRow>
                <TableCell colSpan={3}>
                  <CircularProgress />
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
}
