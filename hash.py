import hashlib

def hash_image(image):
    return hashlib.sha256(image).hexdigest()

print(hash_image(br"C:\Users\adrhd\Pictures\photo$.JPG"))

