import os,socket,threading,time
import subprocess

allow_delete = True
#local_ip = socket.gethostbyname(socket.gethostname())
local_ip = "127.0.0.1"
local_port = 8000
currdir=os.path.abspath('.')

class FTPserverThread(threading.Thread):
    def __init__(self,(conn,addr)):
        self.conn=conn
        self.addr=addr
        self.basewd=currdir
        self.cwd=self.basewd
        self.rest=True
        self.pasv_mode=True
        threading.Thread.__init__(self)

    def run(self):
        self.conn.send('220 Welcome!\r\n')
        while True:
            cmd=self.conn.recv(512)
            if not cmd: break
            else:
                print 'Recieved:',cmd
                try:
                    func=getattr(self,cmd[:4].strip().upper())
                    func(cmd)
                except Exception,e:
                    print 'ERROR:',e
                    self.conn.send('500 Sorry.\r\n')

    def SYST(self,cmd):
        self.conn.send('215 UNIX Type: L8\r\n')
        
    def OPTS(self,cmd):
        if cmd[5:-2].upper()=='UTF8 ON':
            self.conn.send('200 OK.\r\n')
        else:
            self.conn.send('451 Sorry.\r\n')
    def USER(self,cmd):
        user=cmd.strip().split()[1]
        if user == "joke":
            self.conn.send('331 OK.\r\n')
        else:
            self.conn.send('530 sorry.\r\n Masukan Username yang benar.\r\n')
            #raise SystemExit

    def PASS(self,cmd):
        password=cmd.strip().split()[1]
        if password == "fun":
            self.conn.send('331 OK.\r\n')
        else:
            self.conn.send('530 sorry.\r\n Masukan Password yang benar.\r\n')
            #raise SystemExit

    
    def QUIT(self,cmd):
        self.conn.send('221 Goodbye.\r\n')
        # self.conn.close()

    
    # def NOOP(self,cmd):
    #     self.conn.send('200 OK.\r\n')
    
    def TYPE(self,cmd):
        self.mode=cmd[5]
        self.conn.send('200 Binary mode.\r\n')

    def CDUP(self,cmd):
        if not os.path.samefile(self.cwd,self.basewd):
            #learn from stackoverflow
            self.cwd=os.path.abspath(os.path.join(self.cwd,'..'))
        self.conn.send('200 OK.\r\n')
    
    def PWD(self,cmd):
        cwd=os.path.relpath(self.cwd,self.basewd)
        if cwd=='.':
            cwd='/'
        else:
            cwd='/'+cwd
        self.conn.send('257 \"%s\"\r\n' % cwd)
   
    def CWD(self,cmd):
        chwd=cmd[4:-2]
        if chwd=='/':
            self.cwd=self.basewd
        elif chwd[0]=='/':
            self.cwd=os.path.join(self.basewd,chwd[1:])
        else:
            self.cwd=os.path.join(self.cwd,chwd)
        self.conn.send('250 OK.\r\n')

    def PORT(self,cmd):
        if self.pasv_mode:
            self.servsock.close()
            self.pasv_mode = False
        l=cmd[5:].split(',')
        self.dataAddr='.'.join(l[:4])
        self.dataPort=(int(l[4])<<8)+int(l[5])
        self.conn.send('200 Get port.\r\n')

    def PASV(self,cmd):
        self.pasv_mode = True
        self.servsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.servsock.bind((local_ip,0))
        self.servsock.listen(1)
        ip, port = self.servsock.getsockname()
        print 'open', ip, port
        self.conn.send('227 Entering Passive Mode (%s,%u,%u).\r\n' %
                (','.join(ip.split('.')), port>>8&0xFF, port&0xFF))

    def start_datasock(self):
        if self.pasv_mode:
            self.datasock, addr = self.servsock.accept()
            print 'connect:', addr
        else:
            self.datasock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.datasock.connect((self.dataAddr,self.dataPort))

    def stop_datasock(self):
        self.datasock.close()
        if self.pasv_mode:
            self.servsock.close()



    def LIST(self,cmd):
        # print self.cwd
        data = "\n"
        for filename in os.listdir(self.cwd):
            # print filename
            data = data + filename + "\n"
        self.conn.send(data)
 #        self.conn.send('150 Here comes the directory listing.\r\n')
 #        print 'list:', self.cwd
 #        self.start_datasock()
	# #print "tes"
 #        for t in os.listdir(self.cwd):
 #            k=self.toListItem(os.path.join(self.cwd,t))
 #            self.datasock.send(k+'\r\n')
 #        self.stop_datasock()
 #        self.conn.send('226 Directory send OK.\r\n')

 #    def LST(self,cmd):
 #        self.conn.send('150 Here comes the directory listing.\r\n')
 #        print 'list:', self.cwd
	
 #        #fn = self.cwd
	# #print fn
	# #data = ""
	# for filename in os.listdir(self.cwd):
	# 	#print  filename
	# 	st=os.stat(self.cwd)
	# 	fullmode='rwxrwxrwx'
	# 	#self.conn.send('226 Directory send OK.\r\n')
	# 	mode=''
	# 	for i in range(9):
	# 		mode+=((st.st_mode>>(8-i))&1) and fullmode[i] or '-'
	# 	d=(os.path.isdir(fn)) and 'd' or '-'
	# 	#ftime=time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
		
	# 	data =  d+mode+' 1 user group '+str(st.st_size)+ftime+os.path.basename(fn)+filename
	# 	self.conn.send(data+'\r\n')
	# #self.conn.send(data)
        
 #        self.conn.send('226 Directory send OK.\r\n')
	

    def toListItem(self,fn):
        st=os.stat(fn)
        fullmode='rwxrwxrwx'
        mode=''
        for i in range(9):
            mode+=((st.st_mode>>(8-i))&1) and fullmode[i] or '-'
        d=(os.path.isdir(fn)) and 'd' or '-'
        ftime=time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
        return d+mode+' 1 user group '+str(st.st_size)+ftime+os.path.basename(fn)

    def MKD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        os.mkdir(dn)
        self.conn.send('257 Directory created.\r\n')

    def RMD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        if allow_delete:
            os.rmdir(dn)
            self.conn.send('250 Directory deleted.\r\n')
        else:
            self.conn.send('450 Not allowed.\r\n')


    def DELE(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        if allow_delete:
            os.remove(fn)
            self.conn.send('250 File deleted.\r\n')
        else:
            self.conn.send('450 Not allowed.\r\n')

    def RNFR(self,cmd):
        self.rnfn=os.path.join(self.cwd,cmd[5:-2])
        self.conn.send('350 Ready.\r\n')

    def RNTO(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        os.rename(self.rnfn,fn)
        self.conn.send('250 File renamed.\r\n')

    def REST(self,cmd):
        self.pos=int(cmd[5:-2])
        self.rest=True
        self.conn.send('250 File position reseted.\r\n')

    def RETR(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        #fn=os.path.join(self.cwd,cmd[5:-2]).lstrip('/')
        print 'Downlowding:',fn
        if self.mode=='I':
            fi=open(fn,'rb')
        else:
            fi=open(fn,'r')
        self.conn.send('150 Opening data connection.\r\n')
        if self.rest:
            fi.seek(self.pos)
            self.rest=False
        data= fi.read(1024)
        self.start_datasock()
        while data:
            self.datasock.send(data)
            data=fi.read(1024)
        fi.close()
        self.stop_datasock()
        self.conn.send('226 Transfer complete.\r\n')

    def STOR(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        print 'Uplaoding:',fn
        fileopen=open(fn,'wb')
        self.conn.send('150 Opening data connection.\r\n')
        # self.start_datasock()
        while True:
            data=self.conn.recv(1024)
            if not data: break
            fileopen.write(data)
        fileopen.close()
        # self.stop_datasock()
        fileopen.close()
        self.conn.send('226 Transfer complete.\r\n')

    def HELP(self,cmd):
        cmdlist = ( "CWD    --  Mengubah direktori aktif\n"
                    "QUIT   --  Keluar aplikasi\n"
                    "RETR   --  Mengunduh file\n"
                    "STOR   --  Mengunggah file\n"
                    "RNFR   --  Mengganti nama file\n"
                    "RNTO   --  Mengganti nama file\n"
                    "DELE   --  Menghapus file\n"
                    "RMD    --  Menghapus direktori\n"
                    "MKD    --  Membuat direktori\n"
                    "PWD    --  Mencetak direktori aktif\n"
                    "LIST   --  Mendaftar file dan direktori\n"
                    "HELP   --  Menampilkan daftar perintah\n")
        self.conn.send(cmdlist)


class FTPserver(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((local_ip,local_port))
        threading.Thread.__init__(self)

    def run(self):
        self.sock.listen(5)
        while True:
            th=FTPserverThread(self.sock.accept())
            th.daemon=True
            th.start()

    def stop(self):
        self.sock.close()

if __name__=='__main__':
    ftp=FTPserver()
    ftp.daemon=True
    ftp.start()
    print 'On', local_ip, ':', local_port
    raw_input('Enter to end...\n')
    ftp.stop()
