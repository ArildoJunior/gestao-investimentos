// FILE: frontend/src/components/layout/MainLayout.tsx

import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sheet, SheetContent } from '@/components/ui/sheet'; // Importe Sheet e SheetContent
import Header from './Header'; // Importe o Header existente
import Sidebar from './Sidebar'; // Importe o Sidebar existente

const MainLayout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleLinkClick = () => {
    // Fecha a sidebar em telas pequenas ao clicar em um link
    if (window.innerWidth < 768) { // Tailwind's 'md' breakpoint is 768px
      setIsSidebarOpen(false);
    }
  };

  return (
    <div className="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
      {/* Sidebar para telas maiores */}
      <div className="hidden border-r bg-muted/40 md:block">
        <Sidebar onLinkClick={handleLinkClick} />
      </div>

      {/* Conteúdo principal */}
      <div className="flex flex-col">
        {/* Header com botão para abrir sidebar em telas menores */}
        <Header /> {/* O Header já contém a lógica do SheetTrigger para mobile */}

        <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6 overflow-auto">
          <Outlet />
        </main>
      </div>

      {/* Sheet para sidebar em telas menores (mobile) */}
      <Sheet open={isSidebarOpen} onOpenChange={setIsSidebarOpen}>
        <SheetContent side="left" className="flex flex-col">
          <Sidebar onLinkClick={handleLinkClick} />
        </SheetContent>
      </Sheet>
    </div>
  );
};

export default MainLayout;