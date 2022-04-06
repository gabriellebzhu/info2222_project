1. Properly store passwords on the server
2. When log in, first check server’s certificate (e.g., you can manually create one using a hardcoded CA public key in your code)
3. Securely transmitting a pwd to server (leveraging secure protocols or design the secure transmission properly)
   1. Use a HMAC to make no certificate
4. Properly check whether password is correct (at least use the simple method that defends against offline pre-computation attacks)
5. Securely transmitting the message from A to B, even the server who can forward communication transcript cannot read the message, or modify the ciphertext (leveraging secure protocols or design the authenticated secure transmission properly)
