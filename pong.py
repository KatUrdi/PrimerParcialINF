import arcade

import random

# Dimensiones de la pantalla
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Dimensiones de las paletas
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 60

# Radio de la pelota
BALL_RADIUS = 10

# Clase para el juego
class PongGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Pong Game")

        self.colision = arcade.Sound("sounds/colision.mp3")
        self.background = arcade.Sound("sounds/background.mp3")
       

        self.ball_texture = arcade.load_texture("img/pelota.png")
        
        self.game_over = False
    
        
        self.player1_score = 0
        self.player2_score = 0

        arcade.load_font("fonts/PublicPixel-z84yD.ttf")

        self.custom_font = "Public Pixel"
        self.player1_paddle = arcade.SpriteSolidColor(PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
        self.player1_paddle.center_x = PADDLE_WIDTH // 2
        self.player1_paddle.center_y = height // 2
        
        self.player2_paddle = arcade.SpriteSolidColor(PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
        self.player2_paddle.center_x = width - PADDLE_WIDTH // 2
        self.player2_paddle.center_y = height // 2

        self.ball = arcade.Sprite()
        self.ball.texture = self.ball_texture
        self.ball.center_x = width // 2
        self.ball.center_y = height // 2

        self.p1_move_up = False
        self.p1_move_down = False
        self.p2_move_up = False
        self.p2_move_down = False
        
        
        self.ball_speed_x = 4
        self.ball_speed_y = 4

    

        self.background.play(loop=True)

   

    def on_draw(self):
        arcade.start_render()

        # Dibuja los puntajes y las paletas
        arcade.draw_text(
            f"Player 1: {self.player1_score}", 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 10,font_name=self.custom_font
        )
        arcade.draw_text(
            f"Player 2: {self.player2_score}", SCREEN_WIDTH - 160, SCREEN_HEIGHT - 40, arcade.color.WHITE, 10, font_name=self.custom_font
        )
        self.player1_paddle.draw()
        self.player2_paddle.draw()

        # Verificar si algún jugador ha ganado y mostrar el mensaje correspondiente
        if  self.player1_score >= 5:
            arcade.draw_text(
                "¡Ganaste, Jugador 1!",
                SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2,
                arcade.color.WHITE, 20, font_name=self.custom_font
            )
            self.game_over = True  # Juego terminado
        elif  self.player2_score >= 5:
            arcade.draw_text(
                "¡Ganaste, Jugador 2!",
                SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2,
                arcade.color.WHITE, 20, font_name=self.custom_font
            )
            self.game_over = True  # Juego terminado

        if not self.game_over:  # Dibuja la pelota solo si el juego no ha terminado
            self.ball.draw()



        if self.game_over:
            arcade.draw_text(
                "Presiona R para reiniciar",
                SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 40,
                arcade.color.WHITE, 16
            )
       
    def update(self, delta_time):
        if self.game_over:
            return 
        self.ball.center_x += self.ball_speed_x
        self.ball.center_y += self.ball_speed_y
        
        # Colisiones con los bordes
        if self.ball.center_x - BALL_RADIUS <= 0 or self.ball.center_x + BALL_RADIUS >= SCREEN_WIDTH:
            self.ball_speed_x *= -1
        
        if self.ball.center_y - BALL_RADIUS <= 0 or self.ball.center_y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.ball_speed_y *= -1
        
        # Colisiones con las paletas
        if (
            self.ball.collides_with_sprite(self.player1_paddle)
            or self.ball.collides_with_sprite(self.player2_paddle)
        ):
            self.ball_speed_x *= -1
           
        
        # Puntuación
        if self.ball.center_x - BALL_RADIUS <= 0:
            self.player2_score += 1
            self.reset_ball()
        elif self.ball.center_x + BALL_RADIUS >= SCREEN_WIDTH:
            self.player1_score += 1
            self.reset_ball()

      
        
       
    def reset_ball(self):
        self.ball.center_x = SCREEN_WIDTH // 2
        self.ball.center_y = SCREEN_HEIGHT // 2
        self.ball_speed_x = 5
        self.ball_speed_y = 5

    def on_key_press(self, key, modifiers):
    # Movimiento de las paletas

        if key == arcade.key.W:
            self.p1_move_up = True
        elif key == arcade.key.S:
            self.p1_move_down = True
        elif key == arcade.key.UP:
            self.p2_move_up = True
        elif key == arcade.key.DOWN:
            self.p2_move_down = True
        elif self.game_over and key == arcade.key.R:
            self.restart_game() 

    def restart_game(self):
        self.game_over = False
        self.player1_score = 0
        self.player2_score = 0
        self.reset_ball()

    def on_key_release(self, key, modifiers):
        # Resto del código aquí...

        # Registrar eventos de liberación de tecla para detener el movimiento
        if key == arcade.key.W:
            self.p1_move_up = False
        elif key == arcade.key.S:
            self.p1_move_down = False
        elif key == arcade.key.UP:
            self.p2_move_up = False
        elif key == arcade.key.DOWN:
            self.p2_move_down = False
    
    def update(self, delta_time):
        self.ball.center_x += self.ball_speed_x
        self.ball.center_y += self.ball_speed_y
        
        
        # Colisiones con los bordes
        if self.ball.center_x - BALL_RADIUS <= 0 or self.ball.center_x + BALL_RADIUS >= SCREEN_WIDTH:
            self.ball_speed_x *= -1
            
        if self.ball.center_y - BALL_RADIUS <= 0 or self.ball.center_y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.ball_speed_y *= -1
        
        # Colisiones con las paletas
        if (
            self.ball.collides_with_sprite(self.player1_paddle)
            or self.ball.collides_with_sprite(self.player2_paddle)
        ):
            self.ball_speed_x *= -1
            self.colision.play()
            
        # Puntuación
        if self.ball.center_x - BALL_RADIUS <= 0:
            self.player2_score += 1
            
            self.reset_ball()
        elif self.ball.center_x + BALL_RADIUS >= SCREEN_WIDTH:
            self.player1_score += 1
            
            self.reset_ball()

        # Movimiento continuo de las paletas mientras se mantienen las teclas presionadas
        if self.p1_move_up and self.player1_paddle.center_y < SCREEN_HEIGHT - PADDLE_HEIGHT // 2:
            self.player1_paddle.center_y += 10  # Ajusta la velocidad según lo desees
        elif self.p1_move_down and self.player1_paddle.center_y > PADDLE_HEIGHT // 2:
            self.player1_paddle.center_y -= 10  # Ajusta la velocidad según lo desees
        
        if self.p2_move_up and self.player2_paddle.center_y < SCREEN_HEIGHT - PADDLE_HEIGHT // 2:
            self.player2_paddle.center_y += 10  # Ajusta la velocidad según lo desees
        elif self.p2_move_down and self.player2_paddle.center_y > PADDLE_HEIGHT // 2:
            self.player2_paddle.center_y -= 10  # Ajusta la velocidad según lo desees
    
    def reset_ball(self):
        self.ball.center_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
        self.ball.center_y = random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4)
        self.ball_speed_x = random.choice([-4, 4])
        self.ball_speed_y = random.choice([-4, 4])
       


game = PongGame(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
