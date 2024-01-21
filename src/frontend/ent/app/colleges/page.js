'use client'
import {useEffect, useState, useCallback} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
} from "@mui/material";
import {useRouter, useSearchParams, usePathname} from "next/navigation";

export default function CollegesPage() {
    const searchParams = useSearchParams();
    const pathname = usePathname();
    const router = useRouter();

    const createQueryString = useCallback(
        (name, value) => {
            const params = new URLSearchParams(searchParams);
            params.set(name, value);

            return params.toString();
        },
        [searchParams]
    );

    const [data, setData] = useState(null);
    const [colleges, setColleges] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(null);
    const page = parseInt(searchParams.get("page")) || 1;
    const PAGE_SIZE = 10;

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(`http://localhost:20001/colleges`);
            const data = await response.json();
            setData(data);
            setMaxDataSize(data.length);
        };

        fetchData();
    }, []);

    useEffect(() => {
        setColleges(null);
        setTimeout(() => {
            setColleges(
                data.filter(
                    (item, index) => Math.floor(index / PAGE_SIZE) === page - 1
                )
            );
        }, 500);
    }, [data, page]);

    return (
        <>
            <h1 sx={{fontSize: "100px"}}>Colleges</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow sx={{backgroundColor: "lightgray"}}>
                            <TableCell>Name</TableCell>
                            <TableCell align="center">Created On</TableCell>
                            <TableCell align="center">Updated On</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {colleges ? (
                            colleges.map((college) => (
                                <TableRow key={college.id}>
                                    <TableCell>{college.name}</TableCell>
                                    <TableCell align="center">{new Date(college.created_on).toLocaleString()}</TableCell>
                                    <TableCell align="center">{new Date(college.updated_on).toLocaleString()}</TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={3}>
                                    <CircularProgress/>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
            {maxDataSize && (
                <Pagination
                    style={{color: "black", marginTop: 8}}
                    variant="outlined"
                    shape="rounded"
                    color={"primary"}
                    onChange={(e, v) => {
                        router.push(pathname + "?" + createQueryString("page", v));
                    }}
                    page={page}
                    count={Math.ceil(maxDataSize / PAGE_SIZE)}
                />
            )}
        </>
    );
}
