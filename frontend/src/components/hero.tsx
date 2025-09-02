import { Button } from "@/components/ui/button"

function Hero() {
    return (
        <div className="h-screen w-full bg-[url('src/assets/images/hero-image.jpg')] bg-cover bg-center pt-20 px-4 sm:pt-22 sm:px-8 md:pt-30 md:px-10 lg:px-16">
            <div className="absolute top-15 inset-0 bg-white/70 backdrop-brightness-50"></div>
            <div className="relative z-10 text-left space-y-8 sm:max-w-160 md:max-w-180 lg:mx-0">
                <h1 className="text-5xl font-semibold sm:text-7xl">Online tools for game emulation</h1>
                <p className="text-lg sm:text-xl">Convert, check and manage your retro games without downloading any extra software. Emulation Tools does it for you.</p>
                <div className="space-x-4">
                    <Button className="text-sm px-4 py-6 sm:text-base">Explore tools</Button>
                    <Button variant="ghost" className="text-sm px-4 py-6 sm:text-base">Learn more</Button>
                </div>
            </div>
        </div>


    )
}

export { Hero }