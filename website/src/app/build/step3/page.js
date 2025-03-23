"use client"

import { useState } from "react";
import Link from "next/link";
import { ToastContainer, toast } from 'react-toastify';

const Step3 = () => {
    const [min, setMin] = useState(localStorage.getItem("min") || 0);
    const [max, setMax] = useState(localStorage.getItem("max") || 0);
    const notify = (message) => toast.error(message, {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: false,
        progress: undefined,
    });

    return (
        <div className="flex justify-center flex-col mt-20">
            <Link href={"/build/step2"}>
                <button
                    className="ml-30 mb-12 text-white px-8 py-2 rounded-lg border-white cursor-pointer hover:bg-[#f4f4f420] transition-all"
                >
                    <img src='/chevron-left.svg' className="inline h-4 mb-0.5"/> Back 
                </button>
            </Link>
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">What's your budget range?</h2>
            <div className={"text-md ml-auto mr-auto w-1/2 items-center justify-center flex flex-row mt-10 whitespace-pre text-white"}>
                <p>Minimum: </p>
                <input className="bg-white p-2 rounded-md text-gray-800 ml-3 placeholder-0" value={min} type="number"
                    onChange={(e) => {
                        setMin(e.target.value)                        
                    }}
                    onBlur={() => {
                        if (min > max) {
                            notify("Minimum cannot be more than maximum")
                            setMin(Math.min(min, max))
                        }
                        localStorage.setItem("min", min)
                    }}
                />
            </div>
            <div className={"text-md ml-auto mr-auto w-1/2 items-center justify-center flex flex-row mt-10 whitespace-pre text-white"}>
                <p>Maximum: </p>
                <input className="bg-white p-2 rounded-md text-gray-800 ml-3" value={max} min={min} type="number"
                    onChange={(e) => {
                        setMax(e.target.value)
                    }}
                    onBlur={() => {
                        if (max < min) {
                            notify("Maximum cannot be less than minimum")
                            setMax(Math.max(max, min))
                        }
                        localStorage.setItem("max", max)
                    }}
                />
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
                <Link href={"/build/step4"}>
                    <button
                        className="border border-white px-8 py-2 rounded-lg text-white cursor-pointer hover:bg-[#f4f4f420] transition-all opacity-100"
                        style={{ transition: "opacity 0.5s ease-in", opacity: min+max ? 1 : 0 }}
                    >
                        Next <img src='/chevron-right.svg' className="inline h-4 mb-0.5 -mr-2"/>
                    </button>
                </Link>
            </div>
            </div>
            <ToastContainer />
        </div>
    )
}

export default Step3
