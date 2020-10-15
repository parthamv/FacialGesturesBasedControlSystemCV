import numpy as np

def eye_aspect_ratio(eye):
    #vertical    
    A=np.linalg.norm(eye[1]-eye[5])    
    B=np.linalg.norm(eye[2]-eye[4])    
    #horizontal
    C=np.linalg.norm(eye[0]-eye[3])
    #ear-ratio
    ear=(A+B)/(2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    #vertical
    A=np.linalg.norm(mouth[13]-mouth[19])
    B=np.linalg.norm(mouth[14]-mouth[18])
    C=np.linalg.norm(mouth[15]-mouth[17])
    #horizontal
    D=np.linalg.norm(mouth[12]-mouth[16])
    #mar-ratio
    mar=(A+B+C)/(2*D)
    return mar

    