"use client"
import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";


function TopTeams() {

    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {

        setProcData(null);
        setGQLData(null);



        if (selectedCountry) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                setProcData(DEMO_TEAMS.filter(t => t.country === selectedCountry));
            }, 500);

            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_GRAPHQL_URL}`);
                setGQLData(DEMO_TEAMS.filter(t => t.country === selectedCountry));
            }, 1000);
        }
    }, [selectedCountry])

    return (
        <>
            <Container maxWidth="100%"
                       sx={{backgroundColor: "white", padding: "2rem", borderRadius: "1rem", border: "solid thin black" }}>
                <Box>
                    <h2 style={{fontSize: "1.5rem", marginBottom: "1rem"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedCountry(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                COUNTRIES.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)
                            }
                        </Select>
                    </FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h1 style={{fontSize: "1.5rem", fontWeight: "bold"}}>Results <small>(PROC)</small></h1>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }

                <br/>

                <h1 style={{fontSize: "1.5rem", fontWeight: "bold"}}>Results <small>(GraphQL)</small></h1>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }
                </Container>
            </>
    );
}

export default TopTeams;
