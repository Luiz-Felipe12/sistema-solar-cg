import sys
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from texture import load_images

# Variaveis globais
global angulo, fAspect, rotX, rotY, rotZ, obsX, obsY, obsZ, solAtivo
global rotX_ini, rotY_ini, obsX_ini, obsY_ini, obsZ_ini, x_ini, y_ini, botao
global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune

solAtivo = 1
orbita = 1
eixoX, eixoY, eixoZ = 0, 0, 0

# Constantes utilizadas na interacao com o mouse
SENS_ROT = 5.0
SENS_OBS = 10.0
SENS_TRANSL = 10.0


def Desenha_planeta(textura, pos_y, pos_x, escala, diametro, raio):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t*2

    # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
    # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    # glutBitmapString(GLUT_BITMAP_9_BY_15, planeta)
    glTranslated(0, -pos_y, 0)
    # Movimento de Translação
    glTranslatef((pos_x * math.cos(2.0 * 3.14 * a*raio / 100)),
                 (pos_y + pos_y * math.sin(2.0 * 3.14 * a*raio / 100)), 0)
    obj = gluNewQuadric()
    gluQuadricTexture(obj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura)
    glScalef(escala, escala, escala)
    glRotated(a * 20, 0, 0, 1)
    gluSphere(obj, diametro, 25, 25)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()  # Fim do push


def Desenha_planetas_com_Satelites_e_Aneis(textura_planeta, textura_satelite, textura_aneis, pos_y, pos_x, escala, diametro1, diametro2, raio, raio_lua):

    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t * 2

    # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
    # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    # glutBitmapString(GLUT_BITMAP_9_BY_15, planeta)
    glTranslated(0, -pos_y, 0)
    # Movimento de Translacao
    glTranslatef((pos_x * math.cos(2.0 * 3.14 * a*raio / 100)),
                 (pos_y + pos_y * math.sin(2.0 * 3.14 * a*raio / 100)), 0)
    obj = gluNewQuadric()
    gluQuadricTexture(obj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_planeta)
    glScalef(escala, escala, escala)
    glRotated(a*20, 0, 0, 1)
    gluSphere(obj, diametro1, 25, 25)
    glScalef(escala, escala, escala)
    # Desenha o anel
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_aneis)
    desenhaAnel(pos_x/80, pos_y/80)

    # Satelite
    # Translacao da Lua
    glTranslatef(pos_x/20*(math.cos(2.0 * 3.14 * a*raio_lua / 100)),
                 (pos_y/20*math.sin(2.0 * 3.14 * a*raio_lua / 100)), 0)
    glBindTexture(GL_TEXTURE_2D, textura_satelite)
    glScalef(escala, escala, escala)
    glRotated(a * 5, 1, 0, 1)
    gluSphere(obj, diametro2, 50, 50)
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()  # Fim do push


def desenha_planetas_com_Satelites(textura_planeta, textura_satelite, pos_y, pos_x, escala, diametro1, diametro2, raio, raio_lua):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t*2

    # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
    # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    # glutBitmapString(GLUT_BITMAP_9_BY_15, planeta)
    glTranslated(0, -pos_y, 0)
    # Movimento de Translacao
    glTranslatef((pos_x * math.cos(2.0 * 3.14 * a*raio / 100)),
                 (pos_y + pos_y * math.sin(2.0 * 3.14 * a*raio / 100)), 0)
    obj = gluNewQuadric()
    gluQuadricTexture(obj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_planeta)
    glScalef(escala, escala, escala)
    glRotated(a*20, 0, 0, 1)
    gluSphere(obj, diametro1, 25, 25)

    # Satelite
    # Translacao da Lua
    glTranslatef(pos_x/10*(math.cos(2.0 * 3.14 * a*raio_lua / 100)),
                 (pos_y/10*math.sin(2.0 * 3.14 * a*raio_lua / 100)), 0)

    glBindTexture(GL_TEXTURE_2D, textura_satelite)
    glScalef(escala, escala, escala)
    glRotated(a*5, 1, 0, 1)
    gluSphere(obj, diametro2, 50, 50)
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()  # Fim do push


def desenhaAnel(eixoX, eixoY):
    # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
    # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
    glPushMatrix()
    # glBegin Inicia uma lista de vertices, e o argumento determina qual objeto sera desenhado
    # GL_LINE_LOOP exibe uma sequencia de linhas conectando os pontos definidos por glVertex e ao final liga o primeiro como ultimo ponto
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        rad = i*3.14/180
        glVertex2f(math.cos(rad)*eixoX, math.sin(rad)
                   * eixoY)  # Especifica um vertice
    glEnd()  # Fim do begin
    # Retira a matriz do topo da pilha e torna esta ultima a matriz de transformacao corrente
    glPopMatrix()  # Fim do push


