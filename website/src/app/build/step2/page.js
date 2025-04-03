"use client"

import { useState } from "react"
import Link from "next/link"

const Step2 = () => {
    const options = [
        ["Alone 😔", 1],
        ["With SO 💑", 2],
        ["Friends 👥", 6],
        ["Family 👪", 4]
    ]

    const [selected, setSelected] = useState(options.find(([option, numPeople]) => numPeople === parseInt(localStorage.getItem("numPeople")))?.[0] || null)
    
    return (
        <div className="mt-20">
            <Link href={"/build/step1"}>
                <button
                    className="ml-30 mb-12 text-ui px-8 py-2 rounded-lg border-ui cursor-pointer hover:bg-[#f4f4f420] transition-all"
                >
                    <img src='/chevron-left.svg' className="inline h-4 mb-0.5"/> Back 
                </button>
            </Link>
            <h2 className="text-4xl text-black text-center w-screen text-ui font-bold">Who?</h2>
            <div className="flex gap-4 w-1/2 mx-auto mt-10 justify-around">
            {
                options.map(([option, numPeople]) => {
                    return <div 
                        key={option}
                        className={"w-36 py-6 my-auto border border-ui flex justify-center items-center text-ui rounded-lg cursor-pointer hover:bg-white/10" + (selected === option ? " bg-white/20" : " bg-transparent")}
                        onClick={() => {
                            setSelected(selected === option ? null : option)
                            localStorage.setItem("numPeople", numPeople)
                        }}>
                            <p>{option}</p>
                    </div>
                })
            }
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
                <Link href={"/build/step3"} className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-ui cursor-pointer mt-10"
                    onClick={() => {
                        localStorage.setItem("numPeople", null)
                    }}>
                        I'm flexible
                </Link>
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
                <Link href={"/build/step3"}>
                    <button
                        className="border border-ui px-8 py-2 rounded-lg text-ui cursor-pointer hover:bg-[#f4f4f420] transition-all opacity-100"
                        style={{ transition: "opacity 0.5s ease-in", opacity: selected ? 1 : 0 }}
                    >
                        Next <img src='/chevron-right.svg' className="inline h-4 mb-0.5 -mr-2"/>
                    </button>
                </Link>
            </div>
        </div>
    )
}

export default Step2
