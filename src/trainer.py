import cv2
import numpy
import os
from PIL import Image

class Trainer:

    # Iniciando reconhecedor
    recognizer = cv2.createLBPHFaceRecognizer();

    # Buscando amostras convertando para array de bits e ids
    def getSamplesId(self, path):
        paths = [os.path.join(path, f) for f in os.listdir(path)];
        faces = [];
        ids   = [];

        for path in paths:
            image      = Image.open(path).convert('L');
            numpyImage = numpy.array(image, 'uint8');

            faces.append(numpyImage);
            ids.append(int(path.split('.')[1]));
            cv2.imshow('training', numpyImage);
            cv2.waitKey(10);

        return numpy.array(ids), faces;

    # Treinar e gerar arquivo de treino
    def train(self):        
        ids, faces = self.getSamplesId('samples');

        self.recognizer.train(faces, ids);
        self.recognizer.save('trainning/data.yml');
        cv2.destroyWindow('training');
