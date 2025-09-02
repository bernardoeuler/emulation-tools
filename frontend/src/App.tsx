import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  NavigationMenuLink
} from "@/components/ui/navigation-menu"

function App() {
    const [count, setCount] = useState(0)

    return (
        <div>
            <div className="flex justify-between py-4 px-40">
                <div>
                    <a href="/" className="flex items-center space-x-4">
                        {/* <img src="src/assets/logo.png" alt="Logo" className="h-10 w-auto" /> */}
                        <span className="text-xl font-bold hidden sm:inline">Emulation Tools</span>
                    </a>
                </div>

                <NavigationMenu>
                    <NavigationMenuList className="flex gap-6">
                        <NavigationMenuItem>
                            <NavigationMenuLink className="text-base" href="/tools">
                                Tools
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuLink className="text-base" href="/resources">
                                Resources
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuLink className="text-base" href="/support">
                                Support
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuLink className="text-base" href="/about">
                                About
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                    </NavigationMenuList>
                </NavigationMenu>
            </div>

            <h1>All-in-One Tools for Game Emulation</h1>
            <p>Emulation Tools makes it easy to manage, convert, and play your favorite retro games. From ROM conversion to save management and patching, everything you need to enjoy classic consoles is in one place — fast, simple, and reliable.</p>
            
        </div>
    )
}

export default App