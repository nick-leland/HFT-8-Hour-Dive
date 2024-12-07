import pygame
import sys
import time
from typing import List
import argparse

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self, screen, font):
        color = (min(self.color[0] + 30, 255), 
                min(self.color[1] + 30, 255), 
                min(self.color[2] + 30, 255)) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class MarketVisualizer:
    def __init__(self, data: List[float], width=800, height=600, tick_interval=0.1):
        pygame.init()
        self.width = width
        self.height = height
        self.data = data
        self.current_idx = 0
        self.tick_interval = tick_interval
        self.window_size = 200  # Number of points to display
        
        # Portfolio tracking
        self.cash = 10000.0
        self.shares = 0
        
        # Calculate min/max for scaling
        self.min_value = min(data)
        self.max_value = max(data)
        
        # Setup display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Market Visualizer")
        
        # Setup fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.bg_color = (0, 0, 0)  # Black background
        self.text_color = (200, 200, 200)  # Light grey text
        self.up_color = (0, 255, 0)  # Green
        self.down_color = (255, 0, 0)  # Red
        
        # Line properties
        self.line_thickness = 2
        
        # Setup buttons
        self.setup_buttons()
        
    def setup_buttons(self):
        button_width = 100
        button_height = 30
        button_margin = 10
        start_y = 100
        
        self.buttons = [
            Button(20, start_y, button_width, button_height, "Buy 1", (0, 100, 0)),
            Button(20, start_y + button_height + button_margin, button_width, button_height, "Buy 10", (0, 100, 0)),
            Button(20, start_y + (button_height + button_margin) * 2, button_width, button_height, "Buy 100", (0, 100, 0)),
            Button(130, start_y, button_width, button_height, "Sell 1", (100, 0, 0)),
            Button(130, start_y + button_height + button_margin, button_width, button_height, "Sell 10", (100, 0, 0)),
            Button(130, start_y + (button_height + button_margin) * 2, button_width, button_height, "Sell 100", (100, 0, 0))
        ]
    
    def handle_trade(self, amount: int, is_buy: bool):
        current_price = self.data[self.current_idx - 1] if self.current_idx > 0 else self.data[0]
        
        if is_buy:
            total_cost = current_price * amount
            if total_cost <= self.cash:
                self.cash -= total_cost
                self.shares += amount
        else:
            if amount <= self.shares:
                total_value = current_price * amount
                self.cash += total_value
                self.shares -= amount
    
    def normalize_to_height(self, value: float) -> float:
        """Convert a value to screen coordinates"""
        margin = self.height * 0.2  # 20% margin top and bottom
        usable_height = self.height - 2 * margin
        normalized = ((value - self.min_value) / (self.max_value - self.min_value))
        return self.height - (margin + normalized * usable_height)
    
    def draw_info(self, current_value: float):
        """Draw information text"""
        # Draw portfolio value
        portfolio_value = self.cash + (self.shares * current_value)
        value_text = f"Cash: ${self.cash:.2f}"
        shares_text = f"Shares: {self.shares}"
        portfolio_text = f"Total Value: ${portfolio_value:.2f}"
        
        text_surface = self.font.render(value_text, True, self.text_color)
        self.screen.blit(text_surface, (20, 20))
        
        shares_surface = self.font.render(shares_text, True, self.text_color)
        self.screen.blit(shares_surface, (400, 20))
        
        portfolio_surface = self.font.render(portfolio_text, True, self.text_color)
        self.screen.blit(portfolio_surface, (20, 60))
        
        # Draw current price
        price_text = f"Current Price: ${current_value:.2f}"
        price_surface = self.small_font.render(price_text, True, self.text_color)
        self.screen.blit(price_surface, (400, 60))
        
        # Draw controls
        controls_text = "Controls: Q to quit, +/- to adjust speed"
        controls_surface = self.small_font.render(controls_text, True, self.text_color)
        self.screen.blit(controls_surface, (20, self.height - 30))
    
    def draw_chart(self, visible_data: List[float]):
        """Draw the line chart"""
        if len(visible_data) < 2:
            return
            
        points = []
        for i, value in enumerate(visible_data):
            x = int((i / len(visible_data)) * self.width)
            y = self.normalize_to_height(value)
            points.append((x, y))
            
        # Draw lines between points
        for i in range(len(points) - 1):
            start_pos = points[i]
            end_pos = points[i + 1]
            
            # Determine color based on price movement
            color = self.up_color if visible_data[i+1] >= visible_data[i] else self.down_color
            
            # Draw line
            pygame.draw.line(self.screen, color, start_pos, end_pos, self.line_thickness)
    
    def run(self):
        running = True
        last_update = time.time()
        
        while running and self.current_idx < len(self.data):
            current_time = time.time()
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.tick_interval = max(0.01, self.tick_interval - 0.01)
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.tick_interval = min(1.0, self.tick_interval + 0.01)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.rect.collidepoint(event.pos):
                            amount = 1 if i % 3 == 0 else (10 if i % 3 == 1 else 100)
                            is_buy = i < 3
                            self.handle_trade(amount, is_buy)
            
            # Update button hover states
            for button in self.buttons:
                button.hover = button.rect.collidepoint(mouse_pos)
            
            # Update visualization
            if current_time - last_update >= self.tick_interval:
                # Clear screen
                self.screen.fill(self.bg_color)
                
                # Get visible data window
                start_idx = max(0, self.current_idx - self.window_size)
                end_idx = self.current_idx
                visible_data = self.data[start_idx:end_idx]
                
                # Draw components
                self.draw_chart(visible_data)
                current_value = self.data[self.current_idx - 1] if self.current_idx > 0 else self.data[0]
                self.draw_info(current_value)
                
                # Draw buttons
                for button in self.buttons:
                    button.draw(self.screen, self.small_font)
                
                # Update display
                pygame.display.flip()
                
                self.current_idx += 1
                last_update = current_time
                
            # Small delay to prevent maxing out CPU
            pygame.time.wait(1)
        
        pygame.quit()

def main():
    parser = argparse.ArgumentParser(description='PyGame Market Data Visualizer')
    parser.add_argument('--tick-interval', type=float, default=0.1,
                      help='Time between updates (seconds)')
    parser.add_argument('--width', type=int, default=800,
                      help='Window width')
    parser.add_argument('--height', type=int, default=600,
                      help='Window height')
    args = parser.parse_args()
    
    # Read data from stdin (one value per line)
    data = [float(line.strip()) for line in sys.stdin]
    
    visualizer = MarketVisualizer(data, args.width, args.height, args.tick_interval)
    visualizer.run()

if __name__ == "__main__":
    main()
