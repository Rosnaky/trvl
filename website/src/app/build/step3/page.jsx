"use client"

import { useState } from "react";
import Link from "next/link";

const Step1 = () => {
    const [min, setMin] = useState(0);
    const [max, setMax] = useState(0);

    return (
        <div className="flex justify-center flex-col mt-20">
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">What's your budget range?</h2>
            <div className={"text-md ml-auto mr-auto w-1/2 items-center justify-center flex flex-row mt-10 whitespace-pre text-white"}>
                <p>Minimum: </p>
                <input className="bg-white p-2 rounded-md text-gray-800 ml-3" value={min} onChange={(e) => {setMin(e.target.value)}}/>
            </div>
            <div className={"text-md ml-auto mr-auto w-1/2 items-center justify-center flex flex-row mt-10 whitespace-pre text-white"}>
                <p>Maximum: </p>
                <input className="bg-white p-2 rounded-md text-gray-800 ml-3" value={max} onChange={(e) => {setMax(e.target.value)}}/>
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
            <Link href={"/build/step4"}>
                <button
                    className="border border-white w-40 h-8 rounded-lg text-white cursor-pointer hover:bg-[#f4f4f420] transition-all opacity-100"
                    style={{ transition: "opacity 0.5s ease-in", opacity: min*max ? 1 : 0 }}
                >
                    Next -&gt;
                </button>
            </Link>
            </div>
        </div>
    )
}

export default Step1
