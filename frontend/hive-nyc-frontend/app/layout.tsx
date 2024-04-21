import type { Metadata } from "next";
import Link from "next/link";
import Head from "next/head";
import { Inter, Merriweather, Playfair_Display } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });
const merriweather = Merriweather({ weight: "400", subsets: ["latin"] });
const playfairDisplay = Playfair_Display({ weight: "700", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "HiveNYC",
  description:
    "Explore and contribute to historical sites around New York City",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={merriweather.className}>
        <div className="min-h-screen flex flex-col">
          <main className="flex-grow">{children}</main>
          <footer className="bg-blue-500 text-white p-4 text-center">
            HiveNYC © 2024
          </footer>
        </div>
      </body>
    </html>
  );
}
