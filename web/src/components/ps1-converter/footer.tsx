import { Button } from "@/components/ui/button"

interface FooterLink {
  label: string
  href: string
}

interface FooterProps {
  links?: FooterLink[]
  companyName?: string
  year?: number
}

const DEFAULT_LINKS: FooterLink[] = [
  { label: "Tools", href: "/tools" },
  { label: "Resources", href: "/resources" },
  { label: "Support", href: "/support" },
  { label: "About", href: "/about" },
]

export function Footer({
  links = DEFAULT_LINKS,
  companyName = "Emulation Tools",
  year = new Date().getFullYear()
}: FooterProps) {
  return (
    <footer className="bg-muted/30 border-t border-border">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-8 md:px-10 lg:px-16 py-12 sm:py-16 md:py-20">
        {/* Content Section */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8 mb-12">
          {/* Logo and Company Info */}
          <div className="flex flex-col items-center lg:items-start">
            <h2 className="text-xl font-bold text-foreground">{companyName}</h2>
          </div>

          {/* Links */}
          <nav className="flex flex-col sm:flex-row gap-4 sm:gap-8 items-center">
            {links.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-foreground hover:text-primary transition-colors whitespace-nowrap"
              >
                {link.label}
              </a>
            ))}
          </nav>

          {/* Button */}
          <Button variant="default" size="sm">
            Explore tools
          </Button>
        </div>

        {/* Divider */}
        <div className="h-px bg-border mb-8" />

        {/* Copyright */}
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            © {year} {companyName}
          </p>
        </div>
      </div>
    </footer>
  )
}
