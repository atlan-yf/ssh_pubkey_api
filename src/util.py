def verifyPubKey(pubKey: str) -> bool:
    # Verify the public key
    if not isinstance(pubKey, str):
        return False
    
    #todo
    return True

# append the pubkey str to ~/.ssh/authorized_keys
def addPubKey(pubKey: str):
    # Add the public key to the database
    if not verifyPubKey(pubKey):
        return
    
    import os
    # Open the file and append the public key
    with open(os.path.expanduser('~/.ssh/authorized_keys'), 'a') as f:
        f.write(pubKey + '\n')