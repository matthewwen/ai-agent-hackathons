"use client"

import Post from "./posts";
import { useEffect } from "react";

export default function ListPage(props: any) {
    const {query, posts, setPosts} = props;
    
    useEffect(() => {
        fetch("/api/google").then(async (res: Response) => {
            const resJson = await res.json()
            setPosts(resJson.places);
        });
    }, [query])

    return (
        <div>
            <div style={{display: "flex"}}>
                {
                    posts === undefined ? <div>Loading....</div> : posts.map((item: any, i: number) => (
                        <Post
                            key={`posts-${i}`}
                            item={item}
                            items={posts}
                            setItems={setPosts}
                            idx={i}
                        />
                    ))
                }
            </div>
        </div>
    )
}