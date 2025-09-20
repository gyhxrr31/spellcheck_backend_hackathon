import { Bell, Search, ShoppingCart, Lightbulb, MapPin, User } from 'lucide-react';
import { Button } from './ui/button';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';

export function Header() {
  return (
    <header className="w-full bg-white border-b border-border">
      <div className="flex items-center justify-between px-6 py-3">
        {/* Left side - Logo */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-red-600 flex items-center justify-center rounded">
              <span className="text-white font-bold text-sm">П</span>
            </div>
            <div>
              <div className="font-medium text-sm">ПОРТАЛ</div>
              <div className="text-xs text-muted-foreground">ПОСТАВЩИКОВ</div>
            </div>
          </div>
          
          <Button variant="ghost" className="flex items-center gap-2 text-sm" onClick={() => console.log('Открыть меню')}>
            Меню
          </Button>
        </div>

        {/* Center - Navigation */}
        <div className="flex items-center gap-6">
          <Button variant="ghost" className="flex items-center gap-2 text-sm" onClick={() => console.log('Открыть центр поддержки')}>
            <Lightbulb className="w-4 h-4" />
            Центр поддержки
          </Button>
          
          <Button variant="ghost" className="flex items-center gap-2 text-sm" onClick={() => console.log('Открыть корзину')}>
            <ShoppingCart className="w-4 h-4" />
            Корзина
          </Button>
          
          <Button variant="ghost" className="flex items-center gap-2 text-sm" onClick={() => console.log('Выбрать регион')}>
            <MapPin className="w-4 h-4" />
            Московская область
          </Button>
        </div>

        {/* Right side - Search and User */}
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => console.log('Открыть поиск')}>
            <Search className="w-4 h-4" />
          </Button>
          
          <Button variant="ghost" size="icon" className="relative" onClick={() => console.log('Открыть уведомления')}>
            <Bell className="w-4 h-4" />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-600 rounded-full"></span>
          </Button>
          
          <div className="flex items-center gap-2">
            <div className="text-right">
              <div className="text-sm">Александр Семёнов</div>
              <div className="text-xs text-muted-foreground">ПО «Склады»</div>
            </div>
            <Avatar className="w-8 h-8">
              <AvatarImage src="/api/placeholder/32/32" />
              <AvatarFallback>АС</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>
    </header>
  );
}