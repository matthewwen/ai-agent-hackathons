"use client"

import { TextField } from "@mui/material"
import { useState } from "react"

export default function IgTag(props: any) {
    const { setStage, setIgTag } = props;
    const [inputValue, setInputValue] = useState('');

    const handleKeyDown = (event: any) => {
        if (event.key === 'Enter') {
            setIgTag(inputValue);
            setStage(1);
        }
    };

    return (
        <div style={{ textAlign: "center", "height": "90vh", "width": "100%", alignContent: "center", overflow: "hidden" }}>
            <div style={{ margin: 10 }}>
                Enter IG Tag to Get Personalized Recommendations for Restaurants
                Press Enter when ready
            </div>
            <TextField
                label="Enter Instagram Tag"
                variant="outlined"
                color="secondary"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
            />
        </div>
    );
}