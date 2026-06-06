import type { Metadata } from 'next';
import './globals.css';
import { AppNav } from '@/components/AppNav';

export const metadata: Metadata = {
  title: 'AMR Research System',
  description: 'Adaptive Mean Reversion — research workstation',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#010409] antialiased" style={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
        <AppNav />
        <div style={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column' }}>
          {children}
        </div>
      </body>
    </html>
  );
}
