"use client"

import { Button } from "@mui/material";
import Post from "./posts";
import { use, useEffect } from "react";

export default function ListPage(props: any) {
    const {query, posts, setPosts} = props;
    
    useEffect(() => {
        setPosts([])
    }, [query])

    return (
        <div>
            <div style={{display: "flex"}}>
                {
                    posts === undefined ? <div>Loading....</div> : posts.map((item: any, i: number) => (
                        <Post
                            key={`posts-${i}`}
                            item={item}
                        />
                    ))
                }
            </div>
        </div>
    )
}