import Image from "next/image";

const Event = ({ event }) => {

    return (
        <div className="border border-white rounded-lg ml-12 m-8 p-4 flex gap-4">
            <img className="w-24 h-24 rounded-2xl" src={event.image}/>
            <div>
                <p className="text-white font-semibold">{event.activity}</p>
                <p className="text-sm">{event.location}</p>
            </div>

        </div>
    )
}

export default Event;