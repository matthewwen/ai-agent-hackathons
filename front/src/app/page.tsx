"use client"
import IgTag from "@/components/igTagPage";
import ListPage from "@/components/listPage";
import GemiResponse from "@/components/judgePage";
import { useEffect, useState } from "react";
import { Button } from "@mui/material";

export default function Home() {
  const [stage, setStage] = useState(0)
  const [igTag, setIgTag] = useState<any>(undefined);
  const [query, setQuery] = useState<any[]>([])
  const [posts, setPosts] = useState<any>(undefined);
  const [llmResponse, setLLMResponse] = useState<any>(undefined);

  const onReset = () => {
    setStage(0);
    setIgTag(undefined);
    setQuery([])
    setPosts(undefined);
  }

  useEffect(() => {
    // call endpoint -> given ig tag
    setQuery(["healthy", "chinese"])
  }, [igTag])

  useEffect(() => {
    console.log({posts});
    if (stage !== 3) {
      return
    }
    // call endpoint -> set user preferences
    setLLMResponse("this is what we think about prompt")
  }, [posts])


  return (
    <div style={{margin: "0 auto", maxWidth: "1080px", display: "flex", flexDirection: "column"}}>
      <div style={{marginTop: 20, display: "flex"}}>
        <Button variant="contained" 
          onClick={onReset}>Reset
        </Button>
        <div style={{flex: 1}}/>
        {
          stage === 1 && 
          <Button 
            variant="contained" 
            onClick={() => {
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
            query={query}
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
