import { NextApiRequest, NextApiResponse } from "next";
import { describe } from "node:test";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({
    places: [
      {
        restaurant_name: "New England Lobster",
        restaurant_location: "Milbrae",
        restaurant_description: "Servers Any Food with Lobster. Not that expensive, pretty good."
      },
      {
        restaurant_name: "Brendas French Soul Food",
        restaurant_location: "Lower Nob Hill",
        restaurant_description: "Serves Good"
      }
    ]
  })

}

  