"use client"

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";

const Step0 = () => {
    const [searchText, setSearchText] = useState("");
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
        <div className="mt-30">
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold mb-9">Where are you coming from?</h2>
            <div className="relative flex-col justify-center items-center">
                <div className="ml-auto mr-auto w-1/1 max-w-200 justify-center">
                    <div className="overflow-hidden flex-row relative min-h-10 rounded-xl bg-white items-center border-1 border-gray-400 shadow-xl ring-black-800">
                        <input onBlur={(e) => {setTimeout(function(){setAutoCompVis(false)}, 300)}} onFocus={(e) => {setAutoCompVis(true); autocomplete(searchText)}} value={searchText} onChange={(e) => {setAutoCompVis(true); autocomplete(e.target.value);}} placeholder={"I'm leaving from..."} className="border-0 text-gray-600 outline-0 mt-1.5 absolute left-1/40 right-3/20"></input>
                        <Link href="/build/step1/" className={`${localStorage.getItem("latLongDest")[0] != -1 ? "group hover:cursor-pointer" : ""} absolute bg-theme-blue left-9/10 right-0 top-0 bottom-0 h-1/1`}>
                            <div className="absolute left-0 right-full group-hover:right-0 h-1/1 bg-foreground transition-right duration-500 ease-in-out"></div>
                            <Image width="20" height="20" stroke="white" src={"/search.svg"} alt="" className="absolute left-3/10 right-1/5 group-hover:scale-110 transition h-3/5 mt-1.5"/>
                        </Link>
                    </div>
                    <div id="autocomplete_container" className={`z-5 overflow-hidden text-gray-400 absolute bg-white w-1/1 max-w-200 rounded-xl border-1 border-gray-300 shadow-xl ring-black-800 ${autoCompVis ? "visible" : "invisible"}`}>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Step0
