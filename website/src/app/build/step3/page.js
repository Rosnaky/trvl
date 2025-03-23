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
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">Anything Else?</h2>
            <div className="flex gap-4 w-1/2 mx-auto mt-10 justify-around">
                <textarea className="bg-white flex w-1/1"/>
            </div>
            <div className={"w-1/1 items-center justify-center flex flex-row"}>
                <Link href={"/build/step3"} className="flex opacity-60 hover:opacity-100 transition duration-200 text-center text-white cursor-pointer mt-10">I'm flexible</Link>
            </div>
        </div>
    )
}

export default Step2
