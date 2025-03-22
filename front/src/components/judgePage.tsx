"use client"

export default function GemiResponse(props: any) {
    const {llmResponse} = props;
    
    return (
        <div>{llmResponse}</div>
    )
}