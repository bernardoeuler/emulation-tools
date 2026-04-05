import { Hero } from "@/components/hero"
import { NavigationBar } from "@/components/navigation-bar"

function App() {
    return (
        <div className="min-h-dvh bg-background">
            <NavigationBar />
            <Hero />
        </div>
    )
}

export default App