import { useAdvancedMarkerRef, AdvancedMarker, InfoWindow } from "@vis.gl/react-google-maps";
import { useState, useCallback, forwardRef, useImperativeHandle } from "react";

const Marker = forwardRef(({ position, event }, ref) => {
    // `markerRef` and `marker` are needed to establish the connection between
    // the marker and infowindow (if you're using the Marker component, you
    // can use the `useMarkerRef` hook instead).
    const [markerRef, marker] = useAdvancedMarkerRef();

    const [infoWindowShown, setInfoWindowShown] = useState(false);

    // clicking the marker will toggle the infowindow
    const handleMarkerClick = useCallback(
        () => setInfoWindowShown(isShown => !isShown),
        []
    );

    // if the maps api closes the infowindow, we have to synchronize our state
    const handleClose = useCallback(() => setInfoWindowShown(false), []);

    useImperativeHandle(ref, () => ({
        infoWindowShown,
        handleMarkerClick,
        activity: event.activity
    }));

    return (
        <>
            <AdvancedMarker
                ref={markerRef}
                position={position}
                onClick={handleMarkerClick}
            />

            {infoWindowShown && (
                <InfoWindow anchor={marker} onClose={handleClose} headerContent={
                    <div className="flex gap-4 overflow-visible z-50">
                        <img src={event.image} className="h-20 w-20 rounded-lg" />
                        <div>
                            <h2 className="text-lg text-black font-medium">{event.activity}</h2>
                            <p className="text-black font-normal">{event.description}</p>
                        </div>
                    </div>
                }>

                </InfoWindow>
            )}
        </>
    );
});

export default Marker;