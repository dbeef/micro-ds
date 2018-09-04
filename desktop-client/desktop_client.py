import socket
import pyaudio

# Acknowledgements:
# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
# https://stackoverflow.com/questions/43737015/play-raw-audio-file-in-python-in-realtime

nintendo_ip = "10.42.0.147"
nintendo_port = 8080
d_total = bytearray()  # Tablica, do której zbierzemy bajty dźwięku
size = 40000  # Całkowita ilość bajtów do odczytania
size_temp = size  # Do zapisywania ilości bajtów pozostałych do odczytania
nds_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nds_client.connect((nintendo_ip, nintendo_port))
nds_client.send('A'.encode('ascii'))


def recvall(sock, n):
    collected_data = b''
    while len(collected_data) < n:
        packet = sock.recv(n - len(collected_data))
        if len(packet) == 0:
            print("NDS zamknął połączenie")
            sock.close()
            return None
        collected_data += packet
        print("New packet, collected data: " + str(len(collected_data)))
    return collected_data


def play_file(fname):
    # otwórz plik
    f = open(fname, 'rb')
    p = pyaudio.PyAudio()
    chunk = 512
    # ustaw specifikację dźwięku -
    # znamy ją, ponieważ taką konfigurację ustawiliśmy na NDS)
    stream = p.open(format=pyaudio.paInt8,
                    channels=1,
                    rate=8000,
                    output=True)
    # odczytaj kawałek danych
    data = f.read(chunk)
    # graj
    while data != 0:
        # pisanie do strumienia jest tym, co odgrywa dźwięk
        stream.write(data)
        data = f.read(chunk)
    # posprzątaj po sobie
    stream.close()
    p.terminate()
    f.close()


while size_temp > 0:
    to_receive = 0
    if size_temp >= 1024:
        to_receive = 1024
    else:
        to_receive = size_temp

    received = recvall(nds_client, to_receive)

    if received is not None:
        d_total.extend(received)
    else:
        break
    size_temp -= to_receive
    print("Całkowita ilość otrzymanych bajtów: " + str(len(d_total)))
    print("Ilość otrzymana w tym obiegu pętli: " + str(to_receive))
    print("Pozostała ilość do otrzymania: " + str(size_temp))

print(type(d_total))
f = open('out', 'wb')
f.write(d_total)
f.close()
play_file('out')
