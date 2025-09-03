import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuList,
    NavigationMenuLink
} from "@/components/ui/navigation-menu"
import { MobileMenu } from "@/components/mobile-menu"

export type NavigationBarOptions = {
    item: string,
    href: string
}

export function NavigationBar() {
    const navOptions: NavigationBarOptions[] = [
        { item: "Home", href: "/" },
        { item: "Tools", href: "/tools" },
        { item: "Resources", href: "/resources" },
        { item: "Support", href: "/support" },
        { item: "About", href: "/about" },
    ]

    return (
        <header className="w-full fixed top-0 flex items-center justify-between p-4 bg-background text-foreground sm:px-8 md:px-10 lg:px-16">
            <div>
                <a href="/" className="flex items-center">
                    {/* <img src="src/assets/logo.png" alt="Logo" className="h-10 w-auto" /> */}
                    <div className="text-lg font-bold">Emulation Tools</div>
                </a>
            </div>

            <NavigationMenu className="hidden md:flex">
                <NavigationMenuList className="flex gap-6">
                    {Array.from(navOptions).map((option, i) => {
                        return (
                            <NavigationMenuItem key={i}>
                                <NavigationMenuLink className="text-base py-0" href={option.href}>{option.item}</NavigationMenuLink>
                            </NavigationMenuItem>
                        )
                    })}
                </NavigationMenuList>
            </NavigationMenu>
            <MobileMenu className="md:hidden" menuOptions={navOptions} />
        </header>
    )
}