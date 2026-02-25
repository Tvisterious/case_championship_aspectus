password = ''
secret = 'r6apu7ep'  # твой секрет
encrypted = 'DG5Dv:=G'  # то, что найдешь

for i in range(8):
    # (зашифрованный[i] XOR (секрет[i] - 48)) + 48
    byte = ord(encrypted[i]) ^ (ord(secret[i]) - 48)
    password += chr(byte + 48)

print(password)
