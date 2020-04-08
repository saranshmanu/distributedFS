def read_file(file_path):
    try:
        data = open(file_path, 'rb')
        message = data.read()
        data.close()
        return True, message
    except Exception as inst:
        return False, None

def write_file(file_path, message):
    try:
        data = open(file_path, 'wb')
        data.write(message)
        data.close()
        return True
    except Exception as inst:
        print(str(inst))
        return False
