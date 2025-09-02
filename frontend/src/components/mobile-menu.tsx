import { Button } from "@/components/ui/button"
import {
    Sheet,
    SheetClose,
    SheetContent,
    SheetTrigger,
} from "@/components/ui/sheet"
import { Menu } from "lucide-react"

import type { NavigationBarOptions } from "@/components/navigation-bar"

export function MobileMenu({ className, menuOptions }: { className: string, menuOptions: NavigationBarOptions[] }) {
    return (
        <div className={`${className}`}>
            <Sheet>
                <SheetTrigger asChild>
                    <Menu>Open</Menu>
                </SheetTrigger>
                <SheetContent className="flex flex-col text-center px-8 py-16">
                    {Array.from(menuOptions).map((option, i) => {
                        return (
                            <div key={i}>
                                <a className="text-lg" href={option.href}>{option.item}</a>
                            </div>
                        )
                    })}
                </SheetContent>
            </Sheet>
        </div>
    )
}
