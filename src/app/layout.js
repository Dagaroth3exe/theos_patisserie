import "./globals.css";

export const metadata = {
  title: "Theo's Patisserie | Luxury Desserts in India",
  description:
    "A luxury patisserie experience with artisanal desserts, online ordering, and Theo's story of craftsmanship in India.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
