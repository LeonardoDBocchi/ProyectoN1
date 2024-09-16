import socket
import threading

sock_clientes = []
cuentas_dict = {'ferbor@tics.cl': {'Nombre': 'Fernanda', 'Pedidos':['Raspberry Pi 5', 'Chala Guchi','Naik Air Wuan']},
                'diecas@tics.cl': {'Nombre': 'Diego','Pedidos':['Raspberry Pi 5', 'Chicle de Choclo']},
                'sebara@tics.cl': {'Nombre':'Sebastian', 'Pedidos':['Polera Colo-Colo','Shore Corto']}}

catalogo = {'Bleyblade':{'cantidad':'3', 'Precio':'5'},
            'Polera Colo-Colo':{'cantidad':'4', 'Precio':'20'},
            'Raspberry Pi 5':{'cantidad':'100', 'Precio':'20'}} 

mutex = threading.Lock()

def cliente(sock):
    global sock_clientes, cuentas_dict
    while True:
        correo = sock.recv(1024).decode()
        if correo in cuentas_dict.keys():
            sock.send('Asistente: Wena malditooo!'.encode())
            sock.send('En que te ayudo \n [1] ver tus productos \n [2] ver catalogo \n ::exit '.encode())
            print(f'Cliente {correo} conectado.')

            while True:
                try:
                    data = sock.recv(1024).decode()
                except:
                    break

                if data == "::exit":
                    sock.send("Adios!".encode())
                    
                    # Se modifican las variables globales usando un mutex.
                    with mutex:
                        sock_clientes.remove(sock)
                    sock.close()
                    print(f'Cliente {correo} desconectado.')
                    break

                

                elif data == "1":
                    #muestra los pedidos de los clientes
                    print(f'El cliente {correo} ha consultado por sus pedidos')
                    with mutex:
                        pedidos = cuentas_dict[correo]['Pedidos']
                        
                    sock.send('Tus productos son: \n '.encode())
                    for producto in pedidos:
                        sock.send(f'{producto} \n'.encode())
                    
                elif data == '2':
                    # Se muestra el catálogo de la tienda
                    print(f'Cliente {correo} ha consultado el catálogo')
                    
                    # Definir el ancho de las columnas
                    ancho_producto = 20
                    ancho_cantidad = 10
                    ancho_precio = 10
                    
                    # Enviar el encabezado
                    sock.send(f"{'Producto':{ancho_producto}} {'Cantidad':{ancho_cantidad}} {'Precio ($)':{ancho_precio}}\n".encode())
                    
                    # Enviar cada producto en el catálogo
                    for producto, detalles in catalogo.items():
                        sock.send(f"{producto:{ancho_producto}} {detalles['cantidad']:{ancho_cantidad}} {detalles['Precio']:{ancho_precio}}\n".encode())


                else:
                    sock.send('Por favor indique un comando valido.'.encode())
            return None

        elif correo == '::exit':
            with mutex:
                sock_clientes.remove(sock)
            sock.close()
            return None

        else: 
            sock.send('No te cacho :/\nVuelve a intentarlo o ::exit para salir.'.encode())

    

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Se buscan clientes que quieran conectarse.
while True:

    # Se acepta la conexion de un cliente
    conn, addr = s.accept()
    sock_clientes.append(conn)

    # Se manda el mensaje de bienvenida
    conn.send("Bienvenid@ a 5 el G!\nIngrese su correo a continuacion: ".encode())

    # Se inicia el thread del cliente
    client_thread = threading.Thread(target=cliente, args=(conn,))
    client_thread.start()