def Desenha():
    glDrawBuffer(GL_BACK)
    # Limpa a janela de visualizao com a cor de fundo especificada
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # desenha todos os objetos na tela
    Sistema_Solar()
    glutSwapBuffers()

# Desenha o sistema solar e as orbitas dos planetas


def Sistema_Solar():
    global mercury, venus

    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # SOL
    if (solAtivo == 1):
        # GLfloat
        light_ambient = [eixoX, eixoY, eixoZ, 1.0]
        light_diffuse = [eixoX, eixoY, eixoZ, 1.0]
        light_specular = [eixoX, eixoY, eixoZ, 1.0]
        light_position = [1.0, 0.0, 0.0, 1.0]

        # configura alguns parametros do modelo de iluminacao: MATERIAL
        mat_ambient = [0.7, 0.7, 0.7, 1.0]
        mat_diffuse = [0.8, 0.8, 0.8, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        high_shininess = [100.0]

        glShadeModel(GL_SMOOTH)

        # Propriedades da fonte de luz
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)

        glPushMatrix()
        glRasterPos2f(0, 1.5)
        # glutBitmapString(GLUT_BITMAP_9_BY_15, "Sol")
        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, sun)
        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
        glRotated(a*7, 0, 0, 1)
        glScalef(3, 3, 3)
        gluSphere(qobj, 1, 25, 25)
        glPopMatrix()  # Fim do push
        glDisable(GL_TEXTURE_2D)
    else:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

       # MERCURIO - Diametro: 4.879,4 km
    Desenha_planeta(mercury, 7, 7, 2, 0.48, 3.7)

    # VENUS - Diametro: 12.103,6 km
    Desenha_planeta(venus, 17, 17, 1.2, 1.21, 2.5)

    # TERRA E LUA - Diametro Terra: 12.756,2 km
    desenha_planetas_com_Satelites(
        earth, moon, 27, 27, 1.2, 1.27, 0.5, 1.9, 0.2)

    # MARTE - Diametro: 6.792,4 km
    desenha_planetas_com_Satelites(mars, moon, 41, 41, 1.2, 0.68, 0.5, 1.9, 1)

    # JUPITER       */ #Diametro: 142.984 km
    Desenha_planetas_com_Satelites_e_Aneis(
        jupiter, moon, saturnRing, 80, 80, 1.5, 1.43, 0.25, 1.9, 1)

    # SATURNO     */ #Diametro: 120.536 km
    Desenha_planetas_com_Satelites_e_Aneis(
        saturn, moon, saturnRing, 97, 97, 1.5, 1.2, 0.25, 1.5, 1)

    # URANO   */ #Diametro: 51.118 km
    Desenha_planetas_com_Satelites_e_Aneis(
        saturnRing, moon, uranusRing, 107, 107, 1.5, 0.51, 0.25, 1.2, 1.3)

    # NETUNO   */  #Diametro: 49.528 km
    Desenha_planetas_com_Satelites_e_Aneis(
        neptune, moon, uranusRing, 127, 127, 1.5, 0.495, 0.20, 1, 1)

    # PLUTAO */  #Diametro: 2.377 km
    desenha_planetas_com_Satelites(
        moon, moon, 140, 140, -0.35, 2.3, 3, 0.8, 0.6)

    glRasterPos2f(0, -51)
    # glutBitmapString(GLUT_BITMAP_9_BY_15, "Cinturao de Asteroides")
    # desenhaAsteroide(10,10)

# Cria uma orbita


def Desenha_Orbita(pos_y, pos_x):
    # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
    # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
    glPushMatrix()
    glTranslated(0, -pos_y, 0)  # Produz uma translacao em (x, y, z)
    # glBegin Inicia uma lista de vertices, e o argumento determina qual objeto sera desenhado
    # GL_LINE_LOOP exibe uma sequencia de linhas conectando os pontos definidos por glVertex e ao final liga o primeiro como ultimo ponto
    glBegin(GL_LINE_LOOP)
    for i in range(100):  # Desenha a linha da orbita, a variavel i vai juntando cada linha em uma circunferencia
        glVertex2f(
            pos_x * math.cos(2.0 * 3.14 * i / 100),
            pos_y + pos_y * math.sin(2.0 * 3.14 * i / 100)
        )  # Especifica um vertice

    glEnd()  # Fim do begin
    glPopMatrix()  # Fim do push


