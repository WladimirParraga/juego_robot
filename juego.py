import pygame
import sys
import random
import speech_recognition as sr  # Importar la biblioteca de reconocimiento de voz

# Inicializar Pygame y el módulo de sonido
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Batalla de Abecedario')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)

# Fuentes
font = pygame.font.Font(None, 36)
option_font = pygame.font.Font(None, 48)

# Cargar efectos de sonido para aciertos y errores
acierto_sounds = [
    pygame.mixer.Sound('sonidos/acierto_1.wav'),
    pygame.mixer.Sound('sonidos/acierto_2.wav'),
    pygame.mixer.Sound('sonidos/acierto_3.wav'),
    pygame.mixer.Sound('sonidos/acierto_4.wav'),
    pygame.mixer.Sound('sonidos/acierto_5.wav')
]

error_sounds = [
    pygame.mixer.Sound('sonidos/error_1.wav'),
    pygame.mixer.Sound('sonidos/error_2.wav'),
    pygame.mixer.Sound('sonidos/error_3.wav'),
    pygame.mixer.Sound('sonidos/error_4.wav'),
    pygame.mixer.Sound('sonidos/error_5.wav')
]

# Cargar imágenes (Sprites)
try:
    background = pygame.image.load('imagenes/background.png')
    background = pygame.transform.scale(background, (800, 450))  # Ajustar fondo a la pantalla (solo 450px de altura)

    player_image = pygame.image.load('imagenes/player_sprite.png')
    player_image = pygame.transform.scale(player_image, (100, 100))  # Ajustar tamaño del jugador

    enemy_image = pygame.image.load('imagenes/enemy_sprite.png')
    enemy_image = pygame.transform.scale(enemy_image, (100, 100))  # Ajustar tamaño del enemigo

except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")
    pygame.quit()
    sys.exit()

# Posiciones de los personajes
player_pos = (100, 300)
enemy_pos = (600, 300)

# Vida de los personajes
player_health = 100
enemy_health = 100

# Diccionario de preguntas con todas las letras del abecedario
questions = {
    "Avión": "A",
    "Ballena": "B",
    "Casa": "C",
    "Delfín": "D",
    "Elefante": "E",
    "Foca": "F",
    "Gato": "G",
    "Helado": "H",
    "Iglesia": "I",
    "Jirafa": "J",
    "Kilo": "K",
    "León": "L",
    "Manzana": "M",
    "Nube": "N",
    "Oso": "O",
    "Perro": "P",
    "Queso": "Q",
    "Ratón": "R",
    "Sol": "S",
    "Tigre": "T",
    "Uva": "U",
    "Vaca": "V",
    "Wafle": "W",
    "Xilófono": "X",
    "Yate": "Y",
    "Zorro": "Z"
}

# Función para dibujar la barra de vida
def draw_health_bar(health, position):
    max_health = 100
    bar_length = 100
    bar_height = 20
    fill = (health / max_health) * bar_length
    pygame.draw.rect(screen, RED, (*position, bar_length, bar_height))
    pygame.draw.rect(screen, GREEN, (*position, fill, bar_height))

# Función para mostrar texto
def draw_text(text, pos, color=BLACK, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Función para generar opciones manuales
def generate_options(correct_answer):
    options = [correct_answer]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while len(options) < 4:
        option = random.choice(letters)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options

# Función para reconocer la respuesta de voz
def reconocer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout=5)
            respuesta = recognizer.recognize_google(audio, language='es-ES')  # Reconocimiento de voz en español
            print(f"Respuesta reconocida: {respuesta}")
            return respuesta.upper()
        except sr.WaitTimeoutError:
            print("No se detectó ninguna respuesta.")
            return None
        except sr.UnknownValueError:
            print("No se entendió la respuesta.")
            return None
        except sr.RequestError:
            print("Error al conectarse al servicio de reconocimiento de voz.")
            return None

