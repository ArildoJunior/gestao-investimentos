import { Link } from 'react-router-dom';
import { Home, Landmark, Wallet, PiggyBank, TrendingUp, DollarSign, Calendar, BarChart, Package2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarProps {
  className?: string;
  onLinkClick?: () => void;
}

const Sidebar = ({ className, onLinkClick }: SidebarProps) => {
  const navItems = [
    { name: 'Dashboard', icon: Home, path: '/' },
    { name: 'Instituições', icon: Landmark, path: '/instituicoes' },
    { name: 'Contas', icon: Wallet, path: '/contas' },
    { name: 'Carteiras', icon: PiggyBank, path: '/carteiras' },
    { name: 'Ativos', icon: TrendingUp, path: '/ativos' },
    { name: 'Movimentações', icon: DollarSign, path: '/movimentacoes' },
    { name: 'Posições', icon: BarChart, path: '/posicoes' },
    { name: 'Aportes', icon: Package2, path: '/aportes' },
    { name: 'Proventos', icon: Calendar, path: '/proventos' },
    { name: 'Eventos Corporativos', icon: Calendar, path: '/eventos-corporativos' },
    { name: 'Radar de Dividendos', icon: Calendar, path: '/radar-dividendos' },
  ];

  return (
    <div className={cn("flex h-full max-h-screen flex-col gap-2", className)}>
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
        <Link to="/" className="flex items-center gap-2 font-semibold" onClick={onLinkClick}>
          <Package2 className="h-6 w-6" />
          <span>Investimentos</span>
        </Link>
      </div>
      <div className="flex-1">
        <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
          {navItems.map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
              onClick={onLinkClick}
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;