import { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const igTag = req.body["igTag"]
  const response = await fetch(`https://ai-agent-hackathons.onrender.com/instagram/${igTag}/full-service`);
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  const data = await response.json();
  console.log('Received data from backend:', data);

  res.status(200).json({
    places: data.recommendations,
    ...data
  })

}

