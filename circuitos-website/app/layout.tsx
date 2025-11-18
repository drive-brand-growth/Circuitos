import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CircuitOS - The Operator's Weapon System | Command Revenue",
  description: "Built for VPs running deals at 2am. Show the truth gap in <2 minutes. Pipeline Truth Detector, Deal Defibrillator, Forecast Reality Check, Quota Kill Switch.",
  keywords: ["revenue operations", "sales analytics", "pipeline management", "forecast accuracy", "CRM truth layer", "operator tools"],
  authors: [{ name: "CircuitOS" }],
  openGraph: {
    title: "CircuitOS - Command Revenue. Eliminate Chaos.",
    description: "The Operator's Weapon System for VPs who need truth, not dashboards.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
