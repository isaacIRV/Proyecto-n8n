import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configuración de Firefox
options = Options()

driver = webdriver.Firefox(options=options)

# Datos simulados de ventas / usuarios a ingresar en el sistema web
usuarios = [
    ("Juaquin", "duoc@duoc.cl", "Valparaiso"),
    ("Pedro", "duoc@duoc.cl", "Valparaiso"),
    ("Juan", "duoc@duoc.cl", "Valparaiso"),
    ("Agustin", "duoc@duoc.cl", "Valparaiso"),
    ("Ricardo", "duoc@duoc.cl", "Valparaiso")
]

resultado = []

try:
    # Navegar a la plataforma
    driver.get("https://fundacion-instituto-profesional-duoc-uc.github.io/ATY1102-MantenedorUsuarios/index.html")

    # Iniciar sesión 
    usuario = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    usuario.send_keys("duoc")
    driver.find_element(By.ID, "password").send_keys("duoc123")
    driver.find_element(By.ID, "loginForm").submit()

    # Esperar que cargue el formulario principal
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dataForm"))
    )

    # Registrar cada usuario / venta
    for nombre, correo, ciudad in usuarios:
        user_field = driver.find_element(By.ID, "nombre")
        user_field.clear()
        user_field.send_keys(nombre)

        email_field = driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(correo)

        ciudad_field = driver.find_element(By.ID, "ciudad")
        ciudad_field.clear()
        ciudad_field.send_keys(ciudad)

        driver.find_element(By.ID, "dataForm").submit()

    time.sleep(1)

    # Extraer la tabla de resultados mediante XPath
    filas = driver.find_elements(By.XPATH, '//*[@id="dataTableBody"]/tr')
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        
        if len(celdas) >= 3:
            nombre_usuario = celdas[0].text.strip()
            email_usuario = celdas[1].text.strip()
            ciudad_usuario = celdas[2].text.strip()
               
            resultado.append({
                "nombre": nombre_usuario,
                "email": email_usuario,
                "ciudad": ciudad_usuario
            })

    # Imprimir resultado en JSON para que n8n lo capture
    print(json.dumps(resultado))

except Exception as e:
    # En caso de error, devolver un JSON con la descripción del problema
    print(json.dumps([{"error": str(e)}]))
finally:
    driver.quit()