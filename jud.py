def judge(a, b, t, w):
    #a = 125.0 ## tyou hen
    #b = 20.0 ## tan hen
    #t = 2.0 ## atusa
    #w = 400.0 ## omosa
    
    #mode = 0 #1..hagaki, 2..teikei, 3..gai, 4..nasi
    if a <= 16.4 and b <= 9.2 and t <= 1.0 and w <= 6.0:
        return 63 #mini reta-
    if a <= 14.8 and b <= 10.0 and t <= 1.0 and w <= 25.0:
        return 63 #hagaki
    
    if a <= 23.5 and b <= 12.0 and t <= 1.0:
        if w < 25.0:
            return 84
        elif w < 50.0:
            return 94
        
    if a <= 34.0 and b <= 25.0 and t <= 3.0:
        if w < 50.0:
            return 120
        elif w < 100.0:
            return 140
        elif w < 150.0:
            return 210
        elif w < 250.0:
            return 250
        elif w < 500.0:
            return 390
        elif w < 1000.0:
            return 580
        
    return 0