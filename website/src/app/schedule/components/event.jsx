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
        <div className="bg-white/20 ml-12 mr-12 mt-4 rounded-xl mb-8 relative gap-8 cursor-pointer object-cover over min-h-40 overflow-hidden" onMouseEnter={setCenter} onClick={openWindow}>
            <img className="absolute saturate-80 w-2/9 h-1/1 object-cover" src={event.image}/>
            <div className="absolute left-19/80 top-2">
                <p className="text-white font-semibold text-xl">{event.activity}</p>
                <p className="text-sm text-white">{event.type}</p>
            </div>

        </div>
    )
}

export default Event;
