'use client'
import React, {useEffect, useState} from "react";
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
                const response = await fetch('http://localhost:20004/api/top5_colleges');
                const data = await response.json();
                console.log('DATA -> ', Array.isArray(data))
                setProcData(data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    return (
        <>
            <h1 sx={{fontSize: "100px"}}>Top 5 Colleges - <b>PROC</b></h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow sx={{backgroundColor: "lightgray"}}>
                            <TableCell>College</TableCell>
                            <TableCell align="center">Number of Players</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {Array.isArray(procData) ? (
                            procData.map((row) => (
                                <TableRow key={row.college}>
                                    <TableCell component="td" scope="row">
                                        {row.college}
                                    </TableCell>
                                    <TableCell component="td" align="center" scope="row">
                                        {row.num_players}
                                    </TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={2}>
                                    <CircularProgress/>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
        </>
    );
}