# Chama a funcao para criar as orbitas de cada planeta
def mostraOrbitas():

    # MERCURIO - Diametro: 4.879,4 km
    Desenha_Orbita(7, 7)

    # VENUS - Diametro: 12.103,6 km
    Desenha_Orbita(17, 17)

    # TERRA - Diametro: 12.756,2 km
    Desenha_Orbita(27, 27)

    # MARTE -Diametro: 6.792,4 km
    Desenha_Orbita(41, 41)

    # JUPITER - Diametro: 142.984 km
    Desenha_Orbita(80, 80)

    # SATURNO - Diametro: 120.536 km
    Desenha_Orbita(97, 97)

    # URANO -Diametro: 51.118 km
    Desenha_Orbita(107, 107)

    # NETUNO - Diametro: 49.528 km
    Desenha_Orbita(127, 127)

    # PLUTAO - Diametro: 2.377 km
    # Desenha_Orbita(140,140)


def Sistema_Solar_com_orbitas():
    glDrawBuffer(GL_BACK)
    # Limpa a janela de visualizao com a cor de fundo especificada
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # desenha todos os objetos na tela
    Sistema_Solar()
    mostraOrbitas()
    glutSwapBuffers()


def atualiza():
    # Marca o plano normal da janela atual como precisando ser reexibido na proxima iteracao do glutMainLoop
    glutPostRedisplay()


def Inicializa():
    global angulo, rotX, rotY, rotZ, obsX, obsY, obsZ
    global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune

    # Inicializa a variavel que especifica o angulo da projecao
    # perspectiva
    angulo = 10
    # Inicializa as variaveis usadas para alterar a posicao do
    # observador virtual
    rotX = 0
    rotY = 0
    rotZ = 0
    obsX = obsY = 0
    obsZ = 150

    # loadTexture() #Inicializa as texturas
    sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune = load_images()

    # #Inicializa obj
    # inicializaObj()

    # Especificando que as facetas traseiras serao cortadas
    glEnable(GL_CULL_FACE)  # Habilita recursos do GL -> cortar as facetas
    glCullFace(GL_BACK)  # Nao mostrar faces do lado de dentro

    # Prepara o OpenGL para realizar calculos de iluminacao
    glEnable(GL_LIGHTING)
    # Especifica que a fonte de luz tem cor padrao para luz (branco)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)  # Atualiza o buffer de profundidade

# Passos padrao da biblioteca
# Especifica a posicao do observador e do alvo


def PosicionaObservador():
    # Especifica o sistema de coordenadas do modelo
    glMatrixMode(GL_MODELVIEW)
    # Inicializa sistema de coordenadas do modelo
    glLoadIdentity()

    # Posiciona e orienta o observador - transformacoes geometricas de translacao e rotacao em (eixoX, eixoY, eixoZ)
    glTranslatef(-obsX*0.5, -obsY*0.5, -obsZ*0.5)
    glRotatef(rotX, 1, 0, 0)
    glRotatef(rotY, 0, 1, 0)
    glRotatef(rotZ, 0, 0, 1)

# Funcao padrao da biblioteca para especificar o volume de visualizacao


def EspecificaParametrosVisualizacao():
    global angulo
    # Especifica sistema de coordenadas de projecao
    glMatrixMode(GL_PROJECTION)
    # Inicializa sistema de coordenadas de projecao
    glLoadIdentity()
    # Especifica a projecao perspectiva(angulo,aspecto,zMin,zMax)
    gluPerspective(angulo, fAspect, 0.5, 2000)
    # Especifica a posicao do observador e do alvo
    PosicionaObservador()

# Funcao padrao da biblioteca para alterar o tamanho da tela


def Redimensiona(w, h):
    global fAspect
    # Para previnir uma divisao por zero
    if (h == 0):
        h = 1

    # Especifica as dimensoes da viewport
    glViewport(0, 0, w, h)
    # Calcula a correção de aspecto
    fAspect = w/h
    # Especifica o volume de visualizacao
    EspecificaParametrosVisualizacao()

# Funcoes para interagir com teclado e mouse


def SpecialKeyboard(tecla, eixoX, eixoY):
    global angulo, rotX, rotY
    # Realiza transformacoes geometricas de rotacao (gira o objeto ao redor do vetor eixoX, eixoY, eixoZ)

    if tecla == GLUT_KEY_RIGHT:
        glRotatef(rotX, 1, 0, 0)
        rotX += 1

    elif tecla == GLUT_KEY_LEFT:
        glRotatef(rotY, 0, 1, 0)
        rotY += 1

    elif tecla == GLUT_KEY_DOWN:
        if (angulo <= 150):
            angulo += 5  # diminui zoom

    elif tecla == GLUT_KEY_UP:
        if (angulo >= 10):
            angulo -= 5  # aumenta zoom
    EspecificaParametrosVisualizacao()  # Modifica a visualizacao do usuario
    # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop
    glutPostRedisplay()

