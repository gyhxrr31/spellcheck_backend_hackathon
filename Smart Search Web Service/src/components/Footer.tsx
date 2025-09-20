import { Headphones, HelpCircle, Facebook, Twitter, Instagram } from 'lucide-react';
import { Button } from './ui/button';

export function Footer() {
  return (
    <footer className="w-full bg-gray-100 border-t border-border">
      <div className="px-6 py-4">
        {/* Top section with links */}
        <div className="flex justify-between items-center mb-4">
          <div className="flex gap-8">
            <Button variant="ghost" className="text-sm p-0 h-auto" onClick={() => console.log('О портале')}>
              О портале
            </Button>
            <Button variant="ghost" className="text-sm p-0 h-auto" onClick={() => console.log('Поставщикам')}>
              Поставщикам
            </Button>
            <Button variant="ghost" className="text-sm p-0 h-auto" onClick={() => console.log('Новости')}>
              Новости
            </Button>
            <Button variant="ghost" className="text-sm p-0 h-auto" onClick={() => console.log('Контакты')}>
              Контакты
            </Button>
            <Button variant="ghost" className="text-sm p-0 h-auto" onClick={() => console.log('Карта сайта')}>
              Карта сайта
            </Button>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="ghost" className="flex items-center gap-2 text-sm" onClick={() => console.log('Служба качества')}>
              <Headphones className="w-4 h-4" />
              Служба качества
            </Button>
            <Button variant="ghost" className="flex items-center gap-2 text-sm" onClick={() => console.log('Написать в службу поддержки')}>
              <HelpCircle className="w-4 h-4" />
              Написать в службу поддержки
            </Button>
          </div>
        </div>
        
        {/* Bottom section */}
        <div className="flex justify-between items-center pt-4 border-t border-border">
          <div className="text-xs text-muted-foreground">
            <div>© 2017-2018 2.0.5</div>
            <div>Портал Поставщиков работает в соответствии с 44-ФЗ</div>
          </div>
          
          <div className="flex gap-2">
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 text-white" onClick={() => window.open('https://facebook.com', '_blank')}>
              <Facebook className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 text-white" onClick={() => window.open('https://twitter.com', '_blank')}>
              <Twitter className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 text-white" onClick={() => window.open('https://instagram.com', '_blank')}>
              <Instagram className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 text-white" onClick={() => window.open('https://vk.com', '_blank')}>
              <span className="text-xs">ВК</span>
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 text-white" onClick={() => window.open('https://youtube.com', '_blank')}>
              <span className="text-xs">YT</span>
            </Button>
          </div>
        </div>
      </div>
    </footer>
  );
}