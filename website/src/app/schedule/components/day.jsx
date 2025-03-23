import Event from "./event"

const Day = ({ day, dayNum, markerRefs }) => {
    return (
        <div className="border border-[#AAAAAAAA] rounded-lg p-4">
            <h4 className="text-2xl text-white font-semibold">Day {dayNum + 1} - Paris, France</h4>
            {day.map((event) => {
                return <Event key={event.activity} event={event} markerRefs={markerRefs} />
            })}
        </div>
    )
}

export default Day;