"use client"

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [searchText, setSearchText] = useState("");

  return (
    <div className="w-screen h-screen bg-background flex justify-center items-center">
       <div className="flex justify-center flex-col h-3/4 w-3/4 gap-10 max-w-300 min-w-100 max-h-600">
        <div className="flex justify-center">
          <p className="flex text-white text-8xl">TRVL</p>
        </div>
        <div className="min-w">

        </div>
        <div className="flex flex-row justify-center">
          <div className="overflow-hidden relative w-1/1 max-w-200 min-h-10 rounded-xl bg-white justify-center items-center pl-5">
            <input value={searchText} onChange={(e) => {setSearchText(e.target.value)}} placeholder={"Where to next?"} className="border-0 text-gray-600 outline-0 mt-auto mb-auto"></input>
            <div className="absolute bg-tertiary left-9/10 right-0 top-0 bottom-0">
              <img src={"/search.svg"} alt="" className="margin-auto"/>
            </div>
          </div>
        </div>
      </div> 
    </div>
  );
}

