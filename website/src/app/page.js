"use client"

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [searchText, setSearchText] = useState("");
  const [autoCompVis, setAutoCompVis] = useState(false);
  const [timeoutID, setTimeoutID] = useState("");
  const [longLat, setLongLat] = useState([-1, -1]);
  const [slide, setSlide] = useState(0);

  const carouselScroll = (dir) => {
    const car = document.getElementById("carousel").children[0];
    if(dir == 1) {
      let child = car.children[0];
      car.removeChild(child);
      car.appendChild(child);
    }
    else {
      let child = car.children[car.children.length-1];
      car.removeChild(child);
      car.insertBefore(child, car.children[0]);
    }
    setSlide((slide+dir)%5);
  }

  const autocomplete = (newVal) => {
    /**if(timeoutID != "") {
      clearTimeout(timeoutID);
    }
    let temp_id = setTimeout(autocompleteReal(newVal), 500);
    console.log(temp_id);
    setTimeoutID(temp_id);**/
    autocompleteReal(newVal);
  }
  
  async function autocompleteReal(newVal) {
    const autocomp = document.getElementById("autocomplete_container");
    setSearchText(newVal);
    setTimeoutID("");
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
              else {
                console.log(json.results[i].city);
                console.log(autocomp.children[j].city);
                console.log(json.results[i].state);
                console.log(autocomp.children[j].state);
                console.log(json.results[i].country);
                console.log(autocomp.children[j].country);
              }
            }
          }
          let newChild = document.createElement("div");
          newChild.className = "min-h-7 pl-3 align-items text-gray-400 hover:bg-gray-100 hover:cursor-pointer";
          let text = `${json.results[i].city}, ${json.results[i].state}, ${json.results[i].country}`;
          newChild.addEventListener("click", function(){setSearchText(text); setAutoCompVis(false);});
          newChild.appendChild(document.createTextNode(text));
          newChild.hiddenData = [json.results[i].lat, json.results[i].lon];
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
  }

  return (
    <div className="w-screen h-screen bg-background flex justify-center items-center">
      <div className="flex justify-center flex-col h-3/4 w-3/4 gap-10 max-w-300 min-w-100 max-h-600">
        <div className="flex flex-shrink justify-center">
          <div className="flex flex-col justify-center">
            <p className="flex text-theme-blue text-8xl font-mono font-semibold">trvl</p>
            <p className="flex justify-center text-md text-theme-blue font-semibold whitespace-pre">Make planning your travel trivial</p>
          </div>
        </div>
        <div className="relative flex-col justify-center items-center">
          <div className="ml-auto mr-auto w-1/1 max-w-200 justify-center">
            <div className="overflow-hidden flex-row relative min-h-10 rounded-xl bg-white items-center border-1 border-gray-400 shadow-xl ring-black-800">
              <input onBlur={(e) => {setTimeout(function(){setAutoCompVis(false)}, 300)}} onFocus={(e) => {setAutoCompVis(true); autocomplete(searchText)}} value={searchText} onChange={(e) => {setAutoCompVis(true); autocomplete(e.target.value);}} placeholder={"Where to next?"} className="border-0 text-gray-600 outline-0 mt-1.5 absolute left-1/40 right-3/20"></input>
              <div className="group absolute bg-theme-blue left-9/10 right-0 top-0 bottom-0 hover:cursor-pointer h-1/1">
              <div className="absolute left-0 right-full group-hover:right-0 h-1/1 bg-foreground transition-right duration-500 ease-in-out"></div>
                <Image width="20" height="20" stroke="white" src={"/search.svg"} alt="" className="absolute left-3/10 right-1/5 group-hover:scale-110 transition h-3/5 mt-1.5"/>
                
              </div>
            </div>
            <div id="autocomplete_container" className={`overflow-hidden text-gray-400 absolute bg-white w-1/1 max-w-200 rounded-xl border-1 border-gray-300 shadow-xl ring-black-800 ${autoCompVis ? "visible" : "invisible"}`}>
            </div>
          </div>
        </div>
        <div className="overflow-hidden flex flex-grow justify-between items-center gap-10 mt-4 w-1/1">
          <div onClick={() => {setTimeout(function(){carouselScroll(-1)}, 300); /**setSlide(true)**/}} className="group hover:cursor-pointer hover:to-background/10 z-2 relative left-0 bg-linear-to-r from-background to-background/0 h-1/1 w-1/8 min-w-10">
            <div className="flex h-1/1 w-1/1 justify-center items-center">
              <Image width="35" height="35" stroke="red" src={"/chevron-left.svg"} alt="" className="z-2 flex min-h-7 h-1/7 opacity-50 group-hover:scale-105 group-hover:opacity-100 transition duration-200"/>
            </div>
          </div>

          <div className="relative h-1/1 w-1/1">
            <div id="carousel" className={`absolute -left-200 -right-200 -translate-x-${slide}/5 top-0 bottom-0 transition ease-in-out duration-300`}>
              <div className="flex flex-row justify-center items-center gap-10 h-1/1">
                <div className="hover:scale-115 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
                  <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src="https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"/>
                  <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
                    <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
                      <div className="flex-3 items-start flex-col min-h-3">
                        <p className="flex text-lg whitespace-pre">Paris,</p>
                        <p className="flex text-sm">France</p>
                      </div>
                      <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
                        <p className="text-3xl font-bold">3</p>
                        <p className="text-sm pb-2">people</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="hover:scale-115 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
                  <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src="https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"/>
                  <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
                    <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
                      <div className="flex-3 items-start flex-col min-h-3">
                        <p className="flex text-lg whitespace-pre">Paris,</p>
                        <p className="flex text-sm">France</p>
                      </div>
                      <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
                        <p className="text-3xl font-bold">3</p>
                        <p className="text-sm pb-2">people</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="hover:scale-115 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
                  <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src="https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"/>
                  <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
                    <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
                      <div className="flex-3 items-start flex-col min-h-3">
                        <p className="flex text-lg whitespace-pre">Paris,</p>
                        <p className="flex text-sm">France</p>
                      </div>
                      <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
                        <p className="text-3xl font-bold">3</p>
                        <p className="text-sm pb-2">people</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="hover:scale-115 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
                  <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src="https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"/>
                  <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
                    <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
                      <div className="flex-3 items-start flex-col min-h-3">
                        <p className="flex text-lg whitespace-pre">Paris,</p>
                        <p className="flex text-sm">France</p>
                      </div>
                      <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
                        <p className="text-3xl font-bold">3</p>
                        <p className="text-sm pb-2">people</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="hover:scale-115 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
                  <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src="https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"/>
                  <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
                    <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
                      <div className="flex-3 items-start flex-col min-h-3">
                        <p className="flex text-lg whitespace-pre">Paris,</p>
                        <p className="flex text-sm">France</p>
                      </div>
                      <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
                        <p className="text-3xl font-bold">3</p>
                        <p className="text-sm pb-2">people</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="hover:scale-115 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
                  <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src="https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"/>
                  <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
                    <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
                      <div className="flex-3 items-start flex-col min-h-3">
                        <p className="flex text-lg whitespace-pre">Paris,</p>
                        <p className="flex text-sm">France</p>
                      </div>
                      <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
                        <p className="text-3xl font-bold">3</p>
                        <p className="text-sm pb-2">people</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div onClick={() => {setTimeout(function(){carouselScroll(1)}, 300); /**setSlide(true)**/}} className="group hover:cursor-pointer hover:to-background/10 z-2 relative left-0 bg-linear-to-l from-background to-background/0 h-1/1 w-1/8 min-w-10">
            <div className="flex h-1/1 w-1/1 justify-center items-center">
              <Image width="35" height="35" stroke="red" src={"/chevron-right.svg"} alt="" className="z-2 flex min-h-7 h-1/7 opacity-50 group-hover:scale-105 group-hover:opacity-100 transition duration-200"/>
            </div>
          </div>
        </div>
      </div> 
    </div>
  );
}

