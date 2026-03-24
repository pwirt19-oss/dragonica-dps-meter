import socket
import json
import random
import time

def send_damage():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 12345)
    
    print("Test Server: Sending random damage data to DPS Meter...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            damage = random.randint(100, 500)
            is_crit = random.random() < 0.1
            
            if is_crit:
                damage = int(damage * 1.5)
            
            damage_data = {
                'damage': damage,
                'crit': is_crit
            }
            
            message = json.dumps(damage_data)
            sock.sendto(message.encode(), server_address)
            
            print(f"Sent: {damage} damage (Crit: {is_crit})")
            
            time.sleep(random.uniform(0.5, 2.0))
    
    except KeyboardInterrupt:
        print("\nTest Server stopped")
    finally:
        sock.close()

if __name__ == '__main__':
    send_damage()