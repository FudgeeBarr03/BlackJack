import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlackJack")


pygame.font.init()
def get_font(size):
    return pygame.font.Font(None, size)

title_img = pygame.image.load("Assets/Buttons/Title.png").convert_alpha()
start_img = pygame.image.load("Assets/Buttons/Start_btn.png").convert_alpha()
exit_img = pygame.image.load("Assets/Buttons/Exit_btn.png").convert_alpha()
hit_img = pygame.image.load("Assets/Buttons/Hit.png").convert_alpha()
stand_img = pygame.image.load("Assets/Buttons/Stand.png").convert_alpha()
retry_img = pygame.image.load("Assets/Buttons/Retry.png").convert_alpha()

class Button:
    def __init__(self, x, y, image, scale):
        width, height = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

card_files =[f"Assets/Cards/Clubs {i}.png" for i in range(1, 14)] + \
            [f"Assets/Cards/Diamonds {i}.png" for i in range(1, 14)] + \
            [f"Assets/Cards/Hearts {i}.png" for i in range(1, 14)] + \
            [f"Assets/Cards/Spades {i}.png" for i in range(1, 14)]

CARD_WIDTH = 128
CARD_HEIGHT = 192

full_deck = []
for file in card_files:
    image = pygame.image.load(file).convert_alpha()
    image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
    
    rank = int(file.split()[1].split('.')[0])
    
    if rank == 1:  
        value = 11
    elif rank >= 11:  
        value = 10
    else:
        value = rank

    full_deck.append({"image": image, "value": value})

def reshuffle_deck():
    global full_deck
    screen.fill((0, 128, 0))
    reshuffle_text = get_font(60).render("Reshuffling Deck...", True, "White")
    screen.blit(reshuffle_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 30))
    pygame.display.update()
    pygame.time.delay(1500)

    full_deck = []
    for file in card_files:
        image = pygame.image.load(file).convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        value = min(10, int(file.split()[1].split('.')[0]))
        if "1.png" in file:
            value = 11
        full_deck.append({"image": image, "value": value})

def deal_card(turn):
    if not full_deck:
        reshuffle_deck()
    
    card = random.choice(full_deck)
    turn.append(card)
    full_deck.remove(card)

def total(turn):
    total_value = sum(card["value"] for card in turn)
    aces = sum(1 for card in turn if card["value"] == 11)
    while total_value > 21 and aces:
        total_value -= 10
        aces -= 1
    return total_value

player_hand, dealer_hand = [], []
player_in, dealer_in = True, True
game_over = False

face_down_card = pygame.image.load("Assets/Cards/Card Back 3.png").convert_alpha()
face_down_card = pygame.transform.scale(face_down_card, (CARD_WIDTH, CARD_HEIGHT))

start_button = Button(320, 500, start_img, 1)
exit_button = Button(670, 500, exit_img, 1)
hit_button = Button(300, 600, hit_img, .6)
stand_button = Button(600, 600, stand_img, .6)
retry_button = Button(220, 250, retry_img, .6)
title_img = Button(300, 120, title_img, 3)

def main_menu():
    global player_hand, dealer_hand, player_in, dealer_in
    running = True
    while running:
        screen.fill((202, 228, 241))
        title_img.draw(screen)
        if start_button.draw(screen):
            play_game()
        elif exit_button.draw(screen):
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
    pygame.quit()


def play_game():
    global player_hand, dealer_hand, player_in, dealer_in, game_over
    player_hand, dealer_hand = [], []
    player_in, dealer_in, game_over = True, True, False
    
    for _ in range(2):
        deal_card(player_hand)
        deal_card(dealer_hand)
    
    running = True
    while running:
        screen.fill((0, 128, 0))
        screen.blit(dealer_hand[0]["image"], (200, 30))
        screen.blit(face_down_card, (300, 30))
        
        for i, card in enumerate(player_hand):
            screen.blit(card["image"], (200 + (i * 100), 380))
        
        player_score_text = get_font(45).render(f"Your total: {total(player_hand)}", True, "White")
        screen.blit(player_score_text, (450, 550))
        
        if player_in and not game_over:
            if hit_button.draw(screen):
                deal_card(player_hand)
                if total(player_hand) >= 21:
                    player_in = False
                    game_over = True
            if stand_button.draw(screen):
                player_in = False
                game_over = True
        
        
        if not player_in and dealer_in:
            while total(dealer_hand) < 17:
                deal_card(dealer_hand)
            dealer_in = False
            game_over = True
        
        if game_over:
            dealer_score_text = get_font(45).render(f"Dealer's total: {total(dealer_hand)}", True, "White")
            screen.blit(dealer_score_text, (450, 200))
            
            for i, card in enumerate(dealer_hand):
                screen.blit(card["image"], (200 + (i * 100), 30))
                
            result_text = get_font(45).render(check_winner(), True, "White")
            screen.blit(result_text, (450, 280))
            
            if retry_button.draw(screen):
                play_game()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
        pygame.display.update()


def check_winner():
    player_total = total(player_hand)
    dealer_total = total(dealer_hand)
    if player_total > 21:
        return "Dealer Wins!"
    elif dealer_total > 21 or player_total > dealer_total:
        return "You Win!"
    elif dealer_total > player_total:
        return "Dealer Wins!"
    else:
        return "It's a Tie!"
    
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
        break

main_menu()
