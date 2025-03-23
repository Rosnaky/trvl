import { useMap } from "@vis.gl/react-google-maps";

const Event = ({ event, markerRefs }) => {
    const map = useMap();

    const setCenter = () => {
        map.setCenter({lat: event.latitude, lng: event.longitude})
        openWindow()
    };
    
    const openWindow = () => {
        markerRefs.current.filter(e => event.activity != e.activity).forEach(e => {
            console.log(e)
            if (e.infoWindowShown) e.handleMarkerClick();
        });

        markerRefs.current.find(e => event.activity == e.activity).handleMarkerClick()
    }

    return (
        <div className="border border-[#77777777] rounded-lg ml-12 m-8 p-4 flex gap-4 cursor-pointer" onMouseEnter={setCenter} onClick={openWindow}>
            <img className="w-28 h-28 rounded-2xl" src={event.image}/>
            <div>
                <p className="text-white font-semibold text-xl">{event.activity}</p>
                <p className="text-sm text-white">{event.type}</p>
            </div>

        </div>
    )
}

export default Event;