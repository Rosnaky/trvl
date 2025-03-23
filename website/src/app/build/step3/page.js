"use client"

import { useState } from "react"
import Link from "next/link"

const Step3 = () => {
    const [selected, setSelected] = useState(null)

    const options = [
        "Alone", "With SO", "Friends", "Family"
    ]

    console.log(selected);

    const [loading, setLoading] = useState(false)

    const handleSubmit = async() => {
        setLoading(true);
        try {
            const response = await fetch("http://localhost:5050/generate-trip", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // "city": localStorage.getItem()
                },
                body: JSON.stringify({ additionalInfo: selected })
            });

            if (response.ok) {
                console.log("Script initialized successfully");
                window.location.href = "/build/step3"; // Redirect after success
            } else {
                console.error("Failed to start script");
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="mt-20">
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">Anything Else?</h2>
            <div className="flex gap-4 w-1/2 mx-auto mt-10 justify-around">
                <textarea className="bg-white flex w-1/1" onChange={(value) => {setSelected(value); localStorage.setItem("additionalInfo", event.target.value)}}/>
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
                <button onClick={() => handleSubmit} className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-white cursor-pointer mt-10">That's everything!</button>
            </div>
        </div>
    )
}

export default Step3
