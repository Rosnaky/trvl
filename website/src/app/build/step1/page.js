"use client"

import { useState } from "react";

import { DayPicker } from "react-day-picker";
import "react-day-picker/style.css";
import './calendar.css'
import Link from "next/link";

const Step1 = () => {
    const [selected, setSelected] = useState(false);

    console.log(selected)

    return (
        <div className="flex flex-col mt-20">
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">When?</h2>
            <div className="mt-20">
                <DayPicker
                    animate
                    className="text-white flex justify-center"
                    mode="range"
                    numberOfMonths={2}
                    min={1}
                    max={7}
                    selected={selected}
                    onSelect={setSelected}
                />
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
                <Link href="/build/step2" className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-white cursor-pointer mt-10">I'm flexible</Link>
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
            <Link href="/build/step2">
                <button
                    className="border border-white w-40 h-8 rounded-lg text-white cursor-pointer hover:bg-[#f4f4f420] transition-all opacity-100"
                    style={{ transition: "opacity 0.5s ease-in", opacity: selected ? 1 : 0 }}
                >
                    Next -&gt;
                </button>
            </Link>
            </div>
        </div>
    )
}

export default Step1
