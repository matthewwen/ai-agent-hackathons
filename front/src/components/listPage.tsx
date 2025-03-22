"use client"

import Post from "./posts";
import { useEffect } from "react";

export default function ListPage(props: any) {
    const {posts, setPosts, igTag} = props;
    
    useEffect(() => {
        fetch("/api/google",  {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({igTag: igTag,})}
        ).then(async (res: Response) => {
            const resJson = await res.json()
            setPosts(resJson.places);
        });
    }, [igTag])

    return (
        <div>
            <div style={{display: "flex", flexWrap: "wrap"}}>
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