import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { SmartSearch } from './components/SmartSearch';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />
      
      <main className="flex-1 flex items-center justify-center py-12">
        <SmartSearch />
      </main>
      
      <Footer />
    </div>
  );
}