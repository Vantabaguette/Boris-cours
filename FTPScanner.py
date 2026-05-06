import ftplib

def anonLogin(hostname):
    try:
        ftp =ftplib.FTP(hostname)
        ftp.login("anonymous")
        print("\n [+]" + str(hostname) + "FTP Anonymous Login Succeeded. ")
        ftp.quit()
        return True
    except Exception:
        print("\n [-]" + str(hostname) + "FTP Anonymous Login Failed. ")
        return False



if __name__ == "__main__" :
    anonLogin("83.166.138.123")