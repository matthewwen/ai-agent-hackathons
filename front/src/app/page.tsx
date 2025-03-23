"use client"
import IgTag from "@/components/igTagPage";
import ListPage from "@/components/listPage";
import GemiResponse from "@/components/judgePage";
import { useEffect, useState } from "react";
import { Button } from "@mui/material";

export default function Home() {
  const [stage, setStage] = useState(0)
  const [igTag, setIgTag] = useState<any>(undefined);
  const [posts, setPosts] = useState<any>(undefined);
  const [llmResponse, setLLMResponse] = useState<any>(undefined);

  const onReset = () => {
    setStage(0);
    setIgTag(undefined);
    setPosts(undefined);
  }

  useEffect(() => {
    if (stage !== 2) {
      return
    }
    console.log({posts});
    // We've moved the API call to the posts.tsx component with the Evaluate Prompt button
    // This prevents duplicate API calls and gives the user more control
  }, [posts, stage])


  return (
    <div style={{margin: "0 auto", maxWidth: "1080px", display: "flex", flexDirection: "column"}}>
      <div style={{marginTop: 20, display: "flex"}}>
        <Button variant="contained" 
          onClick={onReset}>Reset
        </Button>
        <div style={{flex: 1, marginLeft: 10}}>
          {igTag && <a href={`https://www.instagram.com/${igTag}`} target="_blank" rel="noopener noreferrer" >
            @{igTag}
          </a>}
        </div>
        {
          stage === 1 && posts && 
          <Button 
            variant="contained" 
            onClick={() => {
              console.log("setStage", stage)
              setStage(2)
            }}>
              Submit
          </Button>
        }
      </div>
      <div style={{flex: 1}}>
        {stage === 0 && 
          <IgTag 
            setStage={setStage}
            setIgTag={setIgTag}
          />
        }
        {stage === 1 && 
          <ListPage
            igTag={igTag}
            posts={posts}
            setPosts={setPosts}
          />
        }
        {stage === 2 && 
          <GemiResponse
            setStage={setStage}
            llmResponse={llmResponse}
          />
        }
      </div>
    </div>
  );
}
