const EventTile = ({ city, country, image, price, people }) => {
  return (
    <div className="hover:scale-110 hover:shadow-sm transition-scale duration-150 relative rounded-lg overflow-hidden max-w-70 h-1/1 w-2/3 bg-white min-w-40 min-h-40 max-h-70">
        <img className="object-cover absolute w-1/1 h-3/4" width="10" height="10" src={image}/>
        <div className="opacity-80 absolute w-1/4 min-w-15 h-10 bg-black left-3 top-3">
            <p className="text-lg text-center mt-1.5 font-semibold text-white">${price}</p>
        </div>
        <div className="absolute w-1/1 top-3/4 bottom-0 bg-tertiary min-h-10">
        <div className="flex-3 flex w-5/6 m-auto justify-center items-center h-1/1 text-background">
            <div className="flex-3 items-start flex-col min-h-3">
            <p className="flex text-lg whitespace-pre">{city},</p>
            <p className="flex text-sm">{country}</p>
            </div>
            <div className="flex flex-col justify-center items-center h-1/1 min-w-3 min-h-3">
            <p className="text-3xl font-bold">{people}</p>
            <p className="text-sm pb-2">people</p>
            </div>
        </div>
        </div>
    </div>
  );
};

export default EventTile;
