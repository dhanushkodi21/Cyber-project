import streamlit as st
from scipy.io import wavfile 
import numpy as np
import random
import time
import string
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES,DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
import seccure
import rsa

st.set_page_config(
    page_title="Audio/Message Encryption and Decryption",
    page_icon="https://thumbs.dreamstime.com/z/brown-yellow-eye-texture-black-fringe-brown-yellow-eye-texture-black-fringe-white-background-118702165.jpg",
    layout="centered",
    initial_sidebar_state="expanded")

app_mode=st.sidebar.selectbox('Select Page',['Audio Encryption','Message Encryption (RSA)'])

page_bg_img='''
    <style>
    .stApp{
    background-size:cover;
    background-image:url('https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhJoDsppA6x2JI7WQnTgfnYaoTFVW4W48Sg-VDTMjM_l5knjx7o0_pURlt0SDAfHU0mk_jZQPCZojgLiNFQYq9ak_2I2WsNwjrQ_c8OBc-w8f4ATsuq0nK3FmY8NfHZrhwPPatB9qM2Ugl4UjFQI4goBPqTTjJECavIYOgNCLDVlWkB4CBvcBeeCoHabQ/s2560/wallpaper-for-setup-gamer-2560x1440.jpg')
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)



if app_mode=='Audio Encryption':

    st.write('<h1 style="color:crimson;">Audio Encryption and Decryption</h1>', unsafe_allow_html=True)

    encrypt,decrypt=st.columns(spec=[1,1],gap="large")

    with encrypt:
        st.subheader("Encryption: ")
        choice=st.selectbox("Choose an Algorithm",["AES","DES","AES with RSA","Triple DES","Fernet","ECC"],key="encrypt")
        upload_file=st.file_uploader("Choose a wav file",type=["wav"],key="encrypt_file")
        if upload_file is not None:
            bytes_data=upload_file.getvalue()
            with open('uploaded-audio.wav', 'wb') as fw:
                fw.write(bytes_data)
            
            if choice=="AES":
                with open('uploaded-audio.wav', 'rb') as fd:
                    contents = fd.read()
                    
                size=st.selectbox("Choose an key size(in bits)",[128,192,256])
                size=size//8
                if size==16:
                    AES_KEY="xc93yVibrHGAvZ2c"
                elif size==24:
                    AES_KEY="DD77YM3M9YMvXxNvTAvu8ZY5"
                elif size==32:
                    AES_KEY="kN0am97PCnxBZj5OEyz5Xf1PZI9Jiy6X"
                #AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(size))
                AES_IV = "ZriJsdHXo2ynxyJd"
                text="AES key is: " + AES_KEY + " \nAES IV is: " + AES_IV + " \nAES Mode is CFB"
                st.text(text)
                st.error("Note the above details for decryption of the file")
                encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
                encrypted_audio = encryptor.encrypt(contents)
                st.write('<h5 style="color:blue">Your Encrypted File</h5>',unsafe_allow_html=True)
                click=st.download_button(label="Encrypted file",data=encrypted_audio,file_name="AES_encry.wav",mime="audio/wav")
            
            elif choice=="DES":
                with open('uploaded-audio.wav', 'rb') as fd:
                    contents = fd.read()
                size=st.selectbox("Choose an key size(in bits)",[64])
                size=size//8
                DES_KEY="WlbbTdDT"
                DES_IV="WmrAOtB8"
                text="DES key is: " + DES_KEY + " \nDES IV is: " + DES_IV + " \nDES Mode is CFB"
                st.text(text)
                st.error("Note the above details for decrypting the file")
                encryptor = DES.new(DES_KEY.encode("utf-8"), DES.MODE_CFB, DES_IV.encode("utf-8"))
                encrypted_audio = encryptor.encrypt(contents)
                st.write('<h5 style="color:blue">Your Encrypted File</h5>',unsafe_allow_html=True)
                st.download_button(label="Encrypted file",data=encrypted_audio,file_name="DES_encry.wav",mime="audio/wav")
            
            elif choice=="Triple DES":
                with open('uploaded-audio.wav', 'rb') as fd:
                    contents = fd.read()
                size=st.selectbox("Choose an key size(in bits)",[192,128])
                size=size//8
                text="Triple DES key is: " + str(size) + " bytes " + " \nTriple DES Mode is OFB" +"\nTriple DES IV is: 8 bytes"
                st.text(text)
                if size==24:
                    tdk=b'mE4\xeca8nd\xf2]\xb5\xce8d\x83\xad\xa2\x07\x94C\x9b,>\xef'
                else:
                    tdk=b'\xa8\xcbgb\x86m,;\x80\xc7y\xbaX\xcd\xdc;'
                iv=b'\x8c\x15B3@C\xc2\xe9'
                cipher=DES3.new(tdk,DES3.MODE_OFB,iv)
                ciphertext=cipher.encrypt(contents)
                st.write('<h5 style="color:red">DES3 IV (binary file)</h5>',unsafe_allow_html=True)
                st.download_button(label="DES3 IV",data=iv,file_name="DES3_IV.bin")
                st.write('<h5 style="color:red">DES3 Key (binary file)</h5>',unsafe_allow_html=True)
                st.download_button(label="DES3 KEY",data=tdk,file_name="DES3_Key.bin")
                st.write('<h5 style="color:blue">Your Encrypted File</h5>',unsafe_allow_html=True)
                st.download_button(label="Encrypted file",data=ciphertext,file_name="DES3_encry.wav",mime="audio/wav")
            
            elif choice=="Fernet":
                with open('uploaded-audio.wav','rb') as fd:
                    contents=fd.read()
                key = b'I5npNdMjN8slZDdtJ_tAgCN15itiwfvk-QDDEPMCnaU='
                fernet = Fernet(key)
                text="Fernet Key Size is: 32 bytes"
                st.text(text)
                encrypted = fernet.encrypt(contents)
                st.write('<h5 style="color:red">Fernet Key (binary file)</h5>',unsafe_allow_html=True)
                st.download_button(label="Fernet key",data=key,file_name="fernet_key.bin")
                st.write('<h5 style="color:blue">Your Encrypted File</h5>',unsafe_allow_html=True)
                st.download_button(label="Encrypted file",data=encrypted,file_name="Fernet_encry.wav",mime="audio/wav")
            
            elif choice=="ECC":
                with open('uploaded-audio.wav','rb') as fd:
                    contents=fd.read()
                ecc_private_key=st.text_input("Enter Private Key: ")
                if ecc_private_key:
                    ecc_key= seccure.passphrase_to_pubkey(ecc_private_key.encode("utf-8"))
                    ecc_key=str(ecc_key).encode("utf-8")
                    encrypted_audio = seccure.encrypt(contents,ecc_key)
                    st.write('<h5 style="color:blue">Your Encrypted File</h5>',unsafe_allow_html=True)
                    st.error("Remember Your Private Key for decrypting the file")
                    st.download_button(label="Encrypted file",data=encrypted_audio,file_name="ECC_encry.wav",mime="audio/wav")
                 
            
            elif choice=="AES with RSA":
                with open('uploaded-audio.wav', 'rb') as fd:
                    contents = fd.read()
                    
                #size=st.selectbox("Choose an key size(in bits)",[128,192,256])
                #size=size//8
                rsa_size=st.selectbox("Choose an RSA key(in bits)",[2048,1024,4096],key="encry_AES_with_RSA")
                rsa_path="AES+RSA//"+str(rsa_size)
                AES_KEY = 'bZAKPo6kIuHzXmSY'
                AES_IV = 'N9lwkIK58DNwV2GE'
                text="AES key is: " + AES_KEY + " \nAES IV is: " + AES_IV + " \nAES Mode is CFB"
                st.text(text)
                cipher=AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
                ciphertext = cipher.encrypt(contents)
                with open(rsa_path + "//private_key.bin") as f:
                    private_key=f.read()
                st.write('<h5 style="color:blue">Your Encrypted File</h5>',unsafe_allow_html=True)
                st.download_button(label="Encrypted file",data=ciphertext,file_name="AES+RSA_encry.wav",mime="audio/wav")
                st.write('<h5 style="color:red">Download your private key</h5>',unsafe_allow_html=True)
                st.download_button(label="Private Key",data=private_key,file_name="Private_key.bin")
                
                
    with decrypt:
        st.subheader("Decryption: ")
        decrypt_choice=st.selectbox("Choose an Algorithm",["AES","DES","AES with RSA","Triple DES","Fernet","ECC"],key="decrypt")
        upload_file_decrypt=st.file_uploader("Choose a wav file",type=["wav"],key="decrypt_file")
        if upload_file_decrypt is not None:
            bytes_data=upload_file_decrypt.getvalue()
            with open('uploaded-audio_decrpyt.wav', 'wb') as fw:
                fw.write(bytes_data)
                
            if decrypt_choice=="AES":
                with open('uploaded-audio_decrpyt.wav', 'rb') as fd:
                    contents = fd.read()
                aes_key=st.text_input("Enter the AES Key to decrpyt",key="placeholder-1")
                aes_iv=st.text_input("Enter the AES IV to decrpyt",key="placeholder-2")
                if aes_key and aes_iv:
                    decryptor = AES.new(aes_key.encode("utf-8"), AES.MODE_CFB, aes_iv.encode("utf-8"))
                    decrypted_audio = decryptor.decrypt(contents)
                    st.write('<h5 style="color:red">Your Decrypted File</h5>',unsafe_allow_html=True)
                    st.download_button(label="Decrypted file",data=decrypted_audio,file_name="AES_decry.wav",mime="audio/wav")
            
            elif decrypt_choice=="DES":
                with open('uploaded-audio_decrpyt.wav', 'rb') as fd:
                    contents = fd.read()
                des_key=st.text_input("Enter the DES Key to decrpyt",key="placeholder-3")
                des_iv=st.text_input("Enter the DES IV to decrpyt",key="placeholder-4")
                if des_key and des_iv:
                    decryptor = DES.new(des_key.encode("utf-8"), DES.MODE_CFB, des_iv.encode("utf-8"))
                    decrypted_audio = decryptor.decrypt(contents)
                    st.write('<h5 style="color:red">Your Decrypted File</h5>',unsafe_allow_html=True)
                    st.download_button(label="Decrypted file",data=decrypted_audio,file_name="DES_decry.wav",mime="audio/wav")
            
            elif decrypt_choice=="Triple DES":
                with open('uploaded-audio_decrpyt.wav', 'rb') as fd:
                    contents = fd.read()
                des3_key=st.file_uploader("DES3 key: ",type=["bin"],key="des_3_key")
                des3_iv=st.file_uploader("DES3 iv: ",type=["bin"],key="des_3_iv")
                
                if des3_key is not None and des3_iv is not None:
                    cipher=DES3.new(des3_key.getvalue(),DES3.MODE_OFB,des3_iv.getvalue())
                    plaintext=cipher.decrypt(contents)
                    st.write('<h5 style="color:red">Your Decrypted File</h5>',unsafe_allow_html=True)
                    st.download_button(label="Decrypted file",data=plaintext,file_name="DES3_decry.wav",mime="audio/wav")
            
            elif decrypt_choice=="Fernet":
                with open('uploaded-audio_decrpyt.wav', 'rb') as fd:
                    contents = fd.read()
                fernet_key=st.file_uploader("Fernet key: ",type=["bin"],key="fer_key")
                if fernet_key is not None:
                    fernet = Fernet(fernet_key.getvalue())
                    decrypted = fernet.decrypt(contents)
                    st.write('<h5 style="color:red">Your Decrypted File</h5>',unsafe_allow_html=True)
                    st.download_button(label="Decrypted file",data=decrypted,file_name="Fernet_decry.wav",mime="audio/wav")
            
            elif decrypt_choice=="ECC":
                with open('uploaded-audio_decrpyt.wav', 'rb') as fd:
                    contents = fd.read()
                ecc_private_key=st.text_input("Enter Your Private Key")
                if ecc_private_key:
                    decrypted_audio=seccure.decrypt(contents,ecc_private_key.encode("utf-8"))
                    st.write('<h5 style="color:red">Your Decrypted File</h5>',unsafe_allow_html=True)
                    st.download_button(label="Decrypted file",data=decrypted_audio,file_name="ECC_decry.wav",mime="audio/wav")
                  
                
            elif decrypt_choice=="AES with RSA":
                rsa_size=st.selectbox("Choose an RSA key(in bits)",[2048,1024,4096],key="decry_AES_with_RSA")
                rsa_path="AES+RSA//"+str(rsa_size)
                private_key_upload=st.file_uploader("Private Key file: ",type=["bin"],key="private_key_bin")
                with open('uploaded-audio_decrpyt.wav', 'rb') as fd:
                    ciphertext = fd.read()
                with open(rsa_path+"//encrypted_aes_key.bin", "rb") as f:
                    encrypted_aes_key = f.read()
                with open(rsa_path+"//encrypted_iv.bin", "rb") as f:
                    encrypted_iv = f.read()
                if private_key_upload is not None:
                    private_key = RSA.import_key(private_key_upload.getvalue())
                    cipher_rsa = PKCS1_OAEP.new(private_key)
                    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
                    iv = cipher_rsa.decrypt(encrypted_iv)
                    # Decrypt the audio file with AES
                    cipher = AES.new(aes_key, AES.MODE_CFB, iv)
                    audio_data = cipher.decrypt(ciphertext)
                    if audio_data:
                        st.write('<h5 style="color:red">Your Decrypted File</h5>',unsafe_allow_html=True)
                        st.download_button(label="Decrypted file",data=audio_data,file_name="RSA+AES_decry.wav",mime="audio/wav")
                    
else:
    st.write('<h1 style="color:crimson;">Message Encryption and Decryption</h1>', unsafe_allow_html=True)
    encrypt,decrypt=st.columns(spec=[1,1],gap="large")
    with encrypt:
        st.title("Encryption: ")
        size=st.selectbox("Choose an key size(in bytes)",[128,192,256])
        rsa_path="keys//"+str(size)
        with open(rsa_path+"//publicKey.pem",'rb') as p:
            publicKey=rsa.PublicKey.load_pkcs1(p.read())
        input_text=st.text_input("Enter the message")
        if input_text:
            ciphertext=rsa.encrypt(input_text.encode("ascii"),publicKey)
            text="Algorithm Used is: RSA" +"\nHashing Algorithm for Signature is SHA-1"
            st.text(text)
            st.write('<h5 style="color:blue">Your Encrypted Message</h5>',unsafe_allow_html=True)
            st.download_button(label="Encrypted file",data=ciphertext,file_name="RSA_mssg_encry.bin")
            
            
    with decrypt:
        st.title("Decryption: ")
        size=st.selectbox("Key size (in bytes)",[128,192,256])
        rsa_path="keys//"+str(size)
        with open(rsa_path+"//publicKey.pem",'rb') as p:
            publicKey=rsa.PublicKey.load_pkcs1(p.read())
        with open(rsa_path+"//privateKey.pem",'rb') as p:
            privateKey=rsa.PrivateKey.load_pkcs1(p.read())
        upload_file_decrypt=st.file_uploader("Encrypted file",type=["bin"],key="decrypt_file")
        if upload_file_decrypt is not None:
            text=rsa.decrypt(upload_file_decrypt.getvalue(),privateKey)
            st.write('<h5 style="color:red">Decrypted Message</h5>',unsafe_allow_html=True)
            st.success(text.decode("utf-8"))
            
        
        
            
            
            
            
        
            
            
    
    
            
            
            
            
            
            
            
            
        
