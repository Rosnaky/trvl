import { Geist, Geist_Mono, Open_Sans, Borel, Playwrite_US_Trad, Neonderthaw, Shrikhand } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const openSans = Open_Sans({
  variable: "--font-open-sans",
  subsets: ["latin"],
});

const borel = Borel({
  variable: "--font-borel",
  subsets: ["latin"],
  weight: "400",
});

const shrikhand = Shrikhand({
  variable: "--font-playwrite-us",
  subsets: ["latin"],
  weight: "400",
});

export const metadata = {
  title: "trvl",
  description: "Ready to go on a trip but don't know where to visit? Let trvl plan your trip for you!",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${openSans.variable} ${shrikhand.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
