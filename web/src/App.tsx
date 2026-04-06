import { NavigationBar } from "@/components/navigation-bar"
import { PS1Converter } from "@/components/ps1-converter"

function App() {
    return (
        <div className="min-h-dvh bg-background">
            <NavigationBar />
            <PS1Converter />
        </div>
    )
}

export default App