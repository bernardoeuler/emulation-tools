import { Button } from "@/components/ui/button"

function Hero() {
    return (
        <div className="items-center text-left mt-8 px-6 max-w-90 space-y-8">
            <h1 className="text-5xl font-bold sm:text-6xl">Online Tools for Game Emulation</h1>
            <p className="text-lg">Convert, check and manage your retro games without downloading any software</p>
            <div className="space-x-4">
                <Button className="px-4 py-6">Explore tools</Button>
                <Button variant="ghost" className="px-4 py-6">Learn more</Button>
            </div>
        </div>


    )
}

export { Hero }