"use client"

import { Card, CardActions, CardContent } from "@mui/material";
import Typography from "@mui/material/Typography";
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import ThumbDownAltIcon from '@mui/icons-material/ThumbDownAlt';
import { useEffect, useState } from "react";

export default function Post(props: any) {
    const { item, items, setItems, idx } = props;
    const [preference, setPreference] = useState<any>(undefined);
    useEffect(() => {
        const clone = structuredClone(item);
        clone["preference"] = preference
        const newItems = { ...items };
        newItems["recommendations"][idx] = clone;
        setItems(newItems);
    }, [preference])



    return (
        <Card sx={{ width: 275, margin: 1 }}>
            <CardContent sx={{ height: 200, overflow: "scroll" }}>
                <Typography gutterBottom sx={{ fontSize: 15 }}>
                    {item.restaurant_name}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    {item.restaurant_location}
                </Typography>
                <Typography variant="body2">
                    {item.restaurant_description}
                </Typography>
            </CardContent>
            <CardActions>
                <div style={{
                    backgroundColor: preference === "dislike" ? "#F44" : undefined,
                    borderRadius: "100%",
                    width: 30,
                    height: 30,
                    textAlign: "center"
                }}
                    onClick={() => {
                        setPreference("dislike")
                    }}
                >
                    <ThumbDownAltIcon />
                </div>
                <div style={{
                    backgroundColor: preference === "like" ? "#4F4" : undefined,
                    borderRadius: "100%",
                    width: 30,
                    height: 30,
                    textAlign: "center"
                }}
                    onClick={() => {
                        setPreference("like")
                    }}
                >
                    <ThumbUpAltIcon />
                </div>

            </CardActions>

        </Card>
    )
}