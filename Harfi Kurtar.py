"""
Calc & Hang — İşlem Yap, Harfi Kurtar
Kocaeli Sağlık ve Teknoloji Üniversitesi
Programlama Lab I - Proje 1
Geliştirilmiş Görsel Tasarım Versiyonu
"""

import random
import json
import os
from datetime import datetime

# Terminal renk kodları
class Colors:
    """Terminal renklendirme sınıfı"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[35m'
    WHITE = '\033[97m'

# Kelime kategorileri
WORD_CATEGORIES = {
    'meyve': ['elma', 'armut', 'muz', 'kiraz', 'üzüm', 'portakal', 'kavun', 'karpuz', 'çilek', 'mandalina'],
    'hayvan': ['aslan', 'kaplan', 'fil', 'zürafa', 'kanguru', 'köpek', 'kedi', 'tavşan', 'kuş', 'balık'],
    'teknoloji': ['bilgisayar', 'telefon', 'tablet', 'klavye', 'fare', 'monitör', 'yazıcı', 'tarayıcı', 'kamera', 'robot']
}

# Yeni ve farklı asmaca görselleri - daha detaylı
HANGMAN_STAGES = [
    """
    ╔═══════╗
    ║       ║
    ║       
    ║       
    ║       
    ║       
    ╚═══════╝
    """,
    """
    ╔═══════╗
    ║       ║
    ║      😐
    ║       
    ║       
    ║       
    ╚═══════╝
    """,
    """
    ╔═══════╗
    ║       ║
    ║      😟
    ║       │
    ║       
    ║       
    ╚═══════╝
    """,
    """
    ╔═══════╗
    ║       ║
    ║      😨
    ║      ─│
    ║       
    ║       
    ╚═══════╝
    """,
    """
    ╔═══════╗
    ║       ║
    ║      😰
    ║      ─│─
    ║       
    ║       
    ╚═══════╝
    """,
    """
    ╔═══════╗
    ║       ║
    ║      😱
    ║      ─│─
    ║      ╱
    ║       
    ╚═══════╝
    """,
    """
    ╔═══════╗
    ║       ║
    ║      💀
    ║      ─│─
    ║      ╱ ╲
    ║       
    ╚═══════╝
    """
]

class CalcHangGame:
    """Calc & Hang oyun sınıfı"""
    
    def __init__(self):
        """Oyun başlangıç ayarları"""
        self.max_errors = 6
        self.reset_game()
    
    def reset_game(self):
        """Oyun değişkenlerini sıfırla"""
        # Rastgele kategori ve kelime seç
        self.category = random.choice(list(WORD_CATEGORIES.keys()))
        self.word = random.choice(WORD_CATEGORIES[self.category]).upper()
        
        # Oyun durumu
        self.guessed_letters = set()
        self.error_count = 0
        self.bonus_points = 0
        self.score = 0
        self.hint_used = False
        
        # Kullanılan işlemler
        self.used_operations = {
            'toplama': False,
            'çıkarma': False,
            'çarpma': False,
            'bölme': False
        }
        
        # Maskelenmiş kelime
        self.masked_word = ['_'] * len(self.word)
    
    def display_game_state(self):
        """Oyun durumunu ekrana yazdır - YENİ TASARIM"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Farklı başlık tasarımı
        print(f"{Colors.PURPLE}{Colors.BOLD}")
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  🎮 CALC & HANG - İŞLEM YAP, HARFİ KURTAR 🎮  ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print(f"{Colors.END}\n")
        
        # Asmaca görseli - renkli
        print(f"{Colors.FAIL}{Colors.BOLD}{HANGMAN_STAGES[self.error_count]}{Colors.END}")
        
        # Kelime gösterimi - kutucuklar içinde
        print(f"\n{Colors.CYAN}┌{'─' * (len(self.word) * 4 + 1)}┐{Colors.END}")
        kelime_gosterim = "│ " + " │ ".join([f"{Colors.BOLD}{letter}{Colors.END}" if letter != '_' else f"{Colors.WARNING}__{Colors.END}" for letter in self.masked_word]) + " │"
        print(f"{Colors.CYAN}{kelime_gosterim}{Colors.END}")
        print(f"{Colors.CYAN}└{'─' * (len(self.word) * 4 + 1)}┘{Colors.END}\n")
        
        # Tahmin edilen harfler - renkli kutular
        if self.guessed_letters:
            print(f"{Colors.BLUE}┌─ Denenen Harfler {'─' * 30}┐{Colors.END}")
            harf_str = " ".join([f"[{h}]" for h in sorted(self.guessed_letters)])
            print(f"{Colors.BLUE}│ {Colors.WHITE}{harf_str}{Colors.END}")
            print(f"{Colors.BLUE}└{'─' * 47}┘{Colors.END}\n")
        else:
            print(f"{Colors.BLUE}└─ Henüz harf denenmedi{Colors.END}\n")
        
        # Durum bilgileri - progress bar tarzı
        can_bar = "█" * (self.max_errors - self.error_count) + "░" * self.error_count
        print(f"{Colors.WARNING}❤️  Can     : [{can_bar}] {self.max_errors - self.error_count}/{self.max_errors}{Colors.END}")
        
        bonus_bar = "★" * self.bonus_points + "☆" * (5 - min(self.bonus_points, 5))
        print(f"{Colors.GREEN}⭐ Bonus   : [{bonus_bar}] {self.bonus_points}{Colors.END}")
        
        print(f"{Colors.CYAN}🏆 Puan    : {Colors.BOLD}{self.score}{Colors.END} puan")
        
        # İşlem durumu - ikon tabanlı
        print(f"\n{Colors.HEADER}╔══ MATEMATİK İŞLEMLER ═══════════════════════╗{Colors.END}")
        islem_ikons = {
            'toplama': '➕', 
            'çıkarma': '➖', 
            'çarpma': '✖️', 
            'bölme': '➗'
        }
        
        for op, used in self.used_operations.items():
            ikon = islem_ikons.get(op, '•')
            if used:
                status = f"{Colors.FAIL}[✗ KULLANILDI]{Colors.END}"
            else:
                status = f"{Colors.GREEN}[✓ MÜSAİT]   {Colors.END}"
            print(f"{Colors.HEADER}║{Colors.END} {ikon}  {op.capitalize():<12} {status}")
        
        print(f"{Colors.HEADER}╚════════════════════════════════════════════════╝{Colors.END}\n")
    
    def guess_letter(self, letter):
        """Harf tahmini yap"""
        letter = letter.upper()
        
        # Harf kontrolü
        if len(letter) != 1:
            return False, f"{Colors.FAIL}⚠️  Sadece TEK harf girebilirsiniz!{Colors.END}"
        
        if not letter.isalpha():
            return False, f"{Colors.FAIL}⚠️  Lütfen geçerli bir HARF girin!{Colors.END}"
        
        if letter in self.guessed_letters:
            return False, f"{Colors.WARNING}⚠️  '{letter}' harfini daha önce denediniz!{Colors.END}"
        
        # Harfi kaydet
        self.guessed_letters.add(letter)
        
        # Harf kelimede var mı?
        if letter in self.word:
            # Harfi aç
            for i, char in enumerate(self.word):
                if char == letter:
                    self.masked_word[i] = letter
            self.score += 10
            return True, f"{Colors.GREEN}{Colors.BOLD}✓ SÜPER! '{letter}' harfi doğru! (+10 puan){Colors.END}"
        else:
            self.error_count += 1
            self.score -= 5
            return False, f"{Colors.FAIL}{Colors.BOLD}✗ YANLIŞ! '{letter}' kelimede yok. (-5 puan){Colors.END}"
    
    def calculate(self):
        """Hesap makinesi fonksiyonu - YENİ GÖRÜNÜM"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════╗")
        print("║           🧮 HESAP MAKİNESİ 🧮               ║")
        print("╚═══════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        # Kullanılabilir işlemleri göster
        available_ops = [op for op, used in self.used_operations.items() if not used]
        
        if not available_ops:
            print(f"{Colors.FAIL}❌ Tüm işlemler tükendi!{Colors.END}")
            input(f"\n{Colors.WARNING}⏎ Devam için ENTER'a basın...{Colors.END}")
            return
        
        print(f"{Colors.GREEN}Kullanılabilir İşlemler:{Colors.END}")
        islem_sembolleri = {'toplama': '➕', 'çıkarma': '➖', 'çarpma': '✖️', 'bölme': '➗'}
        
        for i, op in enumerate(available_ops, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.END} {islem_sembolleri.get(op, '•')}  {op.capitalize()}")
        print(f"  {Colors.BOLD}[0]{Colors.END} ❌ Vazgeç")
        
        # İşlem seçimi
        try:
            choice = input(f"\n{Colors.CYAN}➤ Seçiminiz (0-{len(available_ops)}):{Colors.END} ").strip()
            
            if choice == '0' or choice.lower() == 'iptal':
                print(f"{Colors.WARNING}↩️  İşlem iptal edildi.{Colors.END}")
                input(f"\n{Colors.WARNING}⏎ ENTER...{Colors.END}")
                return
            
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(available_ops):
                print(f"{Colors.FAIL}❌ Geçersiz seçim!{Colors.END}")
                input(f"\n{Colors.WARNING}⏎ ENTER...{Colors.END}")
                return
            
            operation = available_ops[choice_idx]
            
            # Sayıları al - farklı gösterim
            print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
            num1 = float(input(f"{Colors.BLUE}📥 1. Sayı → {Colors.END}"))
            num2 = float(input(f"{Colors.BLUE}📥 2. Sayı → {Colors.END}"))
            
            # İşlemi yap
            if operation == 'toplama':
                correct_result = num1 + num2
                op_symbol = '+'
            elif operation == 'çıkarma':
                correct_result = num1 - num2
                op_symbol = '-'
            elif operation == 'çarpma':
                correct_result = num1 * num2
                op_symbol = '×'
            elif operation == 'bölme':
                if num2 == 0:
                    print(f"{Colors.FAIL}💥 HATA: Sıfıra bölünemez!{Colors.END}")
                    self.error_count += 1
                    self.score -= 10
                    input(f"\n{Colors.WARNING}⏎ ENTER...{Colors.END}")
                    return
                correct_result = num1 / num2
                op_symbol = '÷'
            
            # Kullanıcının cevabını al
            print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
            user_answer = float(input(f"{Colors.PURPLE}❓ {num1} {op_symbol} {num2} = {Colors.END}"))
            
            # Cevabı kontrol et
            if abs(user_answer - correct_result) <= 1e-6:
                print(f"\n{Colors.GREEN}{Colors.BOLD}{'🎉' * 25}")
                print(f"   ✓✓✓ DOĞRU CEVAP! ✓✓✓")
                print(f"{'🎉' * 25}{Colors.END}")
                
                self.bonus_points += 1
                self.score += 15
                self.used_operations[operation] = True
                
                # Rastgele bir harf aç
                unopened_indices = [i for i, char in enumerate(self.masked_word) if char == '_']
                if unopened_indices:
                    random_idx = random.choice(unopened_indices)
                    self.masked_word[random_idx] = self.word[random_idx]
                    print(f"{Colors.GREEN}🎁 BONUS HARF: '{self.word[random_idx]}' açıldı!{Colors.END}")
                
                print(f"{Colors.GREEN}💰 +15 puan | ⭐ +1 bonus{Colors.END}")
            else:
                print(f"\n{Colors.FAIL}{Colors.BOLD}{'❌' * 25}")
                print(f"   ✗ YANLIŞ CEVAP ✗")
                print(f"{'❌' * 25}{Colors.END}")
                print(f"{Colors.CYAN}Doğru cevap: {Colors.BOLD}{correct_result:.2f}{Colors.END}")
                print(f"{Colors.FAIL}💔 -10 puan | ❤️ -1 can{Colors.END}")
                self.error_count += 1
                self.score -= 10
            
        except ValueError:
            print(f"{Colors.FAIL}❌ Geçersiz sayı girdiniz!{Colors.END}")
        except Exception as e:
            print(f"{Colors.FAIL}💥 Hata: {e}{Colors.END}")
        
        input(f"\n{Colors.WARNING}⏎ Devam için ENTER...{Colors.END}")
    
    def get_hint(self):
        """İpucu al"""
        if self.hint_used:
            print(f"{Colors.WARNING}⚠️  İpucu zaten kullanıldı!{Colors.END}")
            return False
        
        if self.bonus_points < 1:
            print(f"{Colors.FAIL}❌ Yetersiz bonus! (Gerekli: ⭐ 1 bonus){Colors.END}")
            return False
        
        self.bonus_points -= 1
        self.hint_used = True
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════╗")
        print(f"║         💡 İPUCU: {self.category.upper():<28} ║")
        print("╚═══════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        return True
    
    def is_won(self):
        """Oyun kazanıldı mı?"""
        return '_' not in self.masked_word
    
    def is_lost(self):
        """Oyun kaybedildi mi?"""
        return self.error_count >= self.max_errors
    
    def save_score(self, player_name):
        """Skoru kaydet"""
        score_data = {
            'player': player_name,
            'score': self.score,
            'word': self.word,
            'category': self.category,
            'date': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        }
        
        # Mevcut skorları oku
        scores = []
        if os.path.exists('scores.json'):
            try:
                with open('scores.json', 'r', encoding='utf-8') as f:
                    scores = json.load(f)
            except:
                scores = []
        
        # Yeni skoru ekle
        scores.append(score_data)
        
        # Skorları sırala
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:5]
        
        # Kaydet
        with open('scores.json', 'w', encoding='utf-8') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        
        return scores
    
    def display_scores(self, scores):
        """Skorları göster - YENİ TASARIM"""
        print(f"\n{Colors.PURPLE}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════╗")
        print("║           🏆 EN YÜKSEK 5 SKOR 🏆             ║")
        print("╚═══════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        medals = ['🥇', '🥈', '🥉', '🏅', '🏅']
        
        for i, score in enumerate(scores):
            medal = medals[i] if i < len(medals) else '🏅'
            print(f"{medal} {Colors.CYAN}{Colors.BOLD}{score['player']:<15}{Colors.END} │ "
                  f"{Colors.GREEN}{score['score']:>4} puan{Colors.END} │ "
                  f"{Colors.BLUE}{score['word']:<12}{Colors.END} │ "
                  f"{Colors.WARNING}{score['date']}{Colors.END}")
        
        print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")

def main():
    """Ana oyun döngüsü"""
    game = CalcHangGame()
    
    # Hoşgeldin ekranı - farklı tasarım
    print(f"{Colors.PURPLE}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════╗")
    print("║                                               ║")
    print("║     🎮 CALC & HANG - OYUNA HOŞGELDİN 🎮      ║")
    print("║                                               ║")
    print("║         İşlem Yap, Harfi Kurtar!             ║")
    print("║                                               ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    player_name = input(f"{Colors.CYAN}👤 Kullanıcı adınız → {Colors.END}").strip()
    if not player_name:
        player_name = "Anonim"
    
    print(f"\n{Colors.GREEN}Merhaba {Colors.BOLD}{player_name}{Colors.END}{Colors.GREEN}! 👋{Colors.END}")
    input(f"{Colors.WARNING}\n⏎ Başlamak için ENTER'a basın...{Colors.END}")
    
    # Ana oyun döngüsü
    while True:
        game.display_game_state()
        
        # Kazanma/kaybetme kontrolü
        if game.is_won():
            print(f"\n{Colors.GREEN}{Colors.BOLD}")
            print("╔═══════════════════════════════════════════════╗")
            print("║          🎉🎉🎉 KAZANDINIZ! 🎉🎉🎉           ║")
            print("╚═══════════════════════════════════════════════╝")
            print(f"{Colors.END}")
            print(f"{Colors.CYAN}✓ Kelime: {Colors.BOLD}{game.word}{Colors.END}")
            game.score += 50
            break
        
        if game.is_lost():
            print(f"\n{Colors.FAIL}{Colors.BOLD}")
            print("╔═══════════════════════════════════════════════╗")
            print("║           💀 KAYBETTİNİZ! 💀                  ║")
            print("╚═══════════════════════════════════════════════╝")
            print(f"{Colors.END}")
            print(f"{Colors.CYAN}✗ Doğru kelime: {Colors.BOLD}{game.word}{Colors.END}")
            game.score -= 20
            break
        
        # Menü - box tasarımı
        print(f"{Colors.HEADER}┌─── MENÜ ────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.HEADER}│{Colors.END} {Colors.GREEN}[1]{Colors.END} 🔤 Harf Tahmin Et                     {Colors.HEADER}│{Colors.END}")
        print(f"{Colors.HEADER}│{Colors.END} {Colors.GREEN}[2]{Colors.END} 🧮 Matematiksel İşlem Yap             {Colors.HEADER}│{Colors.END}")
        print(f"{Colors.HEADER}│{Colors.END} {Colors.GREEN}[3]{Colors.END} 💡 İpucu Al (1 bonus)                 {Colors.HEADER}│{Colors.END}")
        print(f"{Colors.HEADER}│{Colors.END} {Colors.GREEN}[Q]{Colors.END} 🚪 Çıkış                              {Colors.HEADER}│{Colors.END}")
        print(f"{Colors.HEADER}└─────────────────────────────────────────────┘{Colors.END}")
        
        choice = input(f"\n{Colors.CYAN}➤ Seçim yapın:{Colors.END} ").strip().lower()
        
        if choice == '1':
            letter = input(f"{Colors.BLUE}🔤 Harf girin → {Colors.END}").strip()
            success, message = game.guess_letter(letter)
            print(f"\n{message}")
            input(f"\n{Colors.WARNING}⏎ ENTER...{Colors.END}")
            
        elif choice == '2':
            game.calculate()
            
        elif choice == '3':
            game.get_hint()
            input(f"\n{Colors.WARNING}⏎ ENTER...{Colors.END}")
            
        elif choice == '4' or choice == 'q':
            print(f"\n{Colors.WARNING}👋 Oyun sonlandırılıyor...{Colors.END}")
            break
        
        else:
            print(f"{Colors.FAIL}❌ Geçersiz seçim!{Colors.END}")
            input(f"\n{Colors.WARNING}⏎ ENTER...{Colors.END}")
    
    # Oyun sonu - farklı tasarım
    print(f"\n{Colors.PURPLE}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════╗")
    print("║              📊 OYUN İSTATİSTİKLERİ 📊       ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    print(f"  🏆 Toplam Skor    : {Colors.BOLD}{game.score}{Colors.END} puan")
    print(f"  ⭐ Bonus Puan     : {Colors.BOLD}{game.bonus_points}{Colors.END}")
    print(f"  💔 Yapılan Hata   : {Colors.BOLD}{game.error_count}/{game.max_errors}{Colors.END}")
    print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")
    
    # Skoru kaydet ve göster
    scores = game.save_score(player_name)
    game.display_scores(scores)
    
    # Tekrar oyna
    play_again = input(f"\n{Colors.CYAN}🔄 Tekrar oynamak ister misiniz? (e/h) → {Colors.END}").strip().lower()
    if play_again == 'e':
        game.reset_game()
        main()
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}👋 Görüşmek üzere! Teşekkürler! 🎮{Colors.END}\n")

if __name__ == "__main__":
    main()
