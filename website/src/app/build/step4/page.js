"use client"

import { useState } from "react"
import Link from "next/link"

const Step3 = () => {
    const [selected, setSelected] = useState(null)

    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {
        setLoading(true);
        const cityNameDest = localStorage.getItem('cityNameDest');
        const cityNameOrigin = localStorage.getItem('cityNameOrigin');
        const dateRange = JSON.parse(localStorage.getItem("date")); // Parse the string into an object
        const startDate = dateRange?.from; // Extract 'from' date
        const endDate = dateRange?.to; // Extract 'to' date
        const minBudget = "20"
        const maxBudget = "80"
        const additionalInfo = selected || localStorage.getItem('additionalInfo'); // Use `selected` if available, else fallback to localStorage

        const params = {
            cityNameDest: cityNameDest,
            start_date: startDate,
            end_date: endDate,
            min_budget: minBudget,
            max_budget: maxBudget,
            cityNameOrigin: cityNameOrigin,
            additionalInfo
        };

        try {
            console.log(params)

            const response = await fetch("http://localhost:5050/generate-trip", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(params) // Send all parameters in the request body
            });
    
            if (response.ok) {
                console.log("Script initialized successfully");
    
                // Wait for the response to complete, then redirect
                const responseData = await response.json(); // Assuming the server returns a JSON response
                console.log(responseData); // You can inspect or use the returned data here if needed
    
                window.location.href = "/schedule"; // Redirect after success
            } else {
                console.error("Failed to start script", response.statusText);
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            setLoading(false); // Reset loading state
        }
    };
    

    return (
        <div className="mt-20">
            <Link href={"/build/step3"}>
                <button
                    className="ml-30 mb-12 text-white px-8 py-2 rounded-lg border-white cursor-pointer hover:bg-[#f4f4f420] transition-all"
                >
                    <img src='/chevron-left.svg' className="inline h-4 mb-0.5"/> Back 
                </button>
            </Link>
            <h2 className="text-4xl text-black text-center w-screen text-ui font-bold">Anything Else?</h2>
            <div className="flex gap-4 w-1/2 mx-auto mt-10 justify-around">
                <textarea
                    className="bg-white flex w-1/1 shadow-md p-4 text-black rounded-lg cursor-pointer hover:bg-[#f4f4f4f4] transition-all"
                    onChange={(event) => {
                        setSelected(event.target.value); 
                        localStorage.setItem("additionalInfo", event.target.value);
                    }}
                />
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
            <Link href={"/schedule"}>
                <button
                    className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-white cursor-pointer mt-10 hover:bg-[#f4f4f420] px-4 py-2 rounded-lg"
                >
                    That's everything!
                </button>
            </Link>

            </div>
        </div>
    )
}

export default Step3
