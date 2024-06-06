import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


# Inicialización de la aplicación FastAPI
app = FastAPI()

# HTML para la página del chat
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat Pyladies</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.1.4/dist/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100" onload="solicitarNombreUsuario()">
        <div class="flex flex-row h-screen">
            <div class="bg-gray-800 text-white w-1/4 p-4">
                <h2 class="text-xl mb-2">Usuarias</h2>
                <ul id="usuarios" class="overflow-y-auto"></ul>
            </div>
            <div class="flex flex-col w-3/4 p-6">
                <div class="flex-1 bg-white overflow-y-auto p-4 mb-4 rounded shadow-md">
                    <ul id="mensajes"></ul>
                </div>
                <div class="flex">
                    <input type="text" id="entradaMensaje" class="border p-2 flex-grow" placeholder="Escribe tu mensaje aquí..." onkeypress="if(event.keyCode == 13) { enviarMensaje(); }">
                    <button onclick="enviarMensaje()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Enviar</button>
                </div>
            </div>
        </div>
        <script>
            var ws;
            var mensajes = document.getElementById('mensajes');
            var usuarios = document.getElementById('usuarios');
            var entradaMensaje = document.getElementById('entradaMensaje');
            var nombreUsuario;
            function solicitarNombreUsuario() {
                nombreUsuario = prompt("Por favor, ingresa tu nombre:");
                if (nombreUsuario) {
                    ws = new WebSocket("ws://" + window.location.hostname + ":8000/ws?nombre_usuario=" + encodeURIComponent(nombreUsuario));
                    configurarWebSocket();
                }
            }

            function configurarWebSocket() {
                ws.onmessage = function(evento) {
                    var datosParseados = JSON.parse(evento.data);
                    if (datosParseados.tipo === 'mensaje') {
                        mensajeActual = JSON.parse(datosParseados.mensaje)
                        mensajes.innerHTML += '<li class="p-2 border-b"><strong>' + datosParseados.usuario + ':</strong> ' + mensajeActual.mensaje + '</li>';
                    } else if (datosParseados.tipo === 'lista_usuarios') {
                        usuarios.innerHTML = '';
                        datosParseados.usuarios.forEach(function(usuario) {
                            usuarios.innerHTML += '<li class="p-2 border-b">' + usuario + '</li>';
                        });
                    }
                };
            }

            function enviarMensaje() {
                var mensaje = entradaMensaje.value;
                ws.send(JSON.stringify({tipo: 'mensaje', mensaje: mensaje}));
                entradaMensaje.value = '';
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def obtener():
    return HTMLResponse(html)

# Clase para manejar las conexiones de WebSocket
class AdministradorConexiones:
    def __init__(self):
        self.conexiones_activas: dict[str, WebSocket] = {}

    async def conectar(self, websocket: WebSocket, nombre_usuario: str):
        await websocket.accept()
        self.conexiones_activas[nombre_usuario] = websocket
        await self._transmitir_lista_usuarios()

    def desconectar(self, websocket: WebSocket):
        nombre_usuario = next((usuario for usuario, ws in self.conexiones_activas.items() if ws == websocket), None)
        if nombre_usuario:
            del self.conexiones_activas[nombre_usuario]
            asyncio.create_task(self._transmitir_lista_usuarios())

    async def enviar_mensaje_personal(self, mensaje: str, websocket: WebSocket):
        await websocket.send_text(mensaje)

    async def transmitir(self, mensaje: str, nombre_usuario: str):
        for usuario, conexion in self.conexiones_activas.items():
            await conexion.send_text(mensaje)

    async def _transmitir_lista_usuarios(self):
        lista_usuarios = list(self.conexiones_activas.keys())
        await self.transmitir(json.dumps({'tipo': 'lista_usuarios', 'usuarios': lista_usuarios}), None)


@app.websocket("/ws")
async def endpoint_websocket(websocket: WebSocket, nombre_usuario: str = ""):
    if not nombre_usuario:
        await websocket.close(code=1000, reason="No se proporcionó nombre de usuario")
        return
    await administrador.conectar(websocket, nombre_usuario)
    try:
        while True:
            datos = await websocket.receive_text()
            await administrador.transmitir(json.dumps({'tipo': 'mensaje', 'usuario': nombre_usuario, 'mensaje': datos}), nombre_usuario)
    except WebSocketDisconnect:
        administrador.desconectar(websocket)
    except Exception as e:
        print(f"Error: {e}")

# Instancia del administrador de conexiones
administrador = AdministradorConexiones()