# Función para manejar la selección del jugador (manual o por voz)
def check_answer(correct_answer, use_voice=False):
    global player_health, enemy_health
    if use_voice:
        respuesta_voz = reconocer_voz()
        if respuesta_voz == correct_answer:
            enemy_health -= 20
            acierto_sound = random.choice(acierto_sounds)
            acierto_sound.play()
        else:
            player_health -= 20
            error_sound = random.choice(error_sounds)
            error_sound.play()
    else:
        return  # Si es manual, el jugador selecciona con el mouse

# Función para dibujar el botón de alternar entre voz y manual
def draw_toggle_button():
    button_color = BLUE if use_voice else GRAY
    pygame.draw.rect(screen, button_color, (50, 400, 200, 50))
    text = "Usar Voz" if not use_voice else "Usar Manual"
    draw_text(text, (70, 410), WHITE)

# Ciclo principal del juego
running = True
current_question = random.choice(list(questions.keys()))
options = generate_options(questions[current_question])
use_voice = False  # Cambiar entre True/False usando el botón

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Si se hace clic en el botón de alternar
            if 50 <= mouse_pos[0] <= 250 and 400 <= mouse_pos[1] <= 450:
                use_voice = not use_voice  # Alternar entre voz y manual
            if not use_voice:
                # Lógica para las respuestas manuales
                for i in range(2):
                    if 50 <= mouse_pos[0] <= 350 and 510 + i * 50 <= mouse_pos[1] <= 550 + i * 50:
                        if options[i] == questions[current_question]:
                            enemy_health -= 20
                            acierto_sound = random.choice(acierto_sounds)
                            acierto_sound.play()
                        else:
                            player_health -= 20
                            error_sound = random.choice(error_sounds)
                            error_sound.play()
                        current_question = random.choice(list(questions.keys()))
                        options = generate_options(questions[current_question])
                for i in range(2, 4):
                    if 450 <= mouse_pos[0] <= 750 and 510 + (i - 2) * 50 <= mouse_pos[1] <= 550 + (i - 2) * 50:
                        if options[i] == questions[current_question]:
                            enemy_health -= 20
                            acierto_sound = random.choice(acierto_sounds)
                            acierto_sound.play()
                        else:
                            player_health -= 20
                            error_sound = random.choice(error_sounds)
                            error_sound.play()
                        current_question = random.choice(list(questions.keys()))
                        options = generate_options(questions[current_question])

    # Dibujar fondo
    screen.blit(background, (0, 0))

    # Dibujar personajes
    screen.blit(player_image, player_pos)
    screen.blit(enemy_image, enemy_pos)

    # Dibujar barras de vida
    draw_health_bar(player_health, (player_pos[0], player_pos[1] - 30))
    draw_health_bar(enemy_health, (enemy_pos[0], enemy_pos[1] - 30))

    # Dibujar botón de alternar
    draw_toggle_button()

    # Dibujar sección inferior
    pygame.draw.rect(screen, DARK_GRAY, (0, 450, 800, 150))  # Sección inferior para preguntas y opciones

    # Mostrar pregunta
    draw_text(f"¿Con qué letra empieza {current_question}?", (50, 460), WHITE, font)

    # Mostrar opciones manuales
    if not use_voice:
        for i in range(2):
            pygame.draw.rect(screen, GRAY, (50, 510 + i * 50, 300, 40))
            draw_text(options[i], (200, 515 + i * 50), BLACK, option_font)
        for i in range(2, 4):
            pygame.draw.rect(screen, GRAY, (450, 510 + (i - 2) * 50, 300, 40))
            draw_text(options[i], (600, 515 + (i - 2) * 50), BLACK, option_font)
    else:
        # Si está activada la voz, escuchar la respuesta
        check_answer(questions[current_question], use_voice=True)
        current_question = random.choice(list(questions.keys()))

    pygame.display.flip()

    # Verificar si el juego ha terminado
    if player_health <= 0 or enemy_health <= 0:
        running = False

pygame.quit()
sys.exit()
