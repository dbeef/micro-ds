import socket
import time
import pyaudio


# Acknowledgements:
# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
# https://stackoverflow.com/questions/43737015/play-raw-audio-file-in-python-in-realtime

def play_file(fname):
    # create an audio object
    f = open(fname, 'rb')
    p = pyaudio.PyAudio()
    chunk = 512

    # open stream based on the wave object which has been input.
    stream = p.open(format=pyaudio.paInt8,
                    channels=1,
                    rate=8000,
                    output=True)

    # read data (based on the chunk size)
    data = f.read(chunk)

    # play stream (looping from beginning of file to the end)
    while data != 0:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = f.read(chunk)

        # cleanup stuff.
    stream.close()
    p.terminate()
    f.close()


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    collected_data = b''
    while len(collected_data) < n:
        packet = sock.recv(n - len(collected_data))
        if not packet:
            return None
        collected_data += packet
        print("New packet, collected data: " + str(len(collected_data)))
        # print(str(packet))
    return collected_data


nintendo_ip = "10.42.0.251"
nintendo_port = 8080

nds_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nds_client.connect((nintendo_ip, nintendo_port))

size = 112640

timestamp_total = time.time()
nds_client.send('A'.encode('ascii'))

size_temp = size

d_total = bytearray()

while size_temp > 0:

    to_receive = 0

    if size_temp >= 1024:
        to_receive = 1024
    else:
        to_receive = size_temp

    d_total.extend(recvall(nds_client, to_receive))
    size_temp -= to_receive
    print("Received total: " + str(len(d_total)))
    print("Received now: " + str(to_receive))
    print("To receive left: " + str(size_temp))

print(type(d_total))
total_time = time.time() - timestamp_total
print("Total time: " + str(total_time))
f = open('out', 'wb')
f.write(d_total)
f.close()

play_file('out')
