"use client"

import { useState } from "react";
import Link from "next/link";


const Step0 = () => {
    const [searchText, setSearchText] = useState(localStorage.getItem("cityNameOrigin") || "");
    const [autoCompVis, setAutoCompVis] = useState(false);

    async function autocomplete(newVal) {
        const autocomp = document.getElementById("autocomplete_container");
        setSearchText(newVal);
        if(newVal.length >= 4) {
            const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${newVal}&limit=3&type=city&format=json&apiKey=7430b011e2ce4d42b547e4d108ff75c5`;
            try {
            const response = await fetch(url);
            if(!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            const json = await response.json();
            for(; autocomp.children.length != 0; autocomp.removeChild(autocomp.children[0]));
            for(let i = 0; i < json.results.length; i++) {
                if(!json.results[i].city || !json.results[i].state || !json.results[i].country) {
                continue;
                }
                else {
                for(let j = 0; j < autocomp.children.length; j++) {
                    if(json.results[i].city == autocomp.children[j].city && json.results[i].state == autocomp.children[j].state && json.results[i].country == autocomp.children[j].country) {
                    continue;
                    }
                }
                }
                let newChild = document.createElement("div");
                newChild.className = "min-h-7 pl-3 align-items text-gray-400 hover:bg-gray-100 hover:cursor-pointer";
                let text = `${json.results[i].city}, ${json.results[i].state}, ${json.results[i].country}`;
                newChild.addEventListener("click", function(){
                    setSearchText(text); 
                    setAutoCompVis(false); 
                    localStorage.setItem("cityNameOrigin", json.results[i].city);
                    localStorage.setItem("latLongOrigin", [json.results[i].lat, json.results[i].lon]);
                });
                newChild.appendChild(document.createTextNode(text))
                autocomp.appendChild(newChild);
            }
            }
            catch (error) {
            console.error(error.message);
            }
        }
        else {
            for(; autocomp.children.length != 0; autocomp.removeChild(autocomp.children[0]));
            if(newVal.length > 0) {
                let newChild = document.createElement("div");
                newChild.className = "min-h-7 pl-3 align-items text-gray-400";
                newChild.appendChild(document.createTextNode("..."));
                autocomp.appendChild(newChild);
            }
            else {
                setAutoCompVis(false);
            }
        }
    };

    return (
        <div className="mt-20">
                <Link href={"/"}>
                    <button
                        className="ml-30 mb-10 text-ui px-8 py-2 rounded-lg border-white cursor-pointer hover:bg-[#f4f4f420] transition-all"
                    >
                    <img src='/chevron-left.svg' className="inline h-4 mb-0.5 -ml-1"/> Back 
                    </button>
                </Link>
            <h2 className="text-4xl text-black text-center w-screen text-ui font-bold mb-9">Where are you coming from?</h2>
            <div className="relative flex-col justify-center items-center">
                <div className="ml-auto mr-auto w-1/1 max-w-200 justify-center">
                    <div className="overflow-hidden flex-row relative min-h-10 rounded-xl bg-white items-center border-1 border-gray-400 shadow-xl ring-black-800">
                        <input onBlur={(e) => {setTimeout(function(){setAutoCompVis(false)}, 300)}} onFocus={(e) => {setAutoCompVis(true); autocomplete(searchText)}} value={searchText} onChange={(e) => {setAutoCompVis(true); autocomplete(e.target.value);}} placeholder={"I'm leaving from..."} className="border-0 text-gray-600 outline-0 mt-1.5 absolute left-1/40 right-3/20"></input>
                    </div>
                    <div id="autocomplete_container" className={`z-5 overflow-hidden text-gray-400 absolute bg-white w-1/1 max-w-200 rounded-xl border-1 border-gray-300 shadow-xl ring-black-800 ${autoCompVis ? "visible" : "invisible"}`}>
                    </div>
                </div>
            </div>
            <div className="flex flex-row-reverse w-1/2 mx-auto mt-10">
                <Link href={"/build/step1"}>
                    <button
                        className="border border-ui px-8 py-2 rounded-lg text-ui cursor-pointer hover:bg-[#f4f4f420] transition-all opacity-100"
                        style={{ transition: "opacity 0.5s ease-in", opacity: searchText.split(',').length === 3 ? 1 : 0 }}
                    >
                        Next <img src='/chevron-right.svg' className="inline h-4 mb-0.5 -mr-2"/>
                    </button>
                </Link>
            </div>
        </div>
    )
}

export default Step0
