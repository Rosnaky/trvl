/**"use client"

import Day from "./components/day";
import { APIProvider, Map, AdvancedMarker } from '@vis.gl/react-google-maps';
import Marker from "./components/marker";
import { useRef } from "react";

const Page = () => {
    const markerRefs = useRef([]);


    const schedule = [
        [
            {
                "time": "9:00 AM",
                "activity": "Eiffel Tower Visit",
                "description": "Ascend the Eiffel Tower for panoramic views of Paris. Book tickets in advance.",
                "location": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris",
                "transportation": "Metro: Bir-Hakeim (Line 6), Trocadéro (Line 9)",
                "price": 20.0,
                "latitude": 48.8584,
                "longitude": 2.2945,
                "type": "Sightseeing",
                "image": "https://www.planetware.com/photos-large/F/france-paris-eiffel-tower.jpg"
            },
            {
                "time": "12:30 PM",
                "activity": "Parisian Bistro Lunch",
                "description": "Enjoy classic French cuisine like croque monsieur or steak frites.",
                "location": "Nearby bistro in the 7th arrondissement",
                "transportation": "Walking",
                "price": 25.0,
                "latitude": 48.8560,
                "longitude": 2.3050,
                "type": "Dining",
                "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQI221k-pVhrINHi4iDcLBMjca-chTk3eT2WQ&s"
            },
            {
                "time": "2:00 PM",
                "activity": "Louvre Museum Visit",
                "description": "Explore world-renowned art, including the Mona Lisa and Venus de Milo.",
                "location": "Rue de Rivoli, 75001 Paris",
                "transportation": "Metro: Palais Royal-Musée du Louvre (Line 1, 7)",
                "price": 17.0,
                "latitude": 48.8606,
                "longitude": 2.3376,
                "type": "Museum/Art",
                "image": "https://api-www.louvre.fr/sites/default/files/2021-01/cour-napoleon-et-pyramide_1.jpg"
            },
            {
                "time": "6:00 PM",
                "activity": "Seine River Cruise",
                "description": "Enjoy a relaxing cruise along the Seine River, passing iconic landmarks.",
                "location": "Various departure points along the Seine",
                "transportation": "Metro: Various, depending on departure point",
                "price": 20.0,
                "latitude": 48.8566,
                "longitude": 2.3522,
                "type": "Sightseeing/Cruise",
                "image": "https://media.tacdn.com/media/attractions-splice-spp-674x446/0a/a9/c0/04.jpg"
            },
            {
                "time": "8:30 PM",
                "activity": "Latin Quarter Dinner",
                "description": "Dine in a charming restaurant in the lively Latin Quarter.",
                "location": "Latin Quarter, 5th arrondissement",
                "transportation": "Metro: Cluny-La Sorbonne (Line 10)",
                "price": 35.0,
                "latitude": 48.8530,
                "longitude": 2.3460,
                "type": "Dining",
                "image": "https://static.toiimg.com/thumb/msid-83005872,width-1280,height-720,resizemode-4/83005872.jpg"
            }
        ],
        [
            {
                "time": "9:30 AM",
                "activity": "Notre-Dame & Sainte-Chapelle",
                "description": "See Notre-Dame (exterior) and Sainte-Chapelle's stained glass.",
                "location": "Île de la Cité, 75001 Paris",
                "transportation": "Metro: Cité (Line 4)",
                "price": 11.50,
                "latitude": 48.8530,
                "longitude": 2.3499,
                "type": "Sightseeing/Historical",
                "image": "https://www.planetware.com/photos-large/F/france-paris-notre-dame-cathedral.jpg"
            },
            {
                "time": "12:30 PM",
                "activity": "Cafe Lunch near Île de la Cité",
                "description": "Enjoy a light lunch or sandwich.",
                "location": "Near Île de la Cité",
                "transportation": "Walking",
                "price": 17.50,
                "latitude": 48.8530,
                "longitude": 2.3499,
                "type": "Dining",
                "image": "https://www.thespruceeats.com/thmb/6v73qfJ593v9h1-i23G7866N228=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/ParisCafe-GettyImages-523171120-058b76c8c0894e4395a1262d05779774.jpg"
            },
            {
                "time": "2:00 PM",
                "activity": "Montmartre & Sacré-Cœur",
                "description": "Explore Montmartre and visit the Sacré-Cœur Basilica.",
                "location": "Montmartre, 18th arrondissement",
                "transportation": "Metro: Anvers (Line 2), Abbesses (Line 12)",
                "price": 0.0,
                "latitude": 48.8864,
                "longitude": 2.3430,
                "type": "Sightseeing/Cultural",
                "image": "https://www.planetware.com/photos-large/F/france-paris-sacre-coeur-basilica.jpg"
            },
            {
                "time": "6:00 PM",
                "activity": "Galeries Lafayette Shopping",
                "description": "Browse the department store and enjoy the rooftop views.",
                "location": "40 Boulevard Haussmann, 75009 Paris",
                "transportation": "Metro: Chaussée d'Antin-La Fayette (Line 7, 9)",
                "price": 0.0,
                "latitude": 48.8739,
                "longitude": 2.3310,
                "type": "Shopping",
                "image": "https://www.galerieslafayette.com/files/live/sites/galerieslafayette/files/02_GL_Haussmann/01_Actus/2023/07_Juillet/04_rooftop_terrasse/Galeries-Lafayette-Paris-Haussmann-Terrasse-Rooftop-Vue-Paris-1920x1080.jpg"
            },
            {
                "time": "8:30 PM",
                "activity": "Marais District Dinner",
                "description": "Enjoy a trendy dinner in the Marais.",
                "location": "Marais district, 3rd and 4th arrondissements",
                "transportation": "Metro: Saint-Paul (Line 1)",
                "price": 40.0,
                "latitude": 48.8576,
                "longitude": 2.3590,
                "type": "Dining",
                "image": "https://www.timeout.com/paris/restaurants/le-marais-best-restaurants"
            }
        ]
    ]

    const scheduleMarkers = schedule.flat(1).map((event, idx) => {
        console.log(markerRefs[idx])
        return <Marker ref={(el) => (markerRefs.current[idx] = el)}
        key={event.activity} position={{ lat: event.latitude, lng: event.longitude }} event={event} />
    })

    return (
        <APIProvider apiKey={process.env.NEXT_PUBLIC_GMAPS_API_KEY}>
            <div className="px-12 flex gap-12">
                <div className="w-3/5 pt-20">
                    <h3 className="text-4xl text-center text-white font-semibold pb-12">2 Day Trip to Paris</h3>
                    {
                        schedule.map((day, idx) => {
                            return <Day key={idx} day={day} dayNum={idx} markerRefs={markerRefs} />
                        })
                    }
                </div>
                <div>
                    <div className="w-3/10 py-20 fixed h-6/5">
                        <Map
                            style={{ width: '100%', height: '80%' }}
                            defaultCenter={{ lat: schedule[0][0].latitude, lng: schedule[0][0].longitude }}
                            defaultZoom={13}
                            mapId="ee0d23538130ee44"
                            gestureHandling={'greedy'}
                        >
                            {scheduleMarkers}
                        </Map>
                    </div>
                </div>
            </div>
        </APIProvider>
    )
}

export default Page;**/
