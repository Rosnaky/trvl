"use client"

import { useState } from "react";
import { DayPicker } from "react-day-picker";
import "react-day-picker/style.css";
import './calendar.css'
import Link from "next/link";

const Step1 = () => {
    const [selected, setSelected] = useState(false);

    return (
        <div className="flex flex-col mt-20">
            <Link href={"/build/step0"}>
                <button
                    className="ml-30 mb-4 text-white px-8 py-2 rounded-lg border-white cursor-pointer hover:bg-[#f4f4f420] transition-all"
                >
                    <img src='/chevron-left.svg' className="inline h-4 mb-0.5"/> Back 
                </button>
            </Link>
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">When?</h2>
            <div className="mt-16">
                <DayPicker
                    animate
                    className="text-white flex justify-center"
                    mode="range"
                    numberOfMonths={2}
                    min={1}
                    max={7}
                    selected={selected}
                    onSelect={(value) => {
                        setSelected(value);
                        if (value?.from && value?.to) {
                            const formattedFrom = value.from.toISOString().split("T")[0]; // Convert to YYYY-MM-DD
                            const formattedTo = value.to.toISOString().split("T")[0]; // Convert to YYYY-MM-DD
                            localStorage.setItem("date", JSON.stringify({ from: formattedFrom, to: formattedTo }));
                        }
                    }}
                />
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
                <Link href={"/build/step2"} className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-white cursor-pointer mt-4">I'm flexible</Link>
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-8">
            <Link href={"/build/step2"}>
                <button
                    className="border border-white px-8 py-2 rounded-lg text-white cursor-pointer hover:bg-[#f4f4f420] transition-all opacity-100"
                    style={{ transition: "opacity 0.5s ease-in", opacity: selected ? 1 : 0 }}
                >
                    Next <img src='/chevron-right.svg' className="inline h-4 mb-0.5 -mr-2"/>
                </button>
            </Link>
            </div>
        </div>
    )
}

export default Step1
