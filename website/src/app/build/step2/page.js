"use client"

const Step2 = () => {
    

    return (
        <div className="mt-20">
            <h2 className="text-4xl text-black text-center w-screen text-white font-bold">Who?</h2>
            <div className="flex gap-4 w-1/2 mx-auto mt-10 justify-around">
                <div className="w-36 h-24 my-auto border border-white flex justify-center items-center text-white"><p>Alone</p></div>
                <div className="w-36 h-24 my-auto border border-white flex justify-center items-center text-white"><p>With SO</p></div>
                <div className="w-36 h-24 my-auto border border-white flex justify-center items-center text-white"><p>Friends</p></div>
                <div className="w-36 h-24 my-auto border border-white flex justify-center items-center text-white"><p>Family</p></div>
            </div>
            <p className="text-center text-white cursor-pointer mt-10">I'm flexible</p>
        </div>
    )
}

export default Step2