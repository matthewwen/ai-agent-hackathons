"use client"

import Post from "./posts";
import { Button, Card, CardContent, Container, Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";

export default function ListPage(props: any) {
    const {posts, setPosts, igTag} = props;
    const [newPrompt, setNewPrompt] = useState<string>("");
    const [currentPrompt, setCurrentPrompt] = useState<string>("");
    const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
    
    useEffect(() => {
        if (posts !== undefined) {
            return;
        }
        fetch("/api/google",  {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({igTag: igTag,})}
        ).then(async (res: Response) => {
            const resJson = await res.json()
            setPosts(resJson);
        });
    }, [igTag])
    
    const evaluatePrompt = () => {
        setIsEvaluating(true);
        
        // Make sure we have all the required data before sending
        if (!posts || !posts.recommendations) {
            console.error("Missing recommendations data");
            setIsEvaluating(false);
            return;
        }
        
        // Check if all recommendations have preferences set
        const allPreferencesSet = posts.recommendations.every((rec: any) => rec.preference !== undefined);
        if (!allPreferencesSet) {
            alert("Please set preferences (like/dislike) for all recommendations before evaluating.");
            setIsEvaluating(false);
            return;
        }
        
        // Log the data we're sending for debugging
        console.log("Sending data to backend:", posts);
        
        // Call the deployment server for the rewrite endpoint
        fetch("https://ai-agent-hackathons.onrender.com/rewrite", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(posts)
        }).then(async (res: Response) => {
            if (!res.ok) {
                throw new Error(`Server responded with status: ${res.status}`);
            }
            const resJson = await res.json();
            console.log({resJson});
            
            if (resJson && "current_prompt" in resJson && "response" in resJson) {
                setCurrentPrompt(resJson["current_prompt"]);
                setNewPrompt(resJson["response"]);
                console.log("Current prompt:", resJson["current_prompt"]);
                console.log("New prompt:", resJson["response"]);
            } else {
                console.error("Unexpected response format:", resJson);
                alert("Received unexpected response format from server.");
            }
        }).catch(error => {
            console.error("Error evaluating prompt:", error);
            alert(`Error evaluating prompt: ${error.message}`);
        }).finally(() => {
            setIsEvaluating(false);
        });
    }

    return (
        <div>
            <div style={{display: "flex", flexWrap: "wrap"}}>
                {
                    posts === undefined ? <div>Loading....</div> : posts.recommendations.map((item: any, i: number) => (
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
            
            {posts && posts.recommendations && (
                <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
                    <Paper elevation={3} sx={{ p: 3, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Button 
                            variant="contained" 
                            color="primary" 
                            size="large" 
                            onClick={evaluatePrompt}
                            disabled={isEvaluating}
                            sx={{ mb: 3 }}
                        >
                            {isEvaluating ? "Evaluating..." : "Evaluate Prompt"}
                        </Button>
                        
                        {currentPrompt && (
                            <Card sx={{ width: '100%', mb: 2, bgcolor: '#f5f5f5' }}>
                                <CardContent>
                                    <Typography variant="h6" color="text.secondary" gutterBottom>
                                        Current Prompt:
                                    </Typography>
                                    <Typography variant="body1">
                                        {currentPrompt}
                                    </Typography>
                                </CardContent>
                            </Card>
                        )}
                        
                        {newPrompt && (
                            <Card sx={{ width: '100%', bgcolor: '#e3f2fd' }}>
                                <CardContent>
                                    <Typography variant="h6" color="primary" gutterBottom>
                                        New Prompt:
                                    </Typography>
                                    <Typography variant="body1">
                                        {newPrompt}
                                    </Typography>
                                </CardContent>
                            </Card>
                        )}
                    </Paper>
                </Container>
            )}
        </div>
    )
}