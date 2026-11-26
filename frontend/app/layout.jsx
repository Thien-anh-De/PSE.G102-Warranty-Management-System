import React from "react";
import "./globals.css";

export const metadata = {
  title: "Tra cứu bảo hành | Hưng Thiện",
  description:
    "Tra cứu tiến độ bảo hành thiết bị tại Trung tâm hỗ trợ kỹ thuật Hưng Thiện.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
