import Event from "./event"

const Day = ({ day, dayNum, markerRefs }) => {
    return (
        <div className="bg-white/10 rounded-lg p-4 mb-8">
            <h4 className="text-2xl text-white font-semibold mt-4 ml-12 mb-8">Day {dayNum + 1} - Paris, France</h4>
            {day.map((event) => {
                return <Event key={event.activity} event={event} markerRefs={markerRefs} />
            })}
        </div>
    )
}

export default Day;
