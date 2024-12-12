<h1 align="center">
    <img src ="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&center=true&vCenter=true&width=500&height=70&duration=5000&lines=PLT+API+Detection;" />
</h1>

<h3 align="left">Step by step: </h3>

1.  **install dependecy #pip install flask torch torchvision pillow**

2.  **jalankan program #python (namafile).py ~contoh python detection.py**
    ![image](https://github.com/user-attachments/assets/4315bee3-873b-4349-bee5-7268c5920d51)

3. **Install ngrok & Sign In ke ngrok**
   https://dashboard.ngrok.com/get-started/setup/windows

4. **Buka Powershell, ketik #choco install ngrok , lalu pilih Y**
   
5. **Masukkan authtoken**
    ~contoh : ngrok config add-authtoken 2q53Mo2cuS4xGQ6z9VEfbRHe5kU_47NSRhMGJZ3wPvYtbh95e

6. **Masukkan ngrok http nya, ~contoh : ngrok http 5002**
   ![image](https://github.com/user-attachments/assets/b284c8e2-05c6-403e-ad04-ad580f521f36)


7.  **buka Postman**

8.  **klik New**

9.  **pilih HTTP**

10.  salin link https://40e2-180-243-4-125.ngrok-free.app/predict (link ngrok akan berubah setiap saat)
   
11.  method pilih POST
    ![image](https://github.com/user-attachments/assets/7e588ded-c89c-45f1-b189-80a819fba144)


12.  buka tab bagian Body, pilih form-data, untuk Key isi "image" berupa file, Value berisi hasil upload gambar
    ![image](https://github.com/user-attachments/assets/c3149b28-db42-4309-a3cf-6c01a26712a5)


13.  pilih file gambar

14. setelah file di upload kemudian send
    ![image](https://github.com/user-attachments/assets/c3c3968c-331e-4599-9eb8-1215ca8b1c9a)

15. jika berhasil, akan muncul seperti ini :
    ![image](https://github.com/user-attachments/assets/34f7c466-ad66-4d6c-ba19-46a59d8e727e)

