# Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

# Funciones utiles
def rgb2hsv(r,g,b):
    # obtain hsv coordinates 
    assert type(r)==int and type(g)==int and type(b)==int, 'Invalid coordinates'
    pixel_color = np.array([[[r, g, b]]], dtype=np.uint8)
    pixel_color_hsv = cv2.cvtColor(pixel_color, cv2.COLOR_RGB2HSV)
    return pixel_color_hsv[0][0]

def rgb2lab(r,g,b):
    pixel_color = np.uint8([[(b, g, r)]])

    # Convertir a espacio de color BGR a LAB
    color_bgr = cv2.cvtColor(pixel_color, cv2.COLOR_RGB2BGR)
    color_lab = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2Lab)

    # Extraer los valores LAB del píxel
    return color_lab[0][0]

# Create class that contains all the processes
class ColorSelector:
    def __init__ (self,imagePath: str, colorNumber=13):
        self.imagePath = imagePath
        self.colorNumber = colorNumber
        
        # eventually save colors
        self.colors = []

        # load image
        self.image = cv2.cvtColor(cv2.imread(self.imagePath), cv2.COLOR_BGR2RGB)

        # preprocessing
        kernel = np.ones((3, 3), np.uint8)
        self.preprocessed = cv2.erode(self.image, kernel, iterations=1)

        # imagen para comparar (inicialmente no se guarda nada)
        self.compare = None

    def loadImage2Compare(self, image_path):
        self.compare = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        return self.compare
    
    def visualizeImage(self):
        plt.imshow(self.image)
        plt.axis('off')
        plt.show()
    
    def getcolorNumber(self):
        return self.colorNumber
    
    def getPreprocessedImage(self):
        return self.preprocessed

    def selectColoNumber(self, maxIt = 20):
        # method to select the required number of clusters using inertia -> select k with the minimum inertia
        assert maxIt>=2,'The minimum number of clusters must be 2'
        inertia_scores = []
        for k in range(2, maxIt): 
            kmeans = KMeans(n_clusters=k)
            labels = kmeans.fit_predict(self.preprocessed) 
            inertia_scores.append(kmeans.inertia_)

        optimal_k = inertia_scores.index(min(self.self.preprocessed)) + 2
        return optimal_k
    
    
    def obtainColors(self, trySelectColorsNumber = False):

        if trySelectColorsNumber:
            self.colorNumber = self.selectColoNumber()

        # modify image to get pixel label
        modified_image = self.preprocessed.reshape(self.preprocessed.shape[0]*self.preprocessed.shape[1], 3)

        #fit kmeans algorithm
        print('Fitting KMeans')
        clf = KMeans(n_clusters = self.colorNumber)
        self.labels = clf.fit_predict(modified_image)

        # obtain the colors as centroids
        colors = clf.cluster_centers_.astype(int)
        self.colors = colors

        # show image with all detected colors
        width = 1000
        height_per_color = 250
        empty_image = np.zeros(((1+self.colorNumber)*height_per_color, width, 3), dtype=np.uint8)+255

        rgb = []
        hsv = []
        lab = []

        for i in range(len(colors)):
            center = (width - 150,(i+1)*height_per_color+10)
            color = (int(colors[i][0]),int(colors[i][1]),int(colors[i][2]))
            rgb.append(color)
            empty_image = cv2.circle(empty_image, center, 100, color, -1)

            # colocar las coordenadas en rgb
            text = f"RGB {(int(colors[i][0]),int(colors[i][1]),int(colors[i][2]))}"
            position = (100, (i+1)*height_per_color-60)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)
            
            # colocar las coordenadas en hsv
            hsv_color = rgb2hsv(color[0],color[1],color[2])
            hsv.append(hsv_color)
            text = f"HSV {(hsv_color[0],hsv_color[1],hsv_color[2])}"
            position = (100, (i+1)*height_per_color+10)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)
            
            # colocar las coordenadas en lab
            lab_color = rgb2lab(color[0],color[1],color[2])
            lab.append(lab_color)
            text = f"LAB {(lab_color[0],lab_color[1],lab_color[2])}"
            position = (100, (i+1)*height_per_color+80)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)

        # plt.imshow(empty_image)

        return rgb,hsv,lab,empty_image
    
    def createCSV(self,rgb_list,lab_list,hsv_list, save_path):
        df = pd.DataFrame([{'rgb':rgb_list[i],'lab':lab_list[i], 'hsv':hsv_list[i]} for i in range(len(rgb_list))])
        df.to_csv(save_path+'/resultados.csv')
        return df
            
    def obtainMasks(self):
        # matriz donde cada coordenada de la imagen tiene un label asignado en el clustering
        reshaped_labels = self.labels.reshape(self.preprocessed.shape[:2])

        # crear las mascaras - se va a mostrar en la imagen los lugares donde fueron
        # encontrados los colores
        # en este ejemplo se toma el grupo i entre [0,12]
        i = 8
        mask_i = np.copy(self.preprocessed)

        # Cambiar los valores
        mask_i[reshaped_labels != i] = [0,0,0]


    # ES POSIBLE REALIZAR LA OBTENCION DE COLORES CON UNA REGION DE INTERES
    def getROI(self, xleft,xright,yup,ylow):
        # select a region of interest given the coordinates of the region
        return self.image[int(ylow):int(yup), int(xleft):int(xright)]



    def obtainColorsGradientImage(self):
        pixels = self.preprocessed.reshape((-1, 3))

        # Apply Kmeans to get color segmentation
        kmeans = KMeans(n_clusters=self.colorNumber)
        kmeans.fit(pixels)

        # Get the labels of each pixel
        labels = kmeans.labels_

        # Create an image with the center colors of each cluster
        cluster_centers = kmeans.cluster_centers_.astype(int)
        segmented_image = cluster_centers[labels].reshape(self.image.shape)

        # Get the rgb coordinates of each color
        colors = kmeans.cluster_centers_.astype(int)

        # Create an image with the coordinates in rgb
        width = 900
        empty_image = np.zeros((self.colorNumber*140, width, 3), dtype=np.uint8)+255

        for i in range(len(colors)):
            center = (width - 100,(i+1)*129)
            color = (int(colors[i][0]),int(colors[i][1]),int(colors[i][2]))
            empty_image = cv2.circle(empty_image, center, 60, color, -1)

            text = f"RGB {(int(colors[i][0]),int(colors[i][1]),int(colors[i][2]))}"
            position = (100, (i+1)*130)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)

        return segmented_image

    def compare_with_new_image(self, rgb_original):
        # preprocesar
        kernel = np.ones((3, 3), np.uint8)

        assert (self.compare != None).all(), 'Se debe guardar la imagen a comparar'
        aComparar = self.compare
        preprocessed = cv2.erode(aComparar, kernel, iterations=1)

        modified_image = preprocessed.reshape(preprocessed.shape[0]*preprocessed.shape[1], 3)

        #fit kmeans algorithm
        print('Fitting KMeans')
        clf = KMeans(n_clusters = self.colorNumber)
        labels = clf.fit_predict(modified_image)

        # obtain the colors as centroids
        colors = clf.cluster_centers_.astype(int)

        # show image with all detected colors
        width = 1000
        height_per_color = 250
        empty_image = np.zeros(((1+self.colorNumber)*height_per_color, width, 3), dtype=np.uint8)+255

        rgb = []
        hsv = []
        lab = []

        for i in range(len(colors)):
            center = (width - 150,(i+1)*height_per_color+10)
            color = (int(colors[i][0]),int(colors[i][1]),int(colors[i][2]))
            rgb.append(color)
            empty_image = cv2.circle(empty_image, center, 100, color, -1)

            # colocar las coordenadas en rgb
            text = f"RGB {(int(colors[i][0]),int(colors[i][1]),int(colors[i][2]))}"
            position = (100, (i+1)*height_per_color-60)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)
            
            # colocar las coordenadas en hsv
            hsv_color = rgb2hsv(color[0],color[1],color[2])
            hsv.append(hsv_color)
            text = f"HSV {(hsv_color[0],hsv_color[1],hsv_color[2])}"
            position = (100, (i+1)*height_per_color+10)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)
            
            # colocar las coordenadas en lab
            lab_color = rgb2lab(color[0],color[1],color[2])
            lab.append(lab_color)
            text = f"LAB {(lab_color[0],lab_color[1],lab_color[2])}"
            position = (100, (i+1)*height_per_color+80)
            cv2.putText(empty_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0,0,0), 4)

        
        # comparar con los resultados de la imagen original
        # se calcula la distancia euclidea en el espacio de color rgb
        comparaciones = []
        for i, coord1 in enumerate(rgb_original):
            resultados = {}
            distancias = [np.linalg.norm(np.array(coord1) - np.array(coord2)) for coord2 in rgb]

            # resultados['Indice'] = i
            resultados['Color original (RGB)'] = coord1
            resultados['Color original (LAB)'] = rgb2lab(coord1[0],coord1[1],coord1[2])
            resultados['Color original (HSV)'] = rgb2hsv(coord1[0],coord1[1],coord1[2])
            resultados['Indice correspondiente a menor distancia'] = np.argmin(distancias)
            coord2 = rgb[resultados['Indice correspondiente a menor distancia']]
            resultados['Color correspondiente (RGB)'] = coord2
            resultados['Color correspondiente (LAB)'] = rgb2lab(coord2[0],coord2[1],coord2[2])
            resultados['Color correspondiente (LAB)'] = rgb2hsv(coord2[0],coord2[1],coord2[2])
            resultados['Distancia Euclideana en RGB'] = np.min(distancias)
            comparaciones.append(resultados)

        self.comparaciones = comparaciones
        return comparaciones
    
    def saveComparisons(self, file_path):
        df = pd.DataFrame(self.comparaciones)
        df.to_csv(file_path+'/resultados.csv')

    def visualize_comparison(self, resultados):
        # visualizar las comparaciones
        width = 600
        height_per_color = 250
        image_comparaciones = np.zeros(((1+self.colorNumber)*height_per_color, width, 3), dtype=np.uint8)+255


        for i in range(len(resultados)):
            color_original = resultados[i]['Color original (RGB)']
            # color_original = comparaciones['Color original'].iloc[i]
            color_comparacion = resultados[i]['Color correspondiente (RGB)']
            
            center = (width - 150,(i+1)*height_per_color+10)
            image_comparaciones = cv2.circle(image_comparaciones, center, 100, color_comparacion, -1)

            center = (width - 400,(i+1)*height_per_color+10)
            image_comparaciones = cv2.circle(image_comparaciones, center, 100, color_original, -1)

        plt.axis('off')
        plt.imshow(image_comparaciones)
