import cv2
import numpy
import databaseHelper
import os.path
import trainer
import wx

class Detector:

    # Intancias das outras classes
    dbHelper       = databaseHelper.DbHelper();
    trainning      = trainer.Trainer();

    # Modelo a ser detectado
    haarCascade    = '../haarcascade/haarcascade_frontalface_alt.xml';
    faceDetect     = cv2.CascadeClassifier(haarCascade);

    # Preparar camera
    camera         = cv2.VideoCapture(0);

    # Preparar reconhecedor (raio, vizinhos, tabela_x, tabela_y, confianca)
    recognizer     = cv2.createLBPHFaceRecognizer(1, 8, 8, 8, 100);

    # Fontes
    textFont       = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 1.5, 1, 0, 2);
    controlsFont   = cv2.FONT_HERSHEY_SIMPLEX;

    # Propriedades das amostras
    userIdSample   = 0;
    userNameSample = '';
    sampleId       = 0;

    # Flag para ligar o modo captura
    captureMode    = False;

    # wxPython (GUI)
    dialog         = wx.App();

    # Carreagar Treino Padrão
    recognizer.load("trainning\\data.yml");

    # Alerta com input do nome
    def getUserName(parent = None):
        dlg = wx.TextEntryDialog(parent, 'Qual o seu nome?');
        dlg.ShowModal();
        
        result = dlg.GetValue();
        
        dlg.Destroy();
        
        return result
    
    while(True):
        frame, image = camera.read();
        grayConvert  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
        faces        = faceDetect.detectMultiScale(grayConvert, 1.3, 5);
        
        for(x, y, w, h) in faces:           
            userId, conf = recognizer.predict(grayConvert[y:y+h, x:x+w]);
            userName     = dbHelper.getNameById(userId);

            if(userId == -1 or not(userName)):
                userName = "Nao reconhecido"

            # Retangulo e nome do usuario
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2);
            cv2.cv.PutText(cv2.cv.fromarray(image), userName, (x, y+h), textFont, (0, 0, 255));

            # Iniciar Captura
            if(captureMode == True):
                sampleId = sampleId + 1;
                cv2.imwrite('samples/' + userNameSample + '.' + str(userIdSample) + '.' + str(sampleId) + '.jpg', grayConvert[y:y+h, x:x+w]);
                cv2.putText(image,'Capturando...',(420, 30), controlsFont, 1,(255,255,255),2,cv2.CV_AA);
                cv2.waitKey(10);

        # Terminar captura e treinar
        if(sampleId > 20):
            sampleId    = 0;
            captureMode = False;
            trainning.train();

            recognizer = cv2.createLBPHFaceRecognizer(1, 8, 8, 8, 100);
            recognizer.load("trainning\\data.yml");

        # Demais textos
        cv2.putText(image,'Faculdade Ateneu',(10,30), controlsFont, 1,(255,255,255),2,cv2.CV_AA);
        cv2.putText(image,'Controles:',(10,350), controlsFont, 1,(255,255,255),2,cv2.CV_AA);
        cv2.putText(image,'N -> Novo rosto',(20,390), controlsFont, 0.7,(255,255,255),2,cv2.CV_AA);
        cv2.putText(image,'Q -> Sair',(20,430), controlsFont, 0.7,(255,255,255),2,cv2.CV_AA);
        cv2.putText(image,'Criadores: David e Jadson',(420, 450), controlsFont, 0.5,(255,255,255),1,cv2.CV_AA);
        cv2.putText(image,'Versao: 1.0.0',(420, 470), controlsFont, 0.5,(255,255,255),1,cv2.CV_AA);

        # Tela
        cv2.imshow("Face Detector", image);

        # Sair da aplicação
        if(cv2.waitKey(1) == ord('q')):
            break;

        # Nova leitura
        if(cv2.waitKey(1) == ord('n')):
            dialog.MainLoop();
            userNameSample = getUserName();

            if(userNameSample):
                captureMode  = True;
            
                dbHelper.firstOrUpdate(userNameSample);
                
                userIdSample = dbHelper.getIdByName(userNameSample);
            

    camera.release();
    cv2.destroyAllWindows();
    
