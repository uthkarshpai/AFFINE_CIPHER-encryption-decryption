import random
import streamlit as st

class AffineCipher:
    def __init__(self, a=None, b=None, m=26):
        self.m = m
        
        if a is None:
            self.a = self.generate_coprime_key(self.m)  # Randomly generate if not provided
        else:
            self.a = a
            
        self.b = b if b is not None else random.randint(0, m-1)  # Random b if not provided
        
        if self.gcd(self.a, self.m) != 1:
            raise ValueError(f"a={self.a} and m={self.m} are not coprime, choose a different 'a'.")
    
    def generate_coprime_key(self, m):
        """Generate a random coprime key 'a'."""
        while True:
            a = random.randint(1, m-1)
            if self.gcd(a, m) == 1:
                return a
    
    # Function to find gcd of two numbers
    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    # Function to find modular inverse of a modulo m
    def mod_inverse(self, a, m):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        raise ValueError(f"No modular inverse for a={a} under modulo {m}.")
    
    # Encrypt a single character
    def encrypt_char(self, char):
        if char.isalpha():
            is_upper = char.isupper()
            x = ord(char.lower()) - ord('a')  # convert to 0-25
            encrypted_char = (self.a * x + self.b) % self.m
            encrypted_char = chr(encrypted_char + ord('a'))  # convert back to character
            return encrypted_char.upper() if is_upper else encrypted_char
        return char
    
    # Decrypt a single character
    def decrypt_char(self, char):
        if char.isalpha():
            is_upper = char.isupper()
            y = ord(char.lower()) - ord('a')  # convert to 0-25
            a_inv = self.mod_inverse(self.a, self.m)
            decrypted_char = (a_inv * (y - self.b)) % self.m
            decrypted_char = chr(decrypted_char + ord('a'))  # convert back to character
            return decrypted_char.upper() if is_upper else decrypted_char
        return char
    
    # Encrypt the entire text
    def encrypt(self, plaintext):
        return ''.join([self.encrypt_char(char) for char in plaintext])
    
    # Decrypt the entire text
    def decrypt(self, ciphertext):
        return ''.join([self.decrypt_char(char) for char in ciphertext])

    def get_keys(self):
        """Return the keys used."""
        return self.a, self.b

# Streamlit Interface
def main():
    st.title("Affine Cipher Encryption & Decryption")
    
    # Initialize cipher object with random a and b
    if 'cipher' not in st.session_state:
        st.session_state.cipher = AffineCipher()

    cipher = st.session_state.cipher
    a, b = cipher.get_keys()

    st.sidebar.header("Affine Cipher Keys")
    st.sidebar.write(f"Multiplicative Key (a): {a}")
    st.sidebar.write(f"Additive Key (b): {b}")
    
    if st.sidebar.button("Generate New Random Keys"):
        st.session_state.cipher = AffineCipher()  # Reset the cipher with new random keys
        cipher = st.session_state.cipher
        st.sidebar.write("New keys generated!")
        st.experimental_rerun()

    # Input section
    operation = st.selectbox("Choose Operation", ["Encrypt", "Decrypt"])
    message = st.text_area("Enter the message")
    
    # Initialize the filename field
    filename = st.text_input("Enter the filename (with .txt extension)", "output.txt")
    
    if st.button(f"{operation} Message"):
        if operation == "Encrypt":
            st.session_state.encrypted_message = cipher.encrypt(message)
            st.write(f"**Encrypted Message:** {st.session_state.encrypted_message}")
        elif operation == "Decrypt":
            st.session_state.decrypted_message = cipher.decrypt(message)
            st.write(f"**Decrypted Message:** {st.session_state.decrypted_message}")
    
    # Save option
    if st.button("Save Message to File"):
        if not filename.endswith('.txt'):
            st.error("Please ensure the filename ends with .txt")
        elif operation == "Encrypt" and 'encrypted_message' in st.session_state:
            with open(filename, 'w') as file:
                file.write(st.session_state.encrypted_message)
            st.write(f"Encrypted message saved to {filename}")
        elif operation == "Decrypt" and 'decrypted_message' in st.session_state:
            with open(filename, 'w') as file:
                file.write(st.session_state.decrypted_message)
            st.write(f"Decrypted message saved to {filename}")
        else:
            st.error("No message available to save. Please perform encryption/decryption first.")

if __name__ == "__main__":
    main()
