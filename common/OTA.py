from time import sleep_ms
from machine import reset
from os import listdir
import sys

def extract_boundary(request):
    try:
        boundary_start=request.find('boundary=')
        if boundary_start==-1:return False
        boundary_start+=9
        boundary_end=boundary_start+request[boundary_start:].find('\n')-1
        boundary=request[boundary_start:boundary_end]
        return boundary
    except Exception as e:
        sys.print_exception(e)
        return False

def extract_file_content(request):
    try:
        # request=request.decode()
        boundary=extract_boundary(request)
        content_start=request.find('Content-Type: application/octet-stream\r\n\r\n')+42
        content_end=content_start+request[content_start:].find('--'+boundary)
        file_content=request[content_start:content_end]
        return file_content
    except Exception as e:
        print('Error extracting file content')
        sys.print_exception(e)
        return False

def extract_filename(request):
    try:
        # request=request.decode()

        filename_start=request.find('filename="')+10
        filename_end=filename_start+request[filename_start:].find('"')
        filename=request[filename_start:filename_end]
        return filename
    except Exception as e:
        print('Error extracting filename')
        sys.print_exception(e)
        return False
    
def backup_file(filename):
    try:
        with open(filename,'rb') as f:
            content=f.read()
        with open(filename+'.backup','wb') as f:
            f.write(content)
    except Exception as e:
        print('Error backing up old file')
        sys.print_exception(e)
        return False

def write_file(conn,filename,content):
    try:
        files=listdir()
        if filename in files:backup_file(filename)
        with open(filename,'w') as f:
            f.write(content)
        conn.send('HTTP/1.1 200 OK\r\n')
        conn.close()
        sleep_ms(1000)
        reset()
    except Exception as e:
        conn.send('HTTP/1.1 500 Internal Server Error\r\n')
        conn.close()
        sleep_ms(1000)
        print('Error writing file')
        sys.print_exception(e)
        return False