# Verifica se alguma tecla foi pressionada (com excecao das direcionais)


def teclado(tecla, eixoX, eixoY):
    global solAtivo, orbita, obsZ

    if tecla == chr(27):  # Esc para sair
        sys.exit()

    elif tecla == b'l' or tecla == b'L':  # Remove o Sol e toda a luz do sistema
        solAtivo = not solAtivo
        # Exibe na tela o retorno da funcao chamada
        glutDisplayFunc(Sistema_Solar_com_orbitas)

    elif tecla == b'c' or tecla == b'C':  # Centraliza no Sol - visao superior do sistema
        obsZ = 50

    elif tecla == b'o' or tecla == b'O':  # Mostra ou remove as orbitas
        orbita = not orbita

        if (orbita == True):
            # Exibe na tela o retorno da funcao chamada
            glutDisplayFunc(Sistema_Solar_com_orbitas)
        else:
            # Mostra o sistema solar sem as orbitas
            # Exibe na tela o retorno da funcao chamada
            glutDisplayFunc(Desenha)

    # Volta a matriz ao seu estado padrao (exemplo, comecar da origem em vez do estado atual)
    # Visto que algumas transformacoes sao relativas ao estado atual da matriz (ex: rotacao e translacao)
    glLoadIdentity()
    # Cria uma matriz de visualizacao derivada de um ponto de vista indicando centro da cena e vetor UP
    gluLookAt(obsX, obsY, obsZ, 0, 0, 0, 0, 1, 0)
    # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop
    glutPostRedisplay()

# Gerencia os eventos do mouse, se botao foi pressionado ou nao


def GerenciaMouse(button, state, eixoX, eixoY):
    global obsX, obsY, obsZ, rotX, rotY, obsX_ini, obsY_ini, obsZ_ini, rotX_ini, rotY_ini, x_ini, y_ini, botao

    # Se foi pressionado, salva os parametros atuais
    if (state == GLUT_DOWN):
        x_ini = eixoX
        y_ini = eixoY
        obsX_ini = obsX
        obsY_ini = obsY
        obsZ_ini = obsZ
        rotX_ini = rotX
        rotY_ini = rotY
        botao = button
    else:
        botao = -1


def GerenciaMovimento(eixoX, eixoY):
    global x_ini, y_ini, rotX, rotY, obsX, obsY, obsZ

    # Botao esquerdo do mouse
    if (botao == GLUT_LEFT_BUTTON):
        # Calcula diferenças
        deltax = x_ini - eixoX
        deltay = y_ini - eixoY
        # E modifica angulos
        rotY = rotY_ini - deltax/SENS_ROT
        rotX = rotX_ini - deltay/SENS_ROT

    # Botao direito do mouse
    elif (botao == GLUT_RIGHT_BUTTON):
        deltax = x_ini - eixoX
        deltay = y_ini - eixoY
        # Calcula diferença
        deltaz = deltax - deltay
        # E modifica distancia do observador
        obsZ = obsZ_ini + deltaz/SENS_OBS

    # Padrao da funcao, ja que altera a visualizacao (angulo ou distancia)
    PosicionaObservador()
    # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop
    glutPostRedisplay()


def main():
    # Inicializa a lib glut, com um contexto openGL especificando a versao e em modo de compatibilidade
    # Sera utilizada para criar janelas, ler o teclado e o mouse
    glutInit(sys.argv)
    glutInitContextVersion(1, 1)
    glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE)

    # Inicia uma janela, definindo tamanho e posicao
    # Define janela com RGB, profundidade de dois buffers (um exibido e outro renderizando para trocar com o atual)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1800, 1200)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Sistema Solar")

    # imprimeInstrucoes() <-> Metodo comentado

    # Exibe na tela o retorno da funcao chamada
    glutDisplayFunc(Sistema_Solar_com_orbitas)
    # ??? Qual o objetivo?
    glutReshapeFunc(Redimensiona)
    # Define o retorno das teclas direcionais, teclado e mouse para a janela atual (callback gerado por evento)
    glutSpecialFunc(SpecialKeyboard)
    glutKeyboardFunc(teclado)
    glutMouseFunc(GerenciaMouse)
    # Quando o mouse se move dentro da janela enquanto um ou mais botoes do mouse sao pressionados
    glutMotionFunc(GerenciaMovimento)

    # Inicializa ambiente (variaveis, texturas, fonte de luz e atualizacao de profundidade)
    Inicializa()

    # Processamento em segundo plano ou animacao continua. Chama metodo de atualizar a janela atual
    glutIdleFunc(atualiza)
    # Renderiza a janela criada
    glutMainLoop()
    return 0


main()
