"use client"

import Image from "next/image";
import { useState, useEffect } from "react";
import EventTile from "./components/event-tile.jsx/event-tile";
import Link from "next/link";

export default function Home() {
  const [searchText, setSearchText] = useState("");
  const [autoCompVis, setAutoCompVis] = useState(false);
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

  const locations = [
        {
            "city": "Paris",
            "country": "France",
            "people": 3,
            "price": 325,
            "image": "https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg",
            "id": 0,
        },
        {
            "city": "Barcelona",
            "country": "Spain",
            "people": 5,
            "price": 400,
            "image": "https://www.odysseys-unlimited.com/wp-content/uploads/2023/05/AdobeStock_102733741-scaled.jpeg",
            "id": 1,
        },
        {
            "city": "Florence",
            "country": "Italy",
            "people": 2,
            "price": 250,
            "image": "https://cdn.britannica.com/59/179059-050-62BD6102/Cathedral-of-Santa-Maria-del-Fiore-Florence.jpg",
            "id": 2,
        },
        {
            "city": "Anchorage",
            "country": "United States",
            "people": 7,
            "price": 834,
            "image": "https://res.cloudinary.com/simpleview/image/upload/v1551922247/clients/anchorage/Aurora_Camp_JodyO_Photos_77ea0fae-bf4c-43be-a827-1ef25ac9c2fb.jpg",
            "id": 3,
        },
        {
            "city": "Montreal",
            "country": "Canada",
            "people": 4,
            "price": 185,
            "image": "https://www.usatoday.com/gcdn/authoring/authoring-images/2024/08/14/USAT/74794361007-36472-credit-fr-loic-romer-tourisme-montreal-en-credit-loic-romer-tourisme-montreal.jpg",
            "id": 4,
        }
  ]
  
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
          newChild.addEventListener("click", function(){setSearchText(text); setAutoCompVis(false); localStorage.setItem("latLongDest", [json.results[i].lat, json.results[i].lon]); localStorage.setItem("cityNameDest", json.results[i].city);});
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
              <Link href="/build/step0" className="group absolute bg-theme-blue left-9/10 right-0 top-0 bottom-0 hover:cursor-pointer h-1/1">
                <div className="absolute left-0 right-full group-hover:right-0 h-1/1 bg-foreground transition-right duration-500 ease-in-out"></div>
                <Image width="20" height="20" stroke="white" src={"/search.svg"} alt="" className="absolute left-3/10 right-1/5 group-hover:scale-110 transition h-3/5 mt-1.5"/>
              </Link>
            </div>
            <div id="autocomplete_container" className={`z-5 overflow-hidden text-gray-400 absolute bg-white w-1/1 max-w-200 rounded-xl border-1 border-gray-300 shadow-xl ring-black-800 ${autoCompVis ? "visible" : "invisible"}`}>
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
                {locations.map((location) => {
                    return <EventTile city={location.city} country={location.country} image={location.image} price={location.price} people={location.people} key={location.id}/>
                })}
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
