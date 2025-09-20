import { useState } from 'react';
import { Search, History, Star, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

interface SearchResult {
  id: string;
  type: 'create' | 'search';
  title: string;
  description: string;
  amount?: string;
  category?: string;
  confidence: number;
}

interface SearchHistory {
  id: string;
  query: string;
  timestamp: string;
  rating?: number;
}

export function SmartSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  
  // Mock search history
  const searchHistory: SearchHistory[] = [
    { id: '1', query: 'Создай КС на 300 тыс. на канцелярию', timestamp: '10:30', rating: 5 },
    { id: '2', query: 'Найти контракты на мебель', timestamp: 'Вчера', rating: 4 },
    { id: '3', query: 'Котировочная сессия ноутбуки', timestamp: '2 дня назад' },
  ];

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setShowHistory(false);
    
    try {
      // API call to localhost backend
      const response = await fetch('http://localhost:8000/api/smart-search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setResults(data.results);
      } else {
        // Fallback to mock data if API is not available
        const mockResults: SearchResult[] = [
          {
            id: '1',
            type: 'create',
            title: 'Создать котировочную сессию',
            description: 'Канцелярские товары на сумму 300 000 руб.',
            amount: '300 000',
            category: 'Канцелярские товары',
            confidence: 95
          },
          {
            id: '2',
            type: 'search',
            title: 'Похожие контракты',
            description: 'Найдено 12 контрактов на канцелярские товары',
            confidence: 87
          }
        ];
        setResults(mockResults);
      }
    } catch (error) {
      console.error('Search API error:', error);
      // Show mock results on error
      const mockResults: SearchResult[] = [
        {
          id: '1',
          type: 'create',
          title: 'Создать котировочную сессию',
          description: 'Канцелярские товары на сумму 300 000 руб.',
          amount: '300 000',
          category: 'Канцелярские товары',
          confidence: 95
        }
      ];
      setResults(mockResults);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResultClick = async (result: SearchResult) => {
    if (result.type === 'create') {
      try {
        // API call to create form with pre-filled data
        const response = await fetch('http://localhost:8000/api/create-form', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            amount: result.amount,
            category: result.category,
            title: result.title
          }),
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log('Form created:', data);
          // Redirect to form page
          window.open(data.formUrl, '_blank');
        }
      } catch (error) {
        console.error('Create form error:', error);
      }
    } else {
      try {
        // API call to get search results
        const response = await fetch(`http://localhost:8000/api/search-results?query=${encodeURIComponent(query)}`);
        if (response.ok) {
          const data = await response.json();
          console.log('Search results:', data);
          // Navigate to search results page
        }
      } catch (error) {
        console.error('Search results error:', error);
      }
    }
  };

  const rateResult = async (resultId: string, rating: number) => {
    try {
      await fetch('http://localhost:8000/api/rate-result', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ resultId, rating }),
      });
      console.log(`Rated result ${resultId} with ${rating} stars`);
    } catch (error) {
      console.error('Rating error:', error);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4">
      {/* Main search interface */}
      <div className="text-center mb-8">
        <h1 className="mb-2">Умный поиск по закупкам</h1>
        <p className="text-muted-foreground mb-6">
          Введите запрос на естественном языке для поиска или создания закупок
        </p>
        
        <div className="relative mb-6">
          <div className="flex gap-3 max-w-3xl mx-auto">
            <div className="relative flex-1">
              <div className="absolute left-4 top-1/2 transform -translate-y-1/2 z-10">
                <Sparkles className="w-5 h-5 text-primary/60" />
              </div>
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder='Например: "Создай КС на 300 тыс. на канцелярию" или "Найти контракты на мебель"'
                className="pl-12 pr-4 py-4 text-base border-2 border-border/50 focus:border-primary/50 rounded-xl shadow-sm bg-white/80 backdrop-blur-sm transition-all duration-200 hover:shadow-md focus:shadow-lg"
                onFocus={() => setShowHistory(true)}
              />
            </div>
            <Button 
              onClick={handleSearch} 
              disabled={isLoading} 
              className="px-8 py-4 rounded-xl bg-red-600 hover:bg-red-700 text-white shadow-sm hover:shadow-md transition-all duration-200"
              size="lg"
            >
              <Search className="w-5 h-5 mr-2" />
              {isLoading ? 'Обрабатываю...' : 'Найти'}
            </Button>
          </div>
        </div>

        {/* Quick examples */}
        <div className="flex flex-wrap justify-center gap-3 mb-8">
          <Badge 
            variant="secondary" 
            className="cursor-pointer hover:bg-red-50 hover:text-red-700 hover:border-red-200 px-4 py-2 rounded-full transition-all duration-200"
            onClick={() => setQuery('Создай КС на 500 тыс. на ноутбуки')}
          >
            Создать КС на ноутбуки
          </Badge>
          <Badge 
            variant="secondary"
            className="cursor-pointer hover:bg-red-50 hover:text-red-700 hover:border-red-200 px-4 py-2 rounded-full transition-all duration-200"
            onClick={() => setQuery('Найти контракты на мебель')}
          >
            Поиск контрактов
          </Badge>
          <Badge 
            variant="secondary"
            className="cursor-pointer hover:bg-red-50 hover:text-red-700 hover:border-red-200 px-4 py-2 rounded-full transition-all duration-200"
            onClick={() => setQuery('Добавить ЭЦП в профиль')}
          >
            Управление профилем
          </Badge>
        </div>
      </div>

      {/* Search History */}
      {showHistory && searchHistory.length > 0 && (
        <Card className="mb-6 max-w-3xl mx-auto shadow-sm border-border/50">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-sm">
              <History className="w-4 h-4" />
              История поиска
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-2">
              {searchHistory.map((item) => (
                <div 
                  key={item.id}
                  className="flex items-center justify-between p-3 hover:bg-muted/50 rounded-lg cursor-pointer transition-colors duration-200"
                  onClick={() => {
                    setQuery(item.query);
                    setShowHistory(false);
                  }}
                >
                  <div className="flex-1">
                    <div className="text-sm">{item.query}</div>
                    <div className="text-xs text-muted-foreground">{item.timestamp}</div>
                  </div>
                  {item.rating && (
                    <div className="flex items-center gap-1">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-3 h-3 ${
                            i < item.rating! ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Search Results */}
      {results.length > 0 && (
        <div className="space-y-4 max-w-3xl mx-auto">
          <h2>Результаты поиска</h2>
          {results.map((result) => (
            <Card key={result.id} className="cursor-pointer hover:shadow-lg transition-all duration-200 border-border/50 hover:border-primary/20">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1" onClick={() => handleResultClick(result)}>
                    <div className="flex items-center gap-2 mb-3">
                      <Badge 
                        variant={result.type === 'create' ? 'default' : 'secondary'}
                        className={result.type === 'create' ? 'bg-red-600 hover:bg-red-700' : ''}
                      >
                        {result.type === 'create' ? 'Создание' : 'Поиск'}
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        Уверенность: {result.confidence}%
                      </span>
                    </div>
                    
                    <h3 className="mb-2">{result.title}</h3>
                    <p className="text-muted-foreground text-sm mb-3">{result.description}</p>
                    
                    {result.amount && result.category && (
                      <div className="flex gap-6 text-sm mb-3">
                        <span><strong>Сумма:</strong> {result.amount} руб.</span>
                        <span><strong>Категория:</strong> {result.category}</span>
                      </div>
                    )}
                    
                    <div className="flex items-center gap-2 mt-3 text-sm text-red-600 hover:text-red-700 transition-colors">
                      <span>
                        {result.type === 'create' ? 'Создать форму' : 'Показать результаты'}
                      </span>
                      <ArrowRight className="w-4 h-4" />
                    </div>
                  </div>
                  
                  <div className="flex gap-1 ml-6">
                    {[1, 2, 3, 4, 5].map((rating) => (
                      <Button
                        key={rating}
                        variant="ghost"
                        size="icon"
                        className="w-8 h-8 hover:bg-yellow-50"
                        onClick={(e) => {
                          e.stopPropagation();
                          rateResult(result.id, rating);
                        }}
                      >
                        <Star className="w-4 h-4 hover:fill-yellow-400 hover:text-yellow-400 transition-colors" />
                      </Button>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}