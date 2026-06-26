import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import MainLayout from './components/layout/MainLayout';
import DashboardPage from './pages/dashboard/DashboardPage';
import InstituicoesPage from './pages/instituicoes/InstituicoesPage';
import ContasPage from './pages/contas/ContasPage';
import AtivosPage from './pages/ativos/AtivosPage';
import CarteirasPage from './pages/carteiras/CarteirasPage';
import MovimentacoesPage from './pages/movimentacoes/MovimentacoesPage';
import PosicoesPage from './pages/posicoes/PosicoesPage';
import AportesPage from './pages/aportes/AportesPage';
import ProventosPage from './pages/proventos/ProventosPage';
import EventosCorporativosPage from './pages/eventos-corporativos/EventosCorporativosPage';
import RadarDividendosPage from './pages/radar-dividendos/RadarDividendosPage';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="instituicoes" element={<InstituicoesPage />} />
            <Route path="contas" element={<ContasPage />} />
            <Route path="ativos" element={<AtivosPage />} />
            <Route path="carteiras" element={<CarteirasPage />} />
            <Route path="movimentacoes" element={<MovimentacoesPage />} />
            <Route path="posicoes" element={<PosicoesPage />} />
            <Route path="aportes" element={<AportesPage />} />
            <Route path="proventos" element={<ProventosPage />} />
            <Route path="eventos-corporativos" element={<EventosCorporativosPage />} />
            <Route path="radar-dividendos" element={<RadarDividendosPage />} />
          </Route>
        </Routes>
      </Router>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;