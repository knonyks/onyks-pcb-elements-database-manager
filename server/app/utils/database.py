def createPostgresURI(username, password, host, name, port):
    addr = 'postgresql://'
    addr += username
    addr += ':'
    addr += password
    addr += '@' + host + ":" + str(port) + '/'
    addr += name
    return addr