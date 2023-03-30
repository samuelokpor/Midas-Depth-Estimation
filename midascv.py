#Import Dependencies
import cv2
import torch
from matplotlib import pyplot as plt

#Download the Midas 
midas = torch.hub.load('intel-isl/MiDas', 'MiDaS_small')
midas.to('cuda')
midas.eval()

#Input transformation Pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform

#Hook into OpenCV
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()


    #Transform input for midas
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to('cuda')

    #make a prediction
    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size= img.shape[:2],
            mode='bicubic',
            align_corners=False
        ).squeeze()

        output = prediction.cpu().numpy()

        print(output)
    plt.imshow(output)
    cv2.imshow('CV2Frame', frame)
    plt.pause(0.00001)

    if cv2.waitKey(10) & 0XFF== ord('q'):
        cap.release()
        cv2.destroyAllWindows()

plt.show()