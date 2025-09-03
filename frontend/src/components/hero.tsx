import { Button } from "@/components/ui/button"

function Hero() {
    return (
        <div className="flex flex-wrap items-center gap-8 pt-20 px-4 sm:pt-22 sm:px-8 md:pt-30 md:px-10 lg:px-16 bg-background text-foreground">
            <div className="basis-110 grow text-left space-y-8 lg:mx-0">
                <h1 className="text-5xl font-semibold sm:text-7xl">Online tools for game emulation</h1>
                <p className="text-lg sm:text-xl">Convert, check and manage your retro games without downloading any extra software. Emulation Tools does it for you.</p>
                <div className="space-x-4">
                    <Button className="text-sm px-4 py-6 sm:text-base">Explore tools</Button>
                    <Button variant="ghost" className="text-sm px-4 py-6 sm:text-base">Learn more</Button>
                </div>
            </div>
            <div className="basis-100 grow">
                <img className="w-full" src="src/assets/images/hero-image.svg" alt="Game image" />
            </div>
        </div>


    )
}

export { Hero }