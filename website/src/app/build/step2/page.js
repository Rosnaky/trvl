"use client"

import { useState } from "react"
import Link from "next/link"

const Step2 = () => {
    const [selected, setSelected] = useState(null)

    const options = [
        "Alone", "With SO", "Friends", "Family"
    ]

    console.log(selected);

    return (
        <div className="mt-20">
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">Who?</h2>
            <div className="flex gap-4 w-1/2 mx-auto mt-10 justify-around">
            {
                options.map((option) => {
                    return <div 
                        key={option}
                        className={"w-36 h-24 my-auto border border-white flex justify-center items-center text-white rounded-lg cursor-pointer" + (selected === option ? " bg-white/10" : " bg-transparent")}
                        onClick={() => {setSelected(option); localStorage.setItem("numPeople", option)}}>
                            <p>{option}</p>
                    </div>
                })
            }
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
                <Link href={"/build/step3"} className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-white cursor-pointer mt-10">I'm flexible</Link>
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
                <Link href={"/build/step3"}>
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

export default Step